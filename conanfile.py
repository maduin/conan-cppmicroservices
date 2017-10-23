from conans import ConanFile, CMake, tools
import os

class CppMicroServicesConan(ConanFile):
    name = "CppMicroServices"
    version = "3.0.0"
    license = "Apache-2.0 (https://github.com/CppMicroServices/CppMicroServices/blob/master/LICENSE)"
    url = "https://github.com/maduin/conan-cppmicroservices"
    description = "An OSGi-like C++ dynamic module system and service registry"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "CMakeLists.txt"

    source_url = "https://github.com/CppMicroServices/CppMicroServices/archive/v{version}.zip".format(version=version)
    zip_dir = "CppMicroServices-{version}".format(version=version)
    major_version = version.split(".")[0]

    def source(self):
        tools.get(self.source_url)
        os.rename(os.path.join(self.zip_dir, "CMakeLists.txt"), os.path.join(self.zip_dir, "CMakeListsOriginal.txt"))
        os.rename("CMakeLists.txt", os.path.join(self.zip_dir, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["US_BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_dir=os.path.join(self.source_folder, self.zip_dir))
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = ["include/cppmicroservices{major_version}".format(major_version=self.major_version)]
        self.cpp_info.libs = ["CppMicroServices{major_version}".format(major_version=self.major_version)]

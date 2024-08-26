from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import copy, get
import os


class JoltPhysicsRecipe(ConanFile):
    name = "joltphysics"
    version="1.0"
    description = (
        "A multi core friendly rigid body physics and collision detection "
        "library, written in C++, suitable for games and VR applications."
    )
    license = "MIT"
    topics = ("physics", "simulation", "physics-engine", "physics-simulation", "rigid-body", "game", "collision")
    homepage = "https://github.com/engine3d-dev/JoltPhysics"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = "Build/*", "Jolt/*", "TestFramework/*", "HelloWorld/*", "Samples/*", "UnitTests/*", "JoltViewer/*", "PerformanceTest/*", "Assets/*"

    def requirements(self):
        self.tool_requires("make/4.4.1")
        self.tool_requires("cmake/3.27.1")


    @property
    def _min_cppstd(self):
        return "20"
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self, generator="Unix Makefiles")
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.configure(build_script_folder=os.path.join(self.source_folder, "Build"))
        cmake.build()
    
    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "Jolt"), dst=os.path.join(self.package_folder, "."))
        copy(self, pattern="*.h", src=os.path.join(self.source_folder, "Jolt"), dst=os.path.join(self.package_folder, ".\Jolt"))
        copy(self, pattern="*.cpp", src=os.path.join(self.source_folder, "Jolt"), dst=os.path.join(self.package_folder, "."))
        copy(self, pattern="*.cpp", src=os.path.join(self.source_folder, "Jolt"), dst=os.path.join(self.package_folder, ".\Jolt"))
        copy(self, pattern="*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.so", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        copy(self, pattern="*.dll", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)
        copy(self, pattern="*.dylib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        cmake = CMake(self)
        cmake.install()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "Jolt::Jolt")
        self.cpp_info.libs = ["Jolt"]
        # self.cpp_info.includedirs = ['./', 'Jolt']
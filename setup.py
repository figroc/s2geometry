import os
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.dirname(self.get_ext_fullpath(ext.name))
        extdir = os.path.abspath(os.path.join(extdir, ext.name))

        cmake_args = ["-DBUILD_PYWRAPS2=ON",
                      "-DBUILD_SHARED_LIBS=OFF",
                      "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY="+extdir,
                      "-DCMAKE_SWIG_OUTDIR="+extdir,
                      "-DPYTHON_EXECUTABLE="+sys.executable]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += ["-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(
                cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args,
                              cwd=self.build_temp)
        subprocess.check_call(["cmake", "--build", "."] + build_args,
                              cwd=self.build_temp)


class FilterBuildPy(build_py):
    @staticmethod
    def _excl_(modules):
        return [(m, n, f) for m, n, f in modules
                if n not in ["pywraps2_test", "setup"]]

    def find_modules(self):
        return self._excl_(super().find_modules())

    def find_package_modules(self, package, package_dir):
        return self._excl_(super().find_package_modules(package, package_dir))


setup(
    name="s2geometry",
    version="0.9.0",
    python_requires=">=3.4",

    packages=["s2geometry"],
    package_dir={"s2geometry": "src/python"},
    ext_modules=[CMakeExtension("s2geometry")],
    cmdclass=dict(build_ext=CMakeBuildExt,
                  build_py=FilterBuildPy),

    license="Apache-2.0",
    url="https://github.com/figroc/s2geometry",
    description="Computational geometry and spatial indexing on the sphere",
    long_description="\n".join([
        "A setuptools wrapper around [s2geometry](https://github.com/google/s2geometry).",
        "Notes: All credit goes to Google; this is just a wrapper around their lib.",
        "", "Inspired by [s2-py](https://github.com/mira/s2-py)."]),
    long_description_content_type="text/plain",
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: Apache Software License",
                 "Operating System :: POSIX",
                 "Programming Language :: Python :: 3",
                 "Topic :: Scientific/Engineering :: GIS",
                 "Topic :: Software Development :: Libraries :: Python Modules"],
    author="Figroc Chen",
    author_email="figroc@gmail.com",
)

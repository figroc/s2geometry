import os
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.dirname(self.get_ext_fullpath(ext.name))
        extdir = os.path.abspath(os.path.join(extdir, ext.name))

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DCMAKE_SWIG_OUTDIR=' + extdir,
                      '-DSWIG_OUTFILE_DIR=' + self.build_temp,
                      '-DPYTHON_EXECUTABLE=' + sys.executable,
                      '-DBUILD_SHARED_LIBS=OFF']

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
                cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args,
                              cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)
        print()


class SelectBuildPy(build_py):
    @staticmethod
    def _excl_(modules):
        return [(m, n, f) for m, n, f in modules
                if n not in ['pywraps2_test', 'setup']]

    def find_modules(self):
        return self._excl_(super().find_modules())

    def find_package_modules(self, package, package_dir):
        return self._excl_(super().find_package_modules(package, package_dir))


setup(
    name='s2geometry',
    version='0.9.0',
    packages=['s2geometry'],
    package_dir={'s2geometry': 'src/python'},
    ext_modules=[CMakeExtension('s2geometry')],
    cmdclass=dict(build_ext=CMakeBuildExt,
                  build_py=SelectBuildPy),
)

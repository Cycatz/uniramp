# Copyright (c) 2020, Yung-Yu Chen <yyc@solvcon.net>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software without
#   specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pathlib
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


# Taken from https://stackoverflow.com/a/48015772
class CMakeExtension(Extension):
    def __init__(self, name, **kwa):
        super().__init__(name, sources=[])


class cmake_build_ext(build_ext):

    user_options = build_ext.user_options + [
        ('cmake-args=', None, 'arguments to cmake'),
        ('make-args=', None, 'arguments to make'),
    ]

    def initialize_options(self):

        super().initialize_options()
        self.cmake_args = ''
        self.make_args = ''

    def finalize_options(self):

        super().finalize_options()

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):

        cwd = pathlib.Path().absolute()

        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name)).parent
        extdir.mkdir(parents=True, exist_ok=True)

        local_cmake_args = '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}'.format(
            str(extdir.absolute()))

        subprocess.run(
            'cmake {} {} {}'.format(cwd, local_cmake_args, self.cmake_args),
            shell=True,
            cwd=str(build_temp))

        target_name = ext.name.split('.')[-1]
        subprocess.run(
            'make {} {}'.format(target_name, self.make_args),
            shell=True,
            cwd=str(build_temp))


def main():

    setup(
        name="uniramp",
        version="0.0",
        packages=[
            'uniramp',
        ],
        ext_modules=[CMakeExtension("uniramp._uniramp")],
        cmdclass={'build_ext': cmake_build_ext},
    )


if __name__ == '__main__':
    main()

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

# Build uniramp Python extension (even when the timestamp is clean):
#   make
# Build verbosely:
#   make VERBOSE=1
# Build with clang-tidy
#   make USE_CLANG_TIDY=ON

SETUP_FILE ?= ./setup.mk

ifneq (,$(wildcard $(SETUP_FILE)))
	include $(SETUP_FILE)
endif

SKIP_PYTHON_EXECUTABLE ?= OFF
HIDE_SYMBOL ?= OFF
DEBUG_SYMBOL ?= ON
UNIRAMP_PROFILE ?= OFF
USE_CLANG_TIDY ?= OFF
CMAKE_BUILD_TYPE ?= Release
UNIRAMP_ROOT ?= $(shell pwd)
CMAKE_INSTALL_PREFIX ?= $(UNIRAMP_ROOT)/build/fakeinstall
CMAKE_LIBRARY_OUTPUT_DIRECTORY ?= $(UNIRAMP_ROOT)/uniramp
CMAKE_ARGS ?=
VERBOSE ?=
RUNENV += PYTHONPATH=$(UNIRAMP_ROOT)

pyextsuffix := $(shell python3-config --extension-suffix)
pyvminor := $(shell python3 -c 'import sys; print("%d%d" % sys.version_info[0:2])')

ifeq ($(CMAKE_BUILD_TYPE), Debug)
	BUILD_PATH ?= build/dbg$(pyvminor)
else
	BUILD_PATH ?= build/dev$(pyvminor)
endif

PYTEST ?= $(shell which py.test-3)
ifeq ($(PYTEST),)
	PYTEST := $(shell which pytest)
endif
ifneq ($(VERBOSE),)
	PYTEST_OPTS ?= -v -s
else
	PYTEST_OPTS ?=
endif

.PHONY: default
default: buildext

.PHONY: clean
clean:
	rm -f $(UNIRAMP_ROOT)/uniramp/_uniramp$(pyextsuffix)
	make -C $(BUILD_PATH) clean

.PHONY: cmakeclean
cmakeclean:
	rm -f $(UNIRAMP_ROOT)/uniramp/_uniramp$(pyextsuffix)
	rm -rf $(BUILD_PATH)

.PHONY: pytest
pytest: $(UNIRAMP_ROOT)/uniramp/_uniramp$(pyextsuffix)
	env $(RUNENV) \
		$(PYTEST) $(PYTEST_OPTS) tests/

.PHONY: flake8
flake8:
	make -C $(BUILD_PATH) VERBOSE=$(VERBOSE) flake8

.PHONY: cmake
cmake: $(BUILD_PATH)/Makefile

.PHONY: buildext
buildext: $(UNIRAMP_ROOT)/uniramp/_uniramp$(pyextsuffix)

.PHONY: install
install: cmake
	make -C $(BUILD_PATH) VERBOSE=$(VERBOSE) install

$(UNIRAMP_ROOT)/uniramp/_uniramp$(pyextsuffix): $(BUILD_PATH)/Makefile
	make -C $(BUILD_PATH) VERBOSE=$(VERBOSE) _uniramp_py
	touch $@

$(BUILD_PATH)/Makefile: CMakeLists.txt Makefile
	mkdir -p $(BUILD_PATH) ; \
	cd $(BUILD_PATH) ; \
	env $(RUNENV) \
		cmake $(UNIRAMP_ROOT) \
		-DCMAKE_INSTALL_PREFIX=$(CMAKE_INSTALL_PREFIX) \
		-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=$(CMAKE_LIBRARY_OUTPUT_DIRECTORY) \
		-DCMAKE_BUILD_TYPE=$(CMAKE_BUILD_TYPE) \
		-DSKIP_PYTHON_EXECUTABLE=$(SKIP_PYTHON_EXECUTABLE) \
		-DHIDE_SYMBOL=$(HIDE_SYMBOL) \
		-DDEBUG_SYMBOL=$(DEBUG_SYMBOL) \
		-DUSE_CLANG_TIDY=$(USE_CLANG_TIDY) \
		-DLINT_AS_ERRORS=ON \
		-DUNIRAMP_PROFILE=$(UNIRAMP_PROFILE) \
		$(CMAKE_ARGS)

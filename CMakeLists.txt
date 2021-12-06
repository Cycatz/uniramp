# Copyright (c) 2021, Cycatz <cycatz@staque.xyz>
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

cmake_minimum_required(VERSION 3.15)

#
# Project details
#

project(
  uniramp
  VERSION 0.1.0
  LANGUAGES CXX
)

#
# Set up cmake module path
#

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake/")


#
# Set up project settings
#

include(cmake/StandardSettings.cmake)    



#
# Set up project utils 
# 

include(cmake/Utils.cmake)


#
# Setup alternative names
#

if(${PROJECT_NAME}_USE_ALT_NAMES)
  string(TOLOWER ${PROJECT_NAME} PROJECT_NAME_LOWERCASE)
  string(TOUPPER ${PROJECT_NAME} PROJECT_NAME_UPPERCASE)
else()
  set(PROJECT_NAME_LOWERCASE ${PROJECT_NAME})
  set(PROJECT_NAME_UPPERCASE ${PROJECT_NAME})
endif()



if(NOT SKIP_PYTHON_EXECUTABLE)
    find_program(PYTHON_EXECUTABLE python3)
    message(STATUS "use PYTHON_EXECUTABLE=${PYTHON_EXECUTABLE}")
endif()

option(USE_CLANG_TIDY "use clang-tidy" OFF)
option(LINT_AS_ERRORS "clang-tidy warnings as errors" OFF)

find_program(
    CLANG_TIDY_EXE
    NAMES "clang-tidy"
    DOC "Path to clang-tidy executable"
)
if(USE_CLANG_TIDY)
    if(CLANG_TIDY_EXE)
        set(DO_CLANG_TIDY "${CLANG_TIDY_EXE}")
        if(LINT_AS_ERRORS)
            set(DO_CLANG_TIDY "${DO_CLANG_TIDY}" "-warnings-as-errors=*")
        endif()
        message(STATUS "use clang-tidy with DO_CLANG_TIDY: ${DO_CLANG_TIDY}")
    else()
        message(FATAL_ERROR "USE_CLANG_TIDY is on but clang-tidy is not found")
    endif()
else()
    message(STATUS "not use clang-tidy")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE BOOL "Export compile commands")

option(HIDE_SYMBOL "hide the symbols of python wrapper" OFF)
message(STATUS "HIDE_SYMBOL: ${HIDE_SYMBOL}")

option(DEBUG_SYMBOL "add debug information" ON)
message(STATUS "DEBUG_SYMBOL: ${DEBUG_SYMBOL}")
if(DEBUG_SYMBOL)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
endif()

#
# Pybind11 
#

option(pybind11_path "pybind11 path")
find_package(pybind11 REQUIRED PATHS ${pybind11_path})
message(STATUS "pybind11_INCLUDE_DIRS: ${pybind11_INCLUDE_DIRS}")
include_directories(${pybind11_INCLUDE_DIRS})


#
# FreeType
# 

find_package(Freetype REQUIRED)
message(STATUS "FREETYPE_INCLUDE_DIRS: ${FREETYPE_INCLUDE_DIRS}")
include_directories(${FREETYPE_INCLUDE_DIRS})

set(UNIRAMP_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/include" CACHE INTERNAL "")

include_directories(${UNIRAMP_INCLUDE_DIR})

set(UNIRAMP_HEADERS
    include/uniramp/uniramp.hpp
    include/uniramp/typeface.hpp
)
string(REPLACE "include/" "${CMAKE_CURRENT_SOURCE_DIR}/include/"
       UNIRAMP_HEADERS "${UNIRAMP_HEADERS}")

set(UNIRAMP_PY_HEADERS
    include/uniramp/python/python.hpp
)
string(REPLACE "include/" "${CMAKE_CURRENT_SOURCE_DIR}/include/"
       UNIRAMP_PY_HEADERS "${UNIRAMP_PY_HEADERS}")

include(GNUInstallDirs)

set(UNIRAMP_SOURCES
    src/uniramp.cpp
    src/typeface.cpp
)
pybind11_add_module(
    _uniramp
    ${UNIRAMP_SOURCES}
    ${UNIRAMP_HEADERS}
    ${UNIRAMP_PY_HEADERS}
)

# Linking against with FreeType libraries      
target_link_libraries(_uniramp PRIVATE ${FREETYPE_LIBRARIES})


if(HIDE_SYMBOL)
    set_target_properties(_uniramp PROPERTIES CXX_VISIBILITY_PRESET "hidden")
else()
    set_target_properties(_uniramp PROPERTIES CXX_VISIBILITY_PRESET "default")
endif()

target_compile_options(
    _uniramp PRIVATE
    -Werror -Wall -Wextra
    -Wno-unused-value # for PYBIND11_EXPAND_SIDE_EFFECTS in pybind11.h
    -Wno-noexcept-type # GCC
)

#
# Set up clang-tidy 
#

if(CLANG_TIDY_EXE AND USE_CLANG_TIDY)
    set_target_properties(
        _uniramp PROPERTIES
        CXX_CLANG_TIDY "${DO_CLANG_TIDY}"
    )
endif()

#
# Format the project using the `clang-format` target (i.e: cmake --build build --target clang-format)
#

add_clang_format_target() 

    
set(UNIRAMP_PY_PATH "${PROJECT_SOURCE_DIR}/uniramp")

execute_process(
    COMMAND python3-config --extension-suffix
    OUTPUT_VARIABLE PYEXTSUFFIX)

add_custom_target(_uniramp_py
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:_uniramp> ${UNIRAMP_PY_PATH}/_uniramp${PYEXTSUFFIX}
    DEPENDS _uniramp)

message(STATUS "CMAKE_INSTALL_INCLUDEDIR: ${CMAKE_INSTALL_INCLUDEDIR}")
install(DIRECTORY ${UNIRAMP_INCLUDE_DIR}/uniramp DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

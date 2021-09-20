cmake_minimum_required(VERSION 3.11)

project(gaussian_test)

message(STATUS "Source directory: ${CMAKE_SOURCE_DIR}")
message(STATUS "Build  directory: ${CMAKE_BINARY_DIR}")
message(STATUS "Configuring ${PROJECT_TITLE} ...")

#define CMAKE_MODULE_PATH to use some of our macros and functions...
#and include some of our functions
list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/Modules)
include(MacroOutOfSourceBuild)
include(FetchContentHelpers)
include(ShowCmakeVariables)

macro_ensure_out_of_source_build("${PROJECT_NAME} requires an out of source build.")

# Required boost support
find_package(Boost REQUIRED)
include_directories(${BOOST_INCLUDE_DIRS})

# Required package gLinear and add its include directory
find_package(gLinear REQUIRED)
include_directories(${GLINEAR_INCLUDE_DIRS})

# Required package gLinear and add its include directory
find_package(prlite REQUIRED)
include_directories(${PRLITE_INCLUDE_DIRS})
#message(${PRLITE_INCLUDE_DIRS})
#message(${PRLITE_LIBRARIES})

# Required package emdw and add its include directory
find_package(emdw REQUIRED)
include_directories(${EMDW_INCLUDE_DIRS})

#****************************************************************
# Add xtl and xtensor to our project (header only projects)
#****************************************************************

#FetchContent_gitdefaults(xtl https://github.com/QuantStack/xtl.git 0.6.5 )
#FetchContent_gitdefaults(xtensor https://github.com/QuantStack/xtensor.git 0.20.8 )
#include_directories(${xtensor_SOURCE_DIR}/include ${xtl_SOURCE_DIR}/include)


#****************************************************************
# Our main project targets
#****************************************************************
add_subdirectory(src)

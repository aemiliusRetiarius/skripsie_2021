# select c++ compiler
set(CMAKE_CXX_COMPILER "g++")
set(CMAKE_CXX_FLAGS "-std=c++17 -O3 ") # -DDEBUG_MODE -DCHK_IDX -DDEBUG_MODE -pedantic

# to enable warnings
add_definitions ("-Wall")

# Include the directory itself as a path to include directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)

#
# Here we group supplementary code not necessary for running
# the the emdw system, mostly image processing stuff. In all
# likelihood we will later move them to other libraries.
#
# The OTHER .cc source files
set(MY_OBJECTS )
#
# The OTHER .hpp header files
set(MY_HEADERS )
#
# The .tcc template source files
set(MY_TEMPLATES )

#
# Create a variable called MY_SOURCES containing all code files:
set(MY_SOURCES ${MY_OBJECTS} ${MY_HEADERS} ${MY_TEMPLATES})
#

include_directories(${GLINEAR_INCLUDE_DIRS} ${EMDW_INCLUDE_DIRS})

# For a large number of source files you can create it in a simpler way
# using file() function:
# file(GLOB MY_SOURCES *.cpp)

# My app
add_executable(gaussian_test gaussian_test.cc)
target_link_libraries(gaussian_test ${GLINEAR_LIBRARIES} ${BOOST_LIBRARIES} ${EMDW_LIBRARIES} ${PRLITE_LIBRARIES})

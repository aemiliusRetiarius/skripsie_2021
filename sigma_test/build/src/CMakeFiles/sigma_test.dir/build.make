# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/emile/devel/skripsie_2021/sigma_test

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/emile/devel/skripsie_2021/sigma_test/build

# Include any dependencies generated for this target.
include src/CMakeFiles/sigma_test.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/sigma_test.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/sigma_test.dir/flags.make

src/CMakeFiles/sigma_test.dir/sigma_test.cc.o: src/CMakeFiles/sigma_test.dir/flags.make
src/CMakeFiles/sigma_test.dir/sigma_test.cc.o: ../src/sigma_test.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/emile/devel/skripsie_2021/sigma_test/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/CMakeFiles/sigma_test.dir/sigma_test.cc.o"
	cd /home/emile/devel/skripsie_2021/sigma_test/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/sigma_test.dir/sigma_test.cc.o -c /home/emile/devel/skripsie_2021/sigma_test/src/sigma_test.cc

src/CMakeFiles/sigma_test.dir/sigma_test.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/sigma_test.dir/sigma_test.cc.i"
	cd /home/emile/devel/skripsie_2021/sigma_test/build/src && g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/emile/devel/skripsie_2021/sigma_test/src/sigma_test.cc > CMakeFiles/sigma_test.dir/sigma_test.cc.i

src/CMakeFiles/sigma_test.dir/sigma_test.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/sigma_test.dir/sigma_test.cc.s"
	cd /home/emile/devel/skripsie_2021/sigma_test/build/src && g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/emile/devel/skripsie_2021/sigma_test/src/sigma_test.cc -o CMakeFiles/sigma_test.dir/sigma_test.cc.s

# Object files for target sigma_test
sigma_test_OBJECTS = \
"CMakeFiles/sigma_test.dir/sigma_test.cc.o"

# External object files for target sigma_test
sigma_test_EXTERNAL_OBJECTS =

src/sigma_test: src/CMakeFiles/sigma_test.dir/sigma_test.cc.o
src/sigma_test: src/CMakeFiles/sigma_test.dir/build.make
src/sigma_test: /home/emile/bin/libgLinear.so
src/sigma_test: /usr/local/lib/libemdw.so
src/sigma_test: /usr/local/lib/libprlite.so
src/sigma_test: src/CMakeFiles/sigma_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/emile/devel/skripsie_2021/sigma_test/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable sigma_test"
	cd /home/emile/devel/skripsie_2021/sigma_test/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/sigma_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/sigma_test.dir/build: src/sigma_test

.PHONY : src/CMakeFiles/sigma_test.dir/build

src/CMakeFiles/sigma_test.dir/clean:
	cd /home/emile/devel/skripsie_2021/sigma_test/build/src && $(CMAKE_COMMAND) -P CMakeFiles/sigma_test.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/sigma_test.dir/clean

src/CMakeFiles/sigma_test.dir/depend:
	cd /home/emile/devel/skripsie_2021/sigma_test/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/emile/devel/skripsie_2021/sigma_test /home/emile/devel/skripsie_2021/sigma_test/src /home/emile/devel/skripsie_2021/sigma_test/build /home/emile/devel/skripsie_2021/sigma_test/build/src /home/emile/devel/skripsie_2021/sigma_test/build/src/CMakeFiles/sigma_test.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/sigma_test.dir/depend


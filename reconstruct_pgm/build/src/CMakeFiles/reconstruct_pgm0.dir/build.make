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
CMAKE_SOURCE_DIR = /home/emile/devel/skripsie_2021/reconstruct_pgm

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/emile/devel/skripsie_2021/reconstruct_pgm/build

# Include any dependencies generated for this target.
include src/CMakeFiles/reconstruct_pgm0.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/reconstruct_pgm0.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/reconstruct_pgm0.dir/flags.make

src/CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.o: src/CMakeFiles/reconstruct_pgm0.dir/flags.make
src/CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.o: ../src/reconstruct_pgm.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/emile/devel/skripsie_2021/reconstruct_pgm/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.o"
	cd /home/emile/devel/skripsie_2021/reconstruct_pgm/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.o -c /home/emile/devel/skripsie_2021/reconstruct_pgm/src/reconstruct_pgm.cc

src/CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.i"
	cd /home/emile/devel/skripsie_2021/reconstruct_pgm/build/src && g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/emile/devel/skripsie_2021/reconstruct_pgm/src/reconstruct_pgm.cc > CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.i

src/CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.s"
	cd /home/emile/devel/skripsie_2021/reconstruct_pgm/build/src && g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/emile/devel/skripsie_2021/reconstruct_pgm/src/reconstruct_pgm.cc -o CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.s

# Object files for target reconstruct_pgm0
reconstruct_pgm0_OBJECTS = \
"CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.o"

# External object files for target reconstruct_pgm0
reconstruct_pgm0_EXTERNAL_OBJECTS =

src/reconstruct_pgm0: src/CMakeFiles/reconstruct_pgm0.dir/reconstruct_pgm.cc.o
src/reconstruct_pgm0: src/CMakeFiles/reconstruct_pgm0.dir/build.make
src/reconstruct_pgm0: /home/emile/bin/libgLinear.so
src/reconstruct_pgm0: /home/emile/devel/emdw/build/src/libemdw.so
src/reconstruct_pgm0: /home/emile/devel/prlite/build/src/libprlite.so
src/reconstruct_pgm0: src/CMakeFiles/reconstruct_pgm0.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/emile/devel/skripsie_2021/reconstruct_pgm/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable reconstruct_pgm0"
	cd /home/emile/devel/skripsie_2021/reconstruct_pgm/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/reconstruct_pgm0.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/reconstruct_pgm0.dir/build: src/reconstruct_pgm0

.PHONY : src/CMakeFiles/reconstruct_pgm0.dir/build

src/CMakeFiles/reconstruct_pgm0.dir/clean:
	cd /home/emile/devel/skripsie_2021/reconstruct_pgm/build/src && $(CMAKE_COMMAND) -P CMakeFiles/reconstruct_pgm0.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/reconstruct_pgm0.dir/clean

src/CMakeFiles/reconstruct_pgm0.dir/depend:
	cd /home/emile/devel/skripsie_2021/reconstruct_pgm/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/emile/devel/skripsie_2021/reconstruct_pgm /home/emile/devel/skripsie_2021/reconstruct_pgm/src /home/emile/devel/skripsie_2021/reconstruct_pgm/build /home/emile/devel/skripsie_2021/reconstruct_pgm/build/src /home/emile/devel/skripsie_2021/reconstruct_pgm/build/src/CMakeFiles/reconstruct_pgm0.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/reconstruct_pgm0.dir/depend


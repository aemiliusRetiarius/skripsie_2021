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
CMAKE_SOURCE_DIR = /home/emile/devel/sigma_test

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/emile/devel/sigma_test/build

# Include any dependencies generated for this target.
include src/CMakeFiles/my_emdw_app.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/my_emdw_app.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/my_emdw_app.dir/flags.make

src/CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.o: src/CMakeFiles/my_emdw_app.dir/flags.make
src/CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.o: ../src/my_emdw_app.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/emile/devel/sigma_test/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.o"
	cd /home/emile/devel/sigma_test/build/src && g++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.o -c /home/emile/devel/sigma_test/src/my_emdw_app.cc

src/CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.i"
	cd /home/emile/devel/sigma_test/build/src && g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/emile/devel/sigma_test/src/my_emdw_app.cc > CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.i

src/CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.s"
	cd /home/emile/devel/sigma_test/build/src && g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/emile/devel/sigma_test/src/my_emdw_app.cc -o CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.s

# Object files for target my_emdw_app
my_emdw_app_OBJECTS = \
"CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.o"

# External object files for target my_emdw_app
my_emdw_app_EXTERNAL_OBJECTS =

src/my_emdw_app: src/CMakeFiles/my_emdw_app.dir/my_emdw_app.cc.o
src/my_emdw_app: src/CMakeFiles/my_emdw_app.dir/build.make
src/my_emdw_app: /home/emile/bin/libgLinear.so
src/my_emdw_app: /home/emile/devel/emdw/build/src/libemdw.so
src/my_emdw_app: /home/emile/devel/prlite/build/src/libprlite.so
src/my_emdw_app: src/CMakeFiles/my_emdw_app.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/emile/devel/sigma_test/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable my_emdw_app"
	cd /home/emile/devel/sigma_test/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/my_emdw_app.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/my_emdw_app.dir/build: src/my_emdw_app

.PHONY : src/CMakeFiles/my_emdw_app.dir/build

src/CMakeFiles/my_emdw_app.dir/clean:
	cd /home/emile/devel/sigma_test/build/src && $(CMAKE_COMMAND) -P CMakeFiles/my_emdw_app.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/my_emdw_app.dir/clean

src/CMakeFiles/my_emdw_app.dir/depend:
	cd /home/emile/devel/sigma_test/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/emile/devel/sigma_test /home/emile/devel/sigma_test/src /home/emile/devel/sigma_test/build /home/emile/devel/sigma_test/build/src /home/emile/devel/sigma_test/build/src/CMakeFiles/my_emdw_app.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/my_emdw_app.dir/depend


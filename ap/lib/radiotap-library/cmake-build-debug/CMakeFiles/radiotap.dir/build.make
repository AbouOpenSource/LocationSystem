# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.15

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
CMAKE_COMMAND = /opt/soft/clion-2019.3.3/bin/cmake/linux/bin/cmake

# The command to remove a file.
RM = /opt/soft/clion-2019.3.3/bin/cmake/linux/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/radiotap.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/radiotap.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/radiotap.dir/flags.make

CMakeFiles/radiotap.dir/radiotap.c.o: CMakeFiles/radiotap.dir/flags.make
CMakeFiles/radiotap.dir/radiotap.c.o: ../radiotap.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/radiotap.dir/radiotap.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/radiotap.dir/radiotap.c.o   -c "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/radiotap.c"

CMakeFiles/radiotap.dir/radiotap.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/radiotap.dir/radiotap.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/radiotap.c" > CMakeFiles/radiotap.dir/radiotap.c.i

CMakeFiles/radiotap.dir/radiotap.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/radiotap.dir/radiotap.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/radiotap.c" -o CMakeFiles/radiotap.dir/radiotap.c.s

# Object files for target radiotap
radiotap_OBJECTS = \
"CMakeFiles/radiotap.dir/radiotap.c.o"

# External object files for target radiotap
radiotap_EXTERNAL_OBJECTS =

libradiotap.so: CMakeFiles/radiotap.dir/radiotap.c.o
libradiotap.so: CMakeFiles/radiotap.dir/build.make
libradiotap.so: CMakeFiles/radiotap.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking C shared library libradiotap.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/radiotap.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/radiotap.dir/build: libradiotap.so

.PHONY : CMakeFiles/radiotap.dir/build

CMakeFiles/radiotap.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/radiotap.dir/cmake_clean.cmake
.PHONY : CMakeFiles/radiotap.dir/clean

CMakeFiles/radiotap.dir/depend:
	cd "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/cmake-build-debug" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library" "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library" "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/cmake-build-debug" "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/cmake-build-debug" "/home/abou/Documents/Cours/M1-IOT-S2/Positioning techniques and systems/apNew/lib/radiotap-library/cmake-build-debug/CMakeFiles/radiotap.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/radiotap.dir/depend

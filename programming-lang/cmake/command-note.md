# Cmake command reference/notes

<!--toc:start-->

- [target_link_libraries(<lib> PUBLIC <dep>)](#targetlinklibrarieslib-public-dep)
- [set_target_properties(<targets> PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})](#settargetpropertiestargets-properties-vsdebuggerworkingdirectory-cmakecurrentsourcedir)
<!--toc:end-->

## target_link_libraries(<lib> PUBLIC <dep>)

Makes any project linking `lib` also link against `dep`

## set_target_properties(<targets> PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

Set the working directory for visual studio debugger.

## add_subdirectory(<path> EXCLUDE_FROM_ALL)

[ref](https://cmake.org/cmake/help/latest/prop_dir/EXCLUDE_FROM_ALL.html#prop_dir:EXCLUDE_FROM_ALL)
Exclude targets in the subdirectory from the `ALL` target in the parent directory.

- the target in the subdirectory will be built if it's a dependency of another
  target in the parent directory
- user can built excluded target explicitly
- install rules will be ignored by the parent

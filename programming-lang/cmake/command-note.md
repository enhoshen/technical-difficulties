<!--toc:start-->

- [target_link_libraries(<lib> PUBLIC <dep>)](#targetlinklibrarieslib-public-dep)
- [set_target_properties(<targets> PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})](#settargetpropertiestargets-properties-vsdebuggerworkingdirectory-cmakecurrentsourcedir)
<!--toc:end-->

## target_link_libraries(<lib> PUBLIC <dep>)

Makes any project linking `lib` also link against `dep`

## set_target_properties(<targets> PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

![`TODO`]
Set the working directory for visual studio debugger.

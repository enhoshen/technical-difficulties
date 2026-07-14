# CMake Variable Reference Notes

## Base Directories

- `CMAKE_SOURCE_DIR`: The source directory of the top-most `CMakeLists.txt` in the build tree (the root of the project).
- `PROJECT_SOURCE_DIR`: The source directory of the most recent `project()` command in the current directory scope or any parent scopes.
- `CMAKE_CURRENT_SOURCE_DIR`: The directory of the `CMakeLists.txt` currently being processed by CMake.
- `CMAKE_CURRENT_LIST_DIR`: The directory of the listfile (`CMakeLists.txt` or a `.cmake` script included via `include()`) currently being processed.

### Example Directory Structure

```text
my_workspace/                           # (A) Top-most project root (CMAKE_SOURCE_DIR)
├── CMakeLists.txt                      # Contains: project(MyMainApp)
└── libs/
    └── my_lib/                         # (B) Sub-project root
        ├── CMakeLists.txt              # Contains: project(MyLibrary) & include(cmake/helper.cmake)
        ├── my_lib_sub/                    # (C) Nested subdirectory (no project() call)
        │   └── CMakeLists.txt          # Contains: add_library(my_lib_sub ...)
        └── cmake/
            └── helper.cmake            # (D) Included helper script
```

### Variable Resolution Table

When CMake processes different files in this project, the four variables resolve as follows:

| Processing Location                                   | `CMAKE_SOURCE_DIR` | `PROJECT_SOURCE_DIR`            | `CMAKE_CURRENT_SOURCE_DIR`             | `CMAKE_CURRENT_LIST_DIR`               |
| :---------------------------------------------------- | :----------------- | :------------------------------ | :------------------------------------- | :------------------------------------- |
| `/my_workspace/CMakeLists.txt`                        | `/my_workspace`    | `/my_workspace`                 | `/my_workspace`                        | `/my_workspace`                        |
| `/my_workspace/libs/my_lib/CMakeLists.txt`            | `/my_workspace`    | `/my_workspace/libs/my_lib`     | `/my_workspace/libs/my_lib`            | `/my_workspace/libs/my_lib`            |
| `/my_workspace/libs/my_lib/my_lib_sub/CMakeLists.txt` | `/my_workspace`    | \*\*`/my_workspace/libs/my_lib` | `/my_workspace/libs/my_lib/my_lib_sub` | `/my_workspace/libs/my_lib/my_lib_sub` |
| `/my_workspace/libs/my_lib/cmake/helper.cmake`        | `/my_workspace`    | `/my_workspace/libs/my_lib`     | \*\*`/my_workspace/libs/my_lib`        | \*\*`/my_workspace/libs/my_lib/cmake`  |

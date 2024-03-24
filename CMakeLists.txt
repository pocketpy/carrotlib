cmake_minimum_required(VERSION 3.17)

project(Game)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/3rd)

# project
include_directories(${CMAKE_CURRENT_LIST_DIR}/include)
aux_source_directory(${CMAKE_CURRENT_LIST_DIR}/src PROJECT_SRC)

if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc /utf-8 /O2")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fexceptions -frtti -O2")
endif()

if (ANDROID)
    set(ANDROID_STL c++_shared)
    include_directories(${ANDROID_NDK}/sources/android/native_app_glue)

    add_library(
        ${PROJECT_NAME}Android
        SHARED
        ${PROJECT_SRC}
        platforms/android.cpp
        ${ANDROID_NDK}/sources/android/native_app_glue/android_native_app_glue.c
    )

    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -u ANativeActivity_onCreate")
  
    target_link_libraries(${PROJECT_NAME}Android PRIVATE
        android EGL GLESv3 log 3rdparty
    )
elseif(CMAKE_SYSTEM_NAME STREQUAL "iOS")
    message("Building for iOS static library!!")

    add_library(${PROJECT_NAME} STATIC
        ${PROJECT_SRC}
        platforms/ios.cpp
        ${CMAKE_CURRENT_LIST_DIR}/src/tmp/_hardcoded_assets.cpp
        ${CMAKE_CURRENT_LIST_DIR}/src/tmp/_hardcoded_sources.cpp
    )

    target_compile_definitions(${PROJECT_NAME} PRIVATE PLATFORM_IOS=1)
    target_link_libraries(${PROJECT_NAME} 3rdparty)
elseif(EMSCRIPTEN)
    add_executable(
        ${PROJECT_NAME}
        ${PROJECT_SRC}
        platforms/emscripten.cpp
        ${CMAKE_CURRENT_LIST_DIR}/src/tmp/_hardcoded_assets.cpp
        ${CMAKE_CURRENT_LIST_DIR}/src/tmp/_hardcoded_sources.cpp
    )

    target_link_libraries(${PROJECT_NAME} 3rdparty)
    # -fexceptions is required by pocketpy
    set(EMCC_LINKER_FLAGS "-s USE_GLFW=3 -fexceptions --allow-memory-growth -s TOTAL_MEMORY=512MB -sASYNCIFY -sASSERTIONS")
    set(CMAKE_EXECUTABLE_SUFFIX ".html")
    set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS ${EMCC_LINKER_FLAGS})
else()
    add_executable(${PROJECT_NAME} ${PROJECT_SRC} platforms/standalone.cpp)
    target_link_libraries(${PROJECT_NAME} 3rdparty)

    # Checks if OSX and links appropriate frameworks (Only required on MacOS)
    if (APPLE)
        target_link_libraries(${PROJECT_NAME} "-framework IOKit")
        target_link_libraries(${PROJECT_NAME} "-framework Cocoa")
        target_link_libraries(${PROJECT_NAME} "-framework OpenGL")
    elseif(WIN32)
        if(CMAKE_BUILD_TYPE STREQUAL "Release")
            set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS "/SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")
        endif()
    endif()
endif()
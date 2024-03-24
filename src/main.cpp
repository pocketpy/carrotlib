#include "appw.hpp"
#include "raylib.h"

using namespace pkpy;
using namespace ct;

namespace pkpy{
    void add_module_box2d(VM* vm);
    void add_module_raylib(VM* vm);
    void add_module_imgui(VM* vm);
}

static VM* vm;

int error_screen(Str msg){
    msg = _S(
        "Oops! The game encountered an error.\n",
        get_system_info(), '\n',
        pool64_info(), " & ", pool128_info(), '\n',
        '\n',
    msg);
    int width = (GetScreenWidth() + GetRenderWidth()) / 2;
    int font_size = width / 500 * 10;
    int line_spacing = font_size * 1.2;
    while(!WindowShouldClose()){
        // raylib default font size is 10, use 10/20/30 to be pixel perfect
        BeginDrawing();
        ClearBackground({255, 130, 45, 255});   // 🥕 orange
        SetTextLineSpacing(line_spacing);
        DrawText(msg.c_str(), font_size, font_size, font_size, WHITE);
        EndDrawing();
    }
    return 1;
}

int main(int argc, char** argv){
    vm = new VM();
    vm->_import_handler = &platform_load_asset;
    vm->_stdout = [](const char* s, int n){ platform_log_info(Str(s, n)); };
    vm->_stderr = [](const char* s, int n){ platform_log_error(Str(s, n)); };

    SetLoadFileDataCallback([](const char* filename, int* dataSize) -> unsigned char*{
        int out_size;
        unsigned char* out = platform_load_asset(filename, strlen(filename), &out_size);
        if(out == nullptr){
            vm->IOError(_S("failed to load ", filename, "\n"));
            return nullptr;
        }
        *dataSize = out_size;
        return out;
    });

    SetLoadFileTextCallback([](const char* filename) -> char*{
        int out_size;
        unsigned char* out = platform_load_asset(filename, strlen(filename), &out_size);
        if(out == nullptr){
            vm->IOError(_S("failed to load ", filename, "\n"));
            return nullptr;
        }
        return (char*)out;
    });

    add_module_box2d(vm);
    add_module_raylib(vm);
    add_module_imgui(vm);
    add_module__ct(vm);

#if _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif

// desktop platforms
#if PK_IS_DESKTOP_PLATFORM == 1
    if(argc != 2){
        std::cerr << "usage: " << argv[0] << " [project_dir]" << std::endl;
        exit(1);
    }
    if(!std::filesystem::exists(argv[1])){
        std::cerr << "error: " << argv[1] << " does not exist" << std::endl;
        exit(1);
    }
    std::filesystem::current_path(argv[1]);
    platform_log_info(std::filesystem::current_path().string() + "\n");
#endif

    // android, ios, emscripten can use hardcoded asset backend

    std::string entry_file = "main.py";
    int out_size;
    unsigned char* out = platform_load_asset(entry_file.data(), entry_file.size(), &out_size);
    if(out == nullptr){
        platform_log_error(_S("failed to load ", entry_file, "\n"));
        exit(100);
    }
    Str entry_file_string((char*)out, out_size);
    free(out);
    
    try{
        CodeObject_ co = vm->compile(entry_file_string, entry_file, EXEC_MODE);
        PyObject* res = vm->_exec(co, vm->_main);
        if(res == nullptr) exit(1);
    }catch(Exception& py_exc){
        if(py_exc.type == "RestartException"){
            delete vm;
            main(argc, argv);
            return 0;
        }else{
            platform_log_error(py_exc.summary() + "\n");
            return error_screen(py_exc.summary());
        }
    }catch(std::exception& e){
        platform_log_error(_S("std::exception: ", e.what(), "\n"));
        return error_screen(_S("std::exception: ", e.what()));
    }

    delete vm;
    return 0;
}

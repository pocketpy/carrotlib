#include "appw.hpp"
#include "raylib.h"

using namespace pkpy;
using namespace ct;

namespace pkpy{
    void add_module_box2d(VM* vm);
    void add_module_raylib(VM* vm);
    void add_module_imgui(VM* vm);
}

// the global VM instance
static VM* vm;

// if `error_screen_msg` was set, ios_update() will use error_screen()'s logic
static std::string error_screen_msg;

// main()'s arguments
static int main_argc;
static char** main_argv;

// cached objects
struct _Cached{
    PyObject* game = nullptr;
    PyObject* on_ready = nullptr;
    PyObject* on_update = nullptr;
    PyObject* on_destroy = nullptr;
}cached;

static bool is_initialized(){
    return cached.game != nullptr;
}

static void fatal_error(Str msg){
    platform_log_error(msg + "\n");
    if(!is_initialized()) exit(1);
    error_screen_msg = _S(
        "Oops! The game encountered an error.\n",
        get_system_info(), '\n',
        pool64_info(), " & ", pool128_info(), '\n',
        '\n', msg
    ).str();
}

#define CATCH_EXCEPTION()               \
    catch(Exception& py_exc){           \
        fatal_error(py_exc.summary());  \
    }catch(std::exception& e){          \
        fatal_error(_S("std::exception: ", e.what()));  \
    }

extern "C"{
    void ios_ready();
    void ios_update();
    void ios_destroy();
}

void ios_ready(){
    vm = new VM();
    vm->_import_handler = &platform_load_asset;
    vm->_stdout = [](const char* s, int n){ platform_log_info(Str(s, n)); };
    vm->_stderr = [](const char* s, int n){ platform_log_error(Str(s, n)); };
    vm->heap._gc_marker_ex = [](VM* vm){
        PK_OBJ_MARK(cached.game);
        PK_OBJ_MARK(cached.on_ready);
        PK_OBJ_MARK(cached.on_update);
        PK_OBJ_MARK(cached.on_destroy);
    };

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
    if(main_argc != 2){
        std::cerr << "usage: " << main_argv[0] << " [project_dir]" << std::endl;
        exit(1);
    }
    if(!std::filesystem::exists(main_argv[1])){
        std::cerr << "error: " << main_argv[1] << " does not exist" << std::endl;
        exit(1);
    }
    std::filesystem::current_path(main_argv[1]);
    platform_log_info(std::filesystem::current_path().string() + "\n");
#endif

    std::string entry_file = "main.py";
    int out_size;
    unsigned char* out = platform_load_asset(entry_file.data(), entry_file.size(), &out_size);
    if(out == nullptr) fatal_error(_S("failed to load ", entry_file));
    
    Str entry_file_string((char*)out, out_size);
    free(out);

    try{
        CodeObject_ co = vm->compile(entry_file_string, entry_file, EXEC_MODE);
        if(!vm->_exec(co, vm->_main)){
            fatal_error("`vm->_exec(co, vm->_main)` returns nullptr");
        }
        // find a class derived from cl.Game
        Type cl_game_t = PK_OBJ_GET(Type, vm->_modules["carrotlib"]->attr("Game"));
        for(auto [_, obj]: vm->_main->attr().items()){
            // find a class derived from cl.Game
            if(is_type(obj, VM::tp_type)){
                if(vm->issubclass(PK_OBJ_GET(Type, obj), cl_game_t)){
                    // creata a game instance
                    cached.game = vm->call(obj);
                    cached.on_ready = vm->getattr(cached.game, "on_ready");
                    cached.on_update = vm->getattr(cached.game, "on_update");
                    cached.on_destroy = vm->getattr(cached.game, "on_destroy");
                    break;
                }
            }
        }
        if(!cached.game) fatal_error("failed to find a class derived from `cl.Game`");
        vm->call(cached.on_ready);
    } CATCH_EXCEPTION()
}

void ios_update(){
    if(!error_screen_msg.empty()){
        // error_screen_update
        int width = (GetScreenWidth() + GetRenderWidth()) / 2;
        int font_size = width / 500 * 10;
        int line_spacing = font_size * 1.2;
        // raylib default font size is 10, use 10/20/30 to be pixel perfect
        BeginDrawing();
        ClearBackground({255, 130, 45, 255});   // 🥕 orange
        SetTextLineSpacing(line_spacing);
        DrawText(error_screen_msg.c_str(), font_size, font_size, font_size, WHITE);
        EndDrawing();
        return;
    }
    try{
        vm->call(cached.on_update);
    } CATCH_EXCEPTION()
}

void ios_destroy(){
    if(!is_initialized()) return;
    try{
        vm->call(cached.on_destroy);
    } CATCH_EXCEPTION()
    delete vm;
}

#ifndef PLATFORM_IOS
int main(int argc, char** argv){
    main_argc = argc;
    main_argv = argv;
    ios_ready();
    while(!WindowShouldClose()) ios_update();
    ios_destroy();
    return 0;
}
#endif
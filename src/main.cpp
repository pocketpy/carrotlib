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
    PyVar game = nullptr;
    PyVar on_ready = nullptr;
    PyVar on_update = nullptr;
    PyVar on_destroy = nullptr;
    bool hot_reload_needed = false;
}cached;

static void fatal_error(Str msg){
    platform_log_error(msg + "\n");
    if(cached.game == nullptr) exit(1);
    error_screen_msg = _S(
        "Oops! The game encountered an error.\n",
        platform_system_info(), '\n',
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
    PK_EXPORT void ios_ready();
    PK_EXPORT void ios_update();
    PK_EXPORT void ios_destroy();
}

void ios_ready(){
    platform_init();

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
        unsigned char* out = platform_load_asset(filename, &out_size);
        if(out == nullptr){
            vm->IOError(_S("failed to load ", filename, "\n"));
            return nullptr;
        }
        *dataSize = out_size;
        return out;
    });

    SetLoadFileTextCallback([](const char* filename) -> char*{
        int out_size;
        unsigned char* out = platform_load_asset(filename, &out_size);
        if(out == nullptr){
            vm->IOError(_S("failed to load ", filename, "\n"));
            return nullptr;
        }
        return (char*)out;
    });

    add_module_box2d(vm);
    add_module_raylib(vm);
    add_module_imgui(vm);

#ifndef __EMSCRIPTEN__
    add_module_naett(vm);
#endif

    vm->bind(add_module__ct(vm), "_request_hot_reload()",
        [](VM* vm, ArgsView args){
            cached.hot_reload_needed = true;
            return vm->None;
        });

// desktop platforms
#if PK_IS_DESKTOP_PLATFORM == 1
    if(main_argc > 1){
        if(main_argc != 3){
            platform_log_error("Usage: Game.exe [project_dir] [template_dir]\n");
            exit(1);
        }
        for(int i=1; i<main_argc; i++){
            if(!std::filesystem::exists(main_argv[i])){
                platform_log_error(_S("Error: ", main_argv[i], " does not exist\n"));
                exit(1);
            }
        }
        set_template_path(main_argv[2]);
        std::filesystem::current_path(main_argv[1]);
    }
    platform_log_info(std::filesystem::current_path().string() + "\n");
#endif

    std::string entry_file = "main.py";
    int out_size;
    unsigned char* out = platform_load_asset(entry_file.c_str(), &out_size);
    if(out == nullptr) fatal_error(_S("Error: failed to load ", entry_file));

    Str entry_file_string((char*)out, out_size);
    free(out);

    try{
        CodeObject_ co = vm->compile(entry_file_string, entry_file, EXEC_MODE);
        if(!vm->_exec(co, vm->_main)){
            fatal_error("Error: `vm->_exec(co, vm->_main)` returns nullptr");
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
        if(!cached.game) fatal_error("Error: failed to find a class derived from `cl.Game`");
        vm->call(cached.on_ready);
    } CATCH_EXCEPTION()

    setup_imgui_font();
}

void ios_update(){
    if(!error_screen_msg.empty()){
        // error_screen_update
        static Font font = LoadFontEx(SourceCodePro_Medium, 64, NULL, 0);
        int width = (GetScreenWidth() + GetRenderWidth()) / 2;
        float font_size = (int)(width / 54.0f);
        int line_spacing = font_size;
        BeginDrawing();
        ClearBackground({255, 130, 45, 255});   // 🥕 orange
        SetTextLineSpacing(line_spacing);
        DrawTextEx(font, error_screen_msg.c_str(), {font_size, font_size}, font_size, 0, WHITE);
        EndDrawing();
        return;
    }
    try{
        vm->call(cached.on_update);
    } CATCH_EXCEPTION()
}

void ios_destroy(){
    if(cached.game == nullptr) return;
    try{
        vm->call(cached.on_destroy);
    } CATCH_EXCEPTION()
    delete vm;
}

// not iOS
#if PK_SYS_PLATFORM != 2
int main(int argc, char** argv){
    if(argc > 1){
        std::string_view argv_1(argv[1]);
        if(argv_1.find(".py") == argv_1.size()-3){
            platform_init();
            vm = new VM();
            vm->set_main_argv(argc, argv);
            int size;
            const char* data = (const char*)_default_import_handler(argv[1], &size);
            if(data == nullptr){
                vm->stderr_write(_S("Error: failed to load ", argv_1, '\n'));
                return 1;
            }
            PyVar res = vm->exec(std::string_view(data, size), argv_1, EXEC_MODE);
            delete vm;
            return res != nullptr ? 0 : 1;
        }
    }

    main_argc = argc;
    main_argv = argv;

    ios_ready();
    if(cached.game == nullptr) return 1;
    while(!WindowShouldClose()){
        if(cached.hot_reload_needed){
            // reset everything
            delete vm;
            vm = nullptr;
            memset(&cached, 0, sizeof(cached));
            error_screen_msg.clear();
            return main(argc, argv);
        }
        ios_update();
    }
    ios_destroy();
    return 0;
}
#endif
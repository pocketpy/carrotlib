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

int main(int argc, char** argv){
    vm = new VM();
    vm->_import_handler = &platform_load_asset;
    vm->_stdout = [](const char* s, int n){ platform_log_info(Str(s, n)); };
    vm->_stderr = [](const char* s, int n){ platform_log_error(Str(s, n)); };

    SetLoadFileDataCallback([](const char* filename, int* dataSize) -> unsigned char*{
        int out_size;
        unsigned char* out = platform_load_asset(filename, strlen(filename), &out_size);
        if(out == nullptr){
            vm->IOError(fmt("failed to load ", filename, "\n"));
            return nullptr;
        }
        *dataSize = out_size;
        return out;
    });

    SetLoadFileTextCallback([](const char* filename) -> char*{
        int out_size;
        unsigned char* out = platform_load_asset(filename, strlen(filename), &out_size);
        if(out == nullptr){
            vm->IOError(fmt("failed to load ", filename, "\n"));
            return nullptr;
        }
        return (char*)out;
    });

    add_module_box2d(vm);
    add_module_raylib(vm);
    add_module_imgui(vm);
    add_module__ct(vm);

#if _WIN32
    set_console_cp_utf8_on_win32();
    // vm->bind(vm->_modules["raylib"], "InitWindow(width: int, height: int, title: str)", [](VM* vm, ArgsView args){
    //     int width = CAST(int, args[0]);
    //     int height = CAST(int, args[1]);
    //     const char* title = CAST(CString, args[2]);
    //     InitWindow(width, height, title);
    //     set_input_method_on_win32();
    //     return vm->None;
    // });
#endif

#if !ANDROID
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

    std::string entry_file = "main.py";
    int out_size;
    unsigned char* out = platform_load_asset(entry_file.data(), entry_file.size(), &out_size);
    if(out == nullptr){
        platform_log_error(fmt("failed to load ", entry_file, "\n"));
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
            return 1;
        }
    }catch(std::exception& e){
        platform_log_error(fmt("std::runtime_error: ", e.what(), "\n"));
        return 1;
    }

    delete vm;
    return 0;
}

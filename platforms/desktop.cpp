#include "appw.hpp"

#if _WIN32
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
#endif

using namespace pkpy;

namespace ct{
    void platform_init(){
#if _WIN32
        SetConsoleOutputCP(CP_UTF8);
        SetConsoleCP(CP_UTF8);
#endif
        setvbuf(stdout, nullptr, _IONBF, 0);
        setvbuf(stderr, nullptr, _IONBF, 0);
    }

    void platform_log_info(const Str& text){
        std::cout << text;
    }

    void platform_log_error(const Str& text){
        std::cerr << text;
    }

    unsigned char* platform_load_asset(const char* name_p, int name_size, int* out_size){
        unsigned char* res = _default_import_handler(name_p, name_size, out_size);
        if(res != NULL) return res;
        const char* template_path = get_template_path();
        if(template_path == NULL) return NULL;
        std::filesystem::path path(template_path);
        path /= std::string(name_p, name_size);
        if(!std::filesystem::exists(path)) return NULL;
        // fopen
        FILE* f = fopen(path.string().c_str(), "rb");
        if(f == NULL) return NULL;
        // get file size
        fseek(f, 0, SEEK_END); *out_size = ftell(f); fseek(f, 0, SEEK_SET);
        // read file
        unsigned char* out = new unsigned char[*out_size];
        fread(out, 1, *out_size, f);
        fclose(f);
        return out;
    }

    std::vector<std::string> platform_list_assets(std::string_view root){
        std::vector<std::string> result;
        std::filesystem::path path(root);
        if(!std::filesystem::exists(path)){
            const char* template_path = get_template_path();
            if(template_path == NULL) return {};
            path = std::filesystem::path(template_path) / root;
        }
        if(!std::filesystem::exists(path)) return {};
        for(auto& p: std::filesystem::directory_iterator(path)){
            result.push_back(p.path().string());
        }
        return result;
    }

    Str get_system_info(){
        return _S("sys.platform: ", kPlatformStrings[PK_SYS_PLATFORM]);
    }
}   // namespace ct

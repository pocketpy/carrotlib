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

        naettInit(NULL);
    }

    void platform_log_info(const Str& text){
        std::cout << text;
    }

    void platform_log_error(const Str& text){
        std::cerr << text;
    }

    void platform_desktop_screen_size(int& width, int& height){
#if _WIN32
        RECT desktop;
        const HWND hDesktop = GetDesktopWindow();
        GetWindowRect(hDesktop, &desktop);
        width = desktop.right - desktop.left;
        height = desktop.bottom - desktop.top;
        double scale = GetDpiForWindow(hDesktop) / 96.0;
        width = (int)(width * scale);
        height = (int)(height * scale);
#else
        width = 0;
        height = 0;
#endif
    }

    unsigned char* platform_load_asset(const char* name, int* out_size){
        unsigned char* res = _default_import_handler(name, out_size);
        if(res != NULL) return res;
        const char* template_path = get_template_path();
        if(template_path == NULL) return NULL;
        std::filesystem::path path(template_path);
        path /= std::string(name);
        std::string path_string = path.string();
        return _default_import_handler(path_string.c_str(), out_size);
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

    Str platform_system_info(){
        return _S("sys.platform: ", kPlatformStrings[PK_SYS_PLATFORM]);
    }

    void platform_vibrate(i64 milliseconds, int amplitude){
        // unsupported
    }

    Str platform_caches_directory(){
        std::filesystem::path path = std::filesystem::current_path();
        path /= ".caches";
        if(!std::filesystem::exists(path)){
            std::filesystem::create_directory(path);
        }
        return path.string();
    }

    Str platform_documents_directory(){
        std::filesystem::path path = std::filesystem::current_path();
        path /= ".documents";
        if(!std::filesystem::exists(path)){
            std::filesystem::create_directory(path);
        }
        return path.string();
    }
}   // namespace ct

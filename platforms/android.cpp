#include "appw.hpp"

using namespace pkpy;

#include <android/log.h>

using namespace pkpy;

AAssetManager* get_android_asset_manager(){
    return GetAndroidApp()->activity->assetManager;
}

namespace ct{
    void platform_log_info(const Str& text){
        __android_log_print(ANDROID_LOG_INFO, "Engine", "%s", text.c_str());
    }

    void platform_log_error(const Str& text){
        __android_log_print(ANDROID_LOG_ERROR, "Engine", "%s", text.c_str());
    }

    unsigned char* platform_load_asset(const char* name_p, int name_size, int* out_size){
        std::string name(name_p, name_size);
        AAsset* asset = AAssetManager_open(get_android_asset_manager(), name.c_str(), AASSET_MODE_BUFFER);
        if(!asset) return nullptr;
        int size = AAsset_getLength(asset);
        char* buffer = new char[size];
        AAsset_read(asset, buffer, size);
        AAsset_close(asset);
        *out_size = size;
        return (unsigned char*)buffer;
    }

    std::optional<std::vector<Str>> platform_list_assets(const Str& root){
        std::string s_root = root.str();
        if(s_root == ".") s_root = "";
        if(s_root.size()>2 && s_root[0]=='.' && s_root[1]=='/') s_root = s_root.substr(2);
        AAssetDir* dir = AAssetManager_openDir(get_android_asset_manager(), s_root.c_str());
        if(!dir) return std::nullopt;
        std::vector<Str> list;
        const char* name = nullptr;
        while((name = AAssetDir_getNextFileName(dir)) != nullptr){
            list.emplace_back(name);
        }
        AAssetDir_close(dir);
        return list;
    }
}   // namespace ct
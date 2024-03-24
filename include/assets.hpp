#pragma once

#include <map>
#include <string>
#include <string_view>

#include "pocketpy.h"

inline std::map<
    std::string_view,
    std::pair<const unsigned char*, int>,
    std::less<>
> HardcodedAssets;

extern void init_hardcoded_assets(decltype(HardcodedAssets)& assets);

inline unsigned char* _platform_load_asset(const char* name_p, int name_size, int* out_size){
    auto it = HardcodedAssets.find(std::string_view(name_p, name_size));
    if(it == HardcodedAssets.end()) return nullptr;
    *out_size = it->second.second;
    unsigned char* out = new unsigned char[*out_size];
    memcpy(out, it->second.first, *out_size);
    return out;
}

inline std::vector<std::string> _platform_list_assets(std::string_view root){
    std::vector<std::string> result;
    for(auto& kv: HardcodedAssets){
        if(kv.first.substr(0, root.size()) == root){
            result.push_back(std::string(kv.first));
        }
    }
    return result;
}

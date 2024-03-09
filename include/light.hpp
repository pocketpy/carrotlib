#include <algorithm>
#include <stdexcept>

#include "raylib.h"

namespace aseprite{
    typedef void (*AlgoPixel)(int x, int y, void *data);
    typedef void (*AlgoHLine)(int x1, int y, int x2, void *data);

    void algo_ellipse(int x1, int y1, int x2, int y2, int hPixels, int vPixels, void *data, AlgoPixel proc);
    void algo_ellipsefill(int x1, int y1, int x2, int y2, int hPixels, int vPixels, void *data, AlgoHLine proc);
}

namespace ct{
    struct HdrColor{
        float r, g, b, a;
        HdrColor(float r, float g, float b, float a) : r(r), g(g), b(b), a(std::clamp(a, 0.0f, 1.0f)) {}
        HdrColor(Color color, double intensity) :
            r(color.r / 255.0 * intensity),
            g(color.g / 255.0 * intensity),
            b(color.b / 255.0 * intensity),
            a(color.a) {}
        
        static HdrColor additive(HdrColor src, HdrColor dst){
            // https://github.com/aseprite/aseprite/blob/main/src/doc/blend_funcs.cpp#L497
            return HdrColor(src.r + dst.r, src.g + dst.g, src.b + dst.b, src.a);
        }
    };

    void bake_global_light(Image* img, Color color, double intensity);
    void bake_point_light(Image* img, Color color, double intensity, int x, int y, int r, Image* cookie);
    void bake_particle_light(Image* img, Color color, double intensity, int x, int y, int r);
}
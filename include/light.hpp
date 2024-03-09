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
    struct ColorNoAlpha{
        unsigned char r;
        unsigned char g;
        unsigned char b;

        ColorNoAlpha with_intensity(double intensity){
            return {
                (unsigned char)std::clamp((int)(r * intensity), 0, 255),
                (unsigned char)std::clamp((int)(g * intensity), 0, 255),
                (unsigned char)std::clamp((int)(b * intensity), 0, 255)
            };
        }

        ColorNoAlpha(unsigned char r, unsigned char g, unsigned char b) : r(r), g(g), b(b) {}
        ColorNoAlpha(Color color): r(color.r), g(color.g), b(color.b) {}
        operator Color() const { return {r, g, b, 255}; }
    };

    void bake_global_light(Image* img, ColorNoAlpha color, double intensity);
    void bake_point_light(Image* img, ColorNoAlpha color, double intensity, int x, int y, int r, Image* cookie);
}
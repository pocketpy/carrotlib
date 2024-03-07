#include <algorithm>
#include <tuple>
#include <stdexcept>

#include "raylib.h"

namespace aseprite{
    typedef void (*AlgoPixel)(int x, int y, void *data);
    typedef void (*AlgoHLine)(int x1, int y, int x2, void *data);

    void algo_ellipse(int x1, int y1, int x2, int y2, int hPixels, int vPixels, void *data, AlgoPixel proc);
    void algo_ellipsefill(int x1, int y1, int x2, int y2, int hPixels, int vPixels, void *data, AlgoHLine proc);
}

namespace ct{
    void bake_global_light(Image* img, Color color, double intensity);
    void bake_point_light(Image* img, Color color, double intensity, int x, int y, int r);
}
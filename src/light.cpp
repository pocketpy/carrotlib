#include "light.hpp"

namespace aseprite{

static int adjust_ellipse_args(int& x0, int& y0, int& x1, int& y1,
                               int& hPixels, int& vPixels)
{
  // hPixels : straight horizontal pixels added to mid region of the ellipse.
  hPixels = std::max(hPixels, 0);
  // vPixels : straight vertical pixels added to mid region of the ellipse.
  vPixels = std::max(vPixels, 0);

  // Conditioning swapped points
  if (x0 > x1)
    std::swap(x0, x1);
  if (y0 > y1)
    std::swap(y0, y1);
  int w = x1 - x0 + 1;
  int h = y1 - y0 + 1;

  // hDiameter is the horizontal diameter of a circunference
  // without the addition of straight pixels.
  int hDiameter = w - hPixels;
  // vDiameter is the vertical diameter of a circunference
  // without the addition of straight pixels.
  int vDiameter = h - vPixels;

  // Manual adjustment
  if (w == 8 || w == 12 || w == 22)
    hPixels++;
  if (h == 8 || h == 12 || h == 22)
    vPixels++;

  hPixels = (hDiameter > 5 ? hPixels : 0);
  vPixels = (vDiameter > 5 ? vPixels : 0);

  if ((hDiameter % 2 == 0) && (hDiameter > 5))
    hPixels--;
  if ((vDiameter % 2 == 0) && (vDiameter > 5))
    vPixels--;

  x1 -= hPixels;
  y1 -= vPixels;

  return h;
}

// Ellipse code based on Alois Zingl work released under the MIT
// license http://members.chello.at/easyfilter/bresenham.html
//
// Adapted for Aseprite by David Capello

void algo_ellipse(int x0, int y0, int x1, int y1,
                  int hPixels, int vPixels,
                  void* data, AlgoPixel proc)
{
  int h = adjust_ellipse_args(x0, y0, x1, y1, hPixels, vPixels);

  long a = abs(x1-x0);
  long b = abs(y1-y0);                // diameter
  long b1 = b&1;
  double dx = 4*(1.0-a)*b*b;          // error increment
  double dy = 4*(b1+1)*a*a;           // error increment
  double err = dx + dy + b1*a*a;      // error of 1.step
  double e2;

  y0 += (b+1)/2;
  y1 = y0-b1;           // starting pixel
  a = 8*a*a;
  b1 = 8*b*b;

  int initialY0 = y0;
  int initialY1 = y1;
  int initialX0 = x0;
  int initialX1 = x1 + hPixels;
  do {
    proc(x1 + hPixels, y0 + vPixels, data);                //   I. Quadrant
    proc(x0, y0 + vPixels, data);                          //  II. Quadrant
    proc(x0, y1, data);                                    // III. Quadrant
    proc(x1 + hPixels, y1, data);                          //  IV. Quadrant

    e2 = 2*err;
    if (e2 <= dy) { y0++; y1--; err += dy += a; }                 // y step
    if (e2 >= dx || 2*err > dy) { x0++; x1--; err += dx += b1; }  // x step
  } while (x0 <= x1);

  while (y0 + vPixels - y1 + 1 <= h) {          // too early stop of flat ellipses a=1
    proc(x0 - 1, y0 + vPixels, data);          // -> finish tip of ellipse
    proc(x1 + 1 + hPixels, y0++ + vPixels, data);
    proc(x0 - 1, y1, data);
    proc(x1 + 1 + hPixels, y1--, data);
  }

  // Extra horizontal straight pixels
  if (hPixels > 0) {
    for (int i = x0; i < x1 + hPixels + 1; i++) {
      proc(i, y1 + 1, data);
      proc(i, y0 + vPixels - 1, data);
    }
  }
  // Extra vertical straight pixels
  if (vPixels > 0) {
    for (int i = initialY1 + 1; i < initialY0 + vPixels; i++) {
      proc(initialX0, i, data);
      proc(initialX1, i, data);
    }
  }
}

void algo_ellipsefill(int x0, int y0, int x1, int y1,
                      int hPixels, int vPixels,
                      void* data, AlgoHLine proc)
{
  int h = adjust_ellipse_args(x0, y0, x1, y1, hPixels, vPixels);

  long a = abs(x1-x0), b = abs(y1-y0), b1 = b&1;          // diameter
  double dx = 4*(1.0-a)*b*b, dy = 4*(b1+1)*a*a;           // error increment
  double err = dx+dy+b1*a*a, e2;                          // error of 1.step

  y0 += (b+1)/2; y1 = y0-b1;                              // starting pixel
  a = 8*a*a; b1 = 8*b*b;

  int initialY0 = y0;
  int initialY1 = y1;
  int initialX0 = x0;
  int initialX1 = x1 + hPixels;

  do {
    proc(x0, y0 + vPixels, x1 + hPixels, data);
    proc(x0, y1, x1 + hPixels, data);
    e2 = 2*err;
    if (e2 <= dy) { y0++; y1--; err += dy += a; }                 // y step
    if (e2 >= dx || 2*err > dy) { x0++; x1--; err += dx += b1; }  // x step
  } while (x0 <= x1);

  while (y0 + vPixels - y1 + 1 < h) {             // too early stop of flat ellipses a=1
    proc(x0-1, ++y0 + vPixels, x0-1, data);       // -> finish tip of ellipse
    proc(x1+1 + hPixels, y0 + vPixels, x1+1 + hPixels, data);
    proc(x0-1, --y1, x0-1, data);
    proc(x1+1 + hPixels, y1, x1+1 + hPixels, data);
  }

  if (vPixels > 0) {
    for (int i = initialY1 + 1; i < initialY0 + vPixels; i++)
      proc(initialX0, i, initialX1, data);
  }
}

}


namespace ct{
    static Color additive(Color src, Color dst){
        return {
            (unsigned char)std::clamp((int)src.r + dst.r, 0, 255),
            (unsigned char)std::clamp((int)src.g + dst.g, 0, 255),
            (unsigned char)std::clamp((int)src.b + dst.b, 0, 255),
            (unsigned char)std::clamp((int)src.a + dst.a, 0, 255)
        };
    }

    void bake_global_light(Image* img, ColorNoAlpha color, double intensity){
        if(img->format != PIXELFORMAT_UNCOMPRESSED_R8G8B8A8){
            throw std::runtime_error("img->format != PIXELFORMAT_UNCOMPRESSED_R8G8B8A8");
        }
        int numel = img->width * img->height;
        Color* pixels = (Color*)img->data;
        for(int i=0; i<numel; i++) pixels[i] = additive(color, pixels[i]);
    }

    void bake_point_light(Image* img, ColorNoAlpha color, double intensity, int x, int y, int r, Image* cookie){
        if(img->format != PIXELFORMAT_UNCOMPRESSED_R8G8B8A8){
            throw std::runtime_error("img->format != PIXELFORMAT_UNCOMPRESSED_R8G8B8A8");
        }
        if(cookie->format != PIXELFORMAT_UNCOMPRESSED_GRAYSCALE){
            throw std::runtime_error("cookie->format != PIXELFORMAT_UNCOMPRESSED_GRAYSCALE");
        }
        y = img->height - y - 1;
        for(int i=x-r; i<=x+r; i++){
          for(int j=y-r; j<=y+r; j++){
            int u = (i - x) / (double)r * cookie->width;
            int v = (j - y) / (double)r * cookie->height;
            unsigned mask = ((unsigned char*)cookie->data)[cookie->width * v + u];
            Color* pixel = (Color*)img->data + img->width * j + i;
            *pixel = additive(color.with_intensity(mask / 255.0), *pixel);
          }
        }

        // using ArgsT = std::tuple<Image*, Color, int, int, int>;
        // ArgsT args{img, color, x, y, r};
        // aseprite::algo_ellipsefill(x - r, y - r, x + r, y + r, 0, 0, &args, [](int start_x, int y, int end_x, void* data){
        //     auto [img, color, x0, y0, r] = *(ArgsT*)data;
        //     int base = img->width * (img->height-y-1);
        //     Color* pixels = (Color*)img->data + base;
        //     for(int x = start_x; x <= end_x; x++){
        //         float distance = sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0));
        //         float distance01 = std::clamp(distance / r, 0.0f, 1.0f);
        //         Color new_color = color;
        //         if(distance01 >= 0.75){
        //           new_color.a = (unsigned char)(color.a * (1.0 - distance01));
        //         }
        //         pixels[x] = additive(new_color, pixels[x]);
        //     }
        // });
    }
}
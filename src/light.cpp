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
    void bake_global_light(Image* img, Color color, double intensity){
        if(img->format != PIXELFORMAT_UNCOMPRESSED_R32G32B32A32){
            throw std::runtime_error("img->format != PIXELFORMAT_UNCOMPRESSED_R32G32B32A32");
        }
        int numel = img->width * img->height;
        HdrColor* pixels = (HdrColor*)img->data;
        for(int i=0; i<numel; i++) pixels[i] = HdrColor::additive(HdrColor(color, intensity), pixels[i]);
    }

    void bake_point_light(Image* img, Color color, double intensity, int x, int y, int r, Image* cookie){
        if(img->format != PIXELFORMAT_UNCOMPRESSED_R32G32B32A32){
            throw std::runtime_error("img->format != PIXELFORMAT_UNCOMPRESSED_R32G32B32A32");
        }
        if(cookie && cookie->format != PIXELFORMAT_UNCOMPRESSED_GRAYSCALE){
            throw std::runtime_error("cookie->format != PIXELFORMAT_UNCOMPRESSED_GRAYSCALE");
        }
        if(r <= 0) return;
        y = img->height - y - 1;
        for(int i=0; i<=2*r; i++){
          for(int j=0; j<=2*r; j++){
            int x_ = x - r + i;
            int y_ = y - r + j;
            if(x_ < 0 || x_ >= img->width || y_ < 0 || y_ >= img->height) continue;
            HdrColor* pixel = (HdrColor*)img->data + img->width * y_ + x_;

            if(cookie){
              double u = i / (2.0 * r);   // [0, 1]
              double v = j / (2.0 * r);   // [0, 1]
              int u_offset = (int)(u * (cookie->width - 1));
              int v_offset = (int)(v * (cookie->height - 1));
              u_offset = std::clamp(u_offset, 0, cookie->width - 1);
              v_offset = std::clamp(v_offset, 0, cookie->height - 1);
              unsigned mask = ((unsigned char*)cookie->data)[cookie->width * v_offset + u_offset];
              *pixel = HdrColor::additive(HdrColor(color, mask / 255.0 * intensity), *pixel);
            }else{
              float distance = sqrt((i - r) * (i - r) + (j - r) * (j - r));
              float distance01 = std::clamp(distance / r, 0.0f, 1.0f);
              // quadratic attenuation
              *pixel = HdrColor::additive(HdrColor(color, (1.0 - distance01 * distance01) * intensity), *pixel);
            }
          }
        }
    }
}
from typing import Generic, TypeVar
import raylib as rl
import c

from _carrotlib import _get_cjk_codepoints
from . import g as _g

T = TypeVar("T")

class ResourceLoader(Generic[T]):
    def __init__(self, f_load, f_unload):
        self.f_load = f_load
        self.f_unload = f_unload
        self.cache = {}

    def __call__(self, *args) -> T:
        res = self.cache.get(args)
        if res is None:
            res = self.f_load(*args)
            self.cache[args] = res
        return res
    
    def unload_all(self):
        for res in self.cache.values():
            self.f_unload(res)
        self.cache.clear()

def _load_font_cjk(path: str) -> rl.Font:
    p_data, count = _get_cjk_codepoints()
    UNSCALING = 10
    return rl.LoadFontEx(path, _g.default_font_size * UNSCALING, p_data, count)

def _load_texture_scaled(path: str, scale: float):
    image = rl.LoadImage(path)
    rl.ImageResizeNN(image.addr(), int(image.width*scale), int(image.height*scale))
    texture = rl.LoadTextureFromImage(image)
    rl.UnloadImage(image)
    return texture

def _load_square_texture(size: int):
    raw_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x04\x00\x00\x00\x04\x08\x00\x00\x00\x00\x8c\x9a\xc1\xa2\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x11IDAT\x08\x99c\xfc\xcf\xc0\xc0\xc0\xc4\x80B\x00\x00\x13Q\x01\x07\x9e\xa3\x9e{\x00\x00\x00\x00IEND\xaeB`\x82'
    data = c.struct(len(raw_data))
    for i in range(len(raw_data)):
        data.write_uchar(raw_data[i], offset=i)
    image = rl.LoadImageFromMemory('.png', data.addr(), data.sizeof())
    rl.ImageResizeNN(image.addr(), size, size)
    texture = rl.LoadTextureFromImage(image)
    rl.UnloadImage(image)
    return texture

# You should not modify cached resources directly!!
load_texture = ResourceLoader[rl.Texture2D](rl.LoadTexture, rl.UnloadTexture)
load_texture_scaled = ResourceLoader[rl.Texture2D](_load_texture_scaled, rl.UnloadTexture)
load_square_texture = ResourceLoader[rl.Texture2D](_load_square_texture, rl.UnloadTexture)

load_font_cjk = ResourceLoader[rl.Font](_load_font_cjk, rl.UnloadFont)
load_font = ResourceLoader[rl.Font](rl.LoadFont, rl.UnloadFont)
load_sound = ResourceLoader[rl.Sound](rl.LoadSound, rl.UnloadSound)
load_image = ResourceLoader[rl.Image](rl.LoadImage, rl.UnloadImage)

def _unload_all_resources():
    load_texture.unload_all()
    load_font_cjk.unload_all()
    load_font.unload_all()
    load_sound.unload_all()
    load_image.unload_all()


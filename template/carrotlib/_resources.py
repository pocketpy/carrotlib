from typing import Generic, TypeVar
import raylib as rl

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
    UNSCALING = 8
    return rl.LoadFontEx(path, _g.default_font_size * UNSCALING, p_data, count)

def _load_texture_scaled(path: str, scale: float):
    image = rl.LoadImage(path)
    rl.ImageResizeNN(image.addr(), int(image.width*scale), int(image.height*scale))
    texture = rl.LoadTextureFromImage(image)
    rl.UnloadImage(image)
    return texture

def _load_square_texture(size: int):
    image = rl.GenImageColor(size, size, rl.Color(255, 255, 255, 255))
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
    load_texture_scaled.unload_all()
    load_square_texture.unload_all()
    
    load_font_cjk.unload_all()
    load_font.unload_all()
    load_sound.unload_all()
    load_image.unload_all()


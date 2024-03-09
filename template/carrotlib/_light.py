import raylib as rl
from typing import TypeVar
from linalg import vec2
from _carrotlib import _bake_global_light, _bake_point_light

from ._colors import Colors
from ._node import Node
from . import g as _g

class LightMaterial:
    def __init__(self, lightmap: 'Lightmap'):
        self.lightmap = lightmap
        self.shader = rl.LoadShaderFromMemory("""
#version 330

// Input vertex attributes
in vec3 vertexPosition;
in vec2 vertexTexCoord;
in vec4 vertexColor;

// Input uniform values
uniform mat4 mvp;

// Output vertex attributes (to fragment shader)
out vec4 screenPos;
out vec2 fragTexCoord;
out vec4 fragColor;

vec4 ComputeScreenPos(vec4 pos){
    vec4 o;
    o.x = 0.5 * (pos.x + pos.w);
    o.y = 0.5 * (pos.y + pos.w);
    o.zw = pos.zw;
    return o;              
}

void main()
{
    fragTexCoord = vertexTexCoord;
    fragColor = vertexColor;

    vec4 clipPos = mvp * vec4(vertexPosition, 1.0);
    screenPos = ComputeScreenPos(clipPos);
    gl_Position = clipPos;
}
""",

"""
#version 330

// Input vertex attributes (from vertex shader)
in vec2 fragTexCoord;
in vec4 fragColor;
in vec4 screenPos;

// Input uniform values
uniform sampler2D texture0;
uniform sampler2D texture1;     // lightmap texture
uniform vec4 colDiffuse;        // tint color
uniform vec2 texelSize;         // texture texel size

// Output fragment color
out vec4 finalColor;

void main()
{
    vec2 screenCoord = screenPos.xy / screenPos.w;
    // pixelated
    screenCoord = floor(screenCoord / (texelSize*4)) * (texelSize*4);
    vec4 texel = texture(texture0, fragTexCoord);   // Get texel color
    vec4 light = texture(texture1, screenCoord);    // Get light color
    finalColor = texel * colDiffuse * fragColor * light;
}""")
        self.loc_lightmap = rl.GetShaderLocation(self.shader, "texture1")
        self.loc_texel_size = rl.GetShaderLocation(self.shader, "texelSize")

    def __enter__(self):
        rl.BeginShaderMode(self.shader)
        rl.SetShaderValueTexture(self.shader, self.loc_lightmap, self.lightmap.texture)
        texel_size = vec2(1.0 / self.lightmap.texture.width, 1.0 / self.lightmap.texture.height)
        rl.SetShaderValue(self.shader, self.loc_texel_size, texel_size.addr(), rl.SHADER_UNIFORM_VEC2)
        return self
    
    def __exit__(self, *args):
        rl.EndShaderMode()
        return self
    

T = TypeVar('T', bound='Light2D')

class Lightmap:
    def __init__(self, width: int, height: int) -> None:
        self.image = rl.GenImageColor(width, height, Colors.Blank)
        rl.ImageFormat(self.image.addr(), rl.PIXELFORMAT_UNCOMPRESSED_R32G32B32A32)
        self.texture = rl.LoadTextureFromImage(self.image)
        # lights
        self.lights = []

    def update(self):
        rl.ImageClearBackground(self.image.addr(), Colors.Black)
        for light in self.lights:
            light._bake(self.image)
        rl.UpdateTexture(self.texture, self.image.data)

    def destroy(self):
        rl.UnloadTexture(self.texture)
        rl.UnloadImage(self.image)

class Light2D(Node):
    color: rl.Color = Colors.White
    intensity: float = 1.0

    def __init__(self, lightmap: Lightmap, name=None, parent=None) -> None:
        super().__init__(name=name, parent=parent)
        self.lightmap = lightmap
        lightmap.lights.append(self)

    def _bake(self, image: rl.Image) -> None:
        raise NotImplementedError
    
    def on_destroy(self):
        try:
            self.lightmap.lights.remove(self)
        except ValueError:
            pass


class GlobalLight2D(Light2D):
    def _bake(self, image: rl.Image) -> None:
        _bake_global_light(image.addr(), self.color, self.intensity)


class PointLight2D(Light2D):
    # TODO: support scale
    # TODO: support pixelate
    radius: int = 1

    def _bake(self, image: rl.Image) -> None:
        screen_pos = _g.world_to_viewport.transform_point(self.global_position)
        x, y = round(screen_pos.x), round(screen_pos.y)
        _bake_point_light(image.addr(), self.color, self.intensity, x, y, self.radius)
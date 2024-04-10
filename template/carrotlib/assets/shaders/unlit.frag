// Input vertex attributes (from vertex shader)
_IN_ vec2 fragTexCoord;
_IN_ vec4 fragColor;

// Input uniform values
uniform sampler2D texture0;
uniform vec4 colDiffuse;        // tint color

_DEFINE_GL_FRAG_COLOR_

void main()
{
    vec4 texel = texture(texture0, fragTexCoord);
    texel.xyz = sRGBToLinear(texel.xyz);
    vec4 finalColor = texel * colDiffuse * fragColor;
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
    _GL_FRAG_COLOR_ = finalColor;
}

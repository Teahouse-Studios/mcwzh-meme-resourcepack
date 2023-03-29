#version 150

#moj_import <fog.glsl>
#moj_import "average16x.glsl"

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;
in vec4 normal;

out vec4 fragColor;

void main() {
    float alpha = texture(Sampler0, texCoord0).a;
    if (alpha == 0.0) {
        discard;
    }
    vec4 color = average_16x(Sampler0, texCoord0) * vertexColor * ColorModulator;
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
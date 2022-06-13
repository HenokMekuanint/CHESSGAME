in vec3 position;
in vec3 color;
uniform mat4 transform;
out vec3 newColor;
void main()
   {
     gl_Position = transform * vec4(position, 1.0);
     newColor = color;
   }

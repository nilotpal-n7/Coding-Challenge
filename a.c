const float theta_spacing = 0.07;
const float phi_spacing   = 0.02;
const float screen_width = 1200;
const float screen_height = 1200;
const float pi = 3.14;
const float R1 = 1;
const float R2 = 2;
const float K2 = 5;
const float K1 = screen_width*K2*3/(8*(R1+R2));

render_frame(float A, float B) {
  float cosA = cos(A), sinA = sin(A);
  float cosB = cos(B), sinB = sin(B);

  char output[0..screen_width, 0..screen_height] = ' ';
  float zbuffer[0..screen_width, 0..screen_height] = 0;

  for (float theta=0; theta < 2*pi; theta += theta_spacing) {
    float costheta = cos(theta), sintheta = sin(theta);

    for(float phi=0; phi < 2*pi; phi += phi_spacing) {
      float cosphi = cos(phi), sinphi = sin(phi);

      float circlex = R2 + R1*costheta;
      float circley = R1*sintheta;
      float x = circlex*(cosB*cosphi + sinA*sinB*sinphi)
        - circley*cosA*sinB; 
      float y = circlex*(sinB*cosphi - sinA*cosB*sinphi)
        + circley*cosA*cosB;
      float z = K2 + cosA*circlex*sinphi + circley*sinA;
      float ooz = 1/z;
      int xp = (int) (screen_width/2 + K1*ooz*x);
      int yp = (int) (screen_height/2 - K1*ooz*y);
      float L = cosphi*costheta*sinB - cosA*costheta*sinphi -
        sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi);

      if (L > 0) {
        if(ooz > zbuffer[xp,yp]) {
          zbuffer[xp, yp] = ooz;
          int luminance_index = L*8;
          output[xp, yp] = ".,-~:;=!*#$@"[luminance_index];
        }
      }
    }
  }

  printf("\x1b[H");
  for (int j = 0; j < screen_height; j++) {
    for (int i = 0; i < screen_width; i++) {
      putchar(output[i,j]);
    }
    putchar('\n');
  }
  
}

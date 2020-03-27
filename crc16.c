#include <stdio.h>

int main(int argc, char* argv[]) {

    unsigned char data[0xC00];
    
    FILE *patch;
    patch = fopen(argv[1], "rb"); // hdmi patch
    fread(data, sizeof(data), 1, patch);
    fclose(patch);

	unsigned char *result = data;
    
    unsigned int v5 = 0xC00; // -2 for gen
    unsigned int v7 = 0;
    unsigned int v8 = 0;
    unsigned int v9 = 0;
    unsigned int v10 = 0;
    _Bool v11 = 0;
    unsigned int i = 0;
    
    for ( i = 0; ; i = v7 )
    {
      v11 = v5-- >= 1;
      if ( !v11 )
        break;
      v7 = i;
      v8 = *result++;
      v9 = 0;
      do
      {
        v10 = v8 ^ v7;
        v7 >>= 1;
        v8 >>= 1;
        if ( v10 << 31 )
          v7 ^= 0x1021u;
        ++v9;
      }
      while ( v9 < 8 );
    }

    if(!i)
        printf("Check: Ok (%04x)\n", i);
    else
        printf("Check: Failed (%04x)\n", i);
}
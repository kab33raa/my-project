//4th
#include <stdio.h>

int main() {
    float A; 
    float P;
    float r;
    float t; 
    printf("enter principal : ");
     printf("enter rate : ");
       printf("enter time : ");
    scanf("%f", &P, &r, &t);
    A = P * (1 + r * t);
    printf("Final Amount (A) = %.2f\n", A);

    return 0;
}

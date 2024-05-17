#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct{
char *command;
float freq;
int power;
}cmd_t;


int main(){

    printf("Lets play with structure now");
    cmd_t var1;
    var1.command="gen_freq";
    var1.freq = 10000;
    var1.power = 5;

    printf("parsed command is %s",var1.command);
    printf("Generate Frequency : %f",var1.freq);
    printf("Required Pwer is : %d",var1.power);    


    return 0;
}
#include <stdio.h>
int main(){
	puts("Here we go!");
        setvbuf(stdin,0,2,0);
        setvbuf(stdout,0,2,0);
        char buf[0x100];
        while(1){
                printf(">> ");
                read(0,buf,0x1000);
                printf(&buf);
        }
        return 0;
}


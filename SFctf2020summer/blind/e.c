#include <stdio.h>
int main(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	puts(0x804a010);
//	printf(0x804a010);
}

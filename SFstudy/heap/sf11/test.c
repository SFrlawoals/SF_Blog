#include <stdio.h>
#include <stdlib.h>

void my_init(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
}

int main(){
	my_init();
	char name[0x20];
	char *ptr = malloc(0x410);
	malloc(0x20);
	free(ptr);
	
	getchar();

	malloc(0x410);
	scanf("%s",name);
	
}

#include <stdio.h>


unsigned long int fake_table[0x20];

void trap(){
	while(1)
		puts("And there are no friends at dusk");
}	

void my_init(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	
	fake_table[0] = 0;
	fake_table[1] = 0;
	for(int i=2;i<0x20;i++)
		fake_table[i] = &trap;
}

int main(){
	unsigned long int *target = 0x7ffff7dd19b8;
	my_init();

	puts("We live in a twilight world");

	*target = &fake_table;	// -- KEY
	getchar();

	puts("What???");
	
	return 0;
}

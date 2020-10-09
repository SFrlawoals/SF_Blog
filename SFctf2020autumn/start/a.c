#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char name[0x30];
char target[0x10];

void init(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	strncpy(target,"SUMMER\x00",9);
}

void comment(){
	puts("This is our last journey :/");
	puts("Can you tell me how you feel..? ");
	printf("> ");
	read(0,name,0x30);
	name[strlen(name)-1] = NULL;
	printf("Let's record the past %s\n",target);
}

void menu(){
	puts("");
	puts("M alloc	-- write record");
	puts("F ree	-- delete record");
	printf("> ");
}

int main(){
	char *contents[10]={0,};
	unsigned int idx;
	char sel;
	init();
	comment();
	
	for(int i=0;i<9;i++){
		menu();
		scanf("%c",&sel);
		getchar();
		switch(sel){
			case 'M':
				contents[i] = malloc(0x28);
				printf("Data: ");
				read(0,contents[i],0x28);
				break;

			case 'F':
				printf("Index: ");
				scanf("%d",&idx);
				free(contents[idx]);
				getchar();
				break;

			default:
				return 0;
				break;		
		}
	}
	
	puts("You've done a great job XD");
	
	if(strncmp(target,"AUTUMN",6)==0){
		system("cat flag");
	}else{
		puts("Let's try harder !!!");
		return 0;
	}

}

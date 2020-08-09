#include <stdio.h>
#include <stdlib.h>
char name[0x10];
char target[0x9];

void init(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	strncpy(target,"RAINYDAY\x00",9);
}

void comment(){
	puts("Hello, What's your name?");
	read(0,name,0x10);
	name[strlen(name)-1] = NULL;
	printf("%s, Today is %s\n",name,target);
	puts("What are you going to do today?");
}

void menu(){
	puts("1. write");
	puts("2. erase");
	printf("> ");
}

int main(){
	char *contents[10]={0,};
	unsigned int idx,sel;
	init();
	comment();
	
	for(int i=0;i<9;i++){
		menu();
		scanf("%d",&sel);
		switch(sel){
			case 1:
				contents[i] = malloc(0x10);
				printf("contents: ");
				read(0,contents[i],0x10);
				break;

			case 2:
				printf("Index: ");
				scanf("%d",&idx);
				free(contents[idx]);
				break;

			default:
				return 0;
				break;		
		}
	}
	getchar();
	puts("You know, but you can't because it rains");
	printf("feeling: ");
	if(*contents[1] == NULL){
		char *tmp = malloc(0x10);
		read(0,tmp,0x10);
	}else read(0,contents[1],0x10);
	
		
	if(strncmp(target,"GREATDAY",8)==0){
		system("cat flag");
	}else{
		puts("It's raining. Just study.");
		return 0;
	}

}

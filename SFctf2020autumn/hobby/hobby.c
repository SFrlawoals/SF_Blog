#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *ptr[7];

void print_function();
void init();
void add();
void change();
void delete();
void show();

int main()
{
	char button[0x10];
	int cnt=0;
	int len=0;
	init();
	while (1){
		print_function();
		len = scanf("%s",button);
		button[len] = 0;
		switch(atol(button)){
			case 1:
				if(cnt>=7) {
					printf("Too many Profiles!");
					exit(0);
				}
				add(cnt);
				cnt++;
				break;

			case 2:
				change(cnt);
				break;		

			case 3:
				delete();
				cnt--;
				break;

			case 4:
				if(*(ptr+0x8) != 0){
					show(cnt);
				}
				break;		
	
			case 5:
				exit(0);
				break;
		}
	}
}

void init()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
}

void print_function()
{
	printf("===================\n");
	printf("1.Enter the profile.\n");
	printf("2.Change the profile.\n");
	printf("3.Delete the profile.\n");
	printf("===================\n");
	printf(">> ");
}

void add(int cnt)
{
	int len;
	getchar();
	printf("Enter the profile data\n");
	ptr[cnt]=malloc(0xa8);
	printf("Name : ");
	len=read(0,ptr[cnt]+0x8,0x7);
	//*(ptr[cnt]+len)='\x00';

	printf("Hobby : ");
	len=read(0,ptr[cnt]+0x10,0x98);
	//*(ptr[cnt]+len)='\x00';
	
	*(ptr[cnt])='1';
	printf("Sucess!\n");
}

void change(int cnt)
{
	int idx,len;
	
    	printf("Enter the index: ");
	scanf("%d",&idx);
	getchar();
	if((ptr[idx])==0)
		printf("Wrong index!\n");
	else {
		printf("Name : ");
        	len=read(0,ptr[idx]+0x8,0x7);
	
        	printf("Hobby : ");
        	len=read(0,ptr[idx]+0x10,0x98);
	        //*(ptr[idx]+len-1)='\x00';
	}	
}

void delete()
{
	int idx;
	printf("Select the index: ");
	scanf("%d",&idx);
	if(*(ptr[idx]) != 0) {
		*(ptr[idx])=0;
		free(ptr[idx]);
	}
}

void show(int cnt)
{
	
	for(int i=0; i<cnt; i++) 
		printf("%s\n",ptr[i]);
}

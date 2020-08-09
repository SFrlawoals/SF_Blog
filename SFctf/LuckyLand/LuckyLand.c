#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#pragma GCC visibility push(hidden)

struct USER{
	char number[4];
	char name[20];
	unsigned int LUK;
}user;

void intro(){
	puts("							      <woaalsdl12@gmail.com>");
	puts("");
	puts("     ██╗ █████╗ ███╗   ███╗    ██████╗  ██████╗ ████████╗    ███████╗███████╗███████╗");
	puts("     ██║██╔══██╗████╗ ████║    ██╔══██╗██╔═══██╗╚══██╔══╝    ╚════██║╚════██║╚════██║");
	puts("     ██║███████║██╔████╔██║    ██████╔╝██║   ██║   ██║           ██╔╝    ██╔╝    ██╔╝");
	puts("██   ██║██╔══██║██║╚██╔╝██║    ██╔═══╝ ██║   ██║   ██║          ██╔╝    ██╔╝    ██╔╝ ");
	puts("╚█████╔╝██║  ██║██║ ╚═╝ ██║    ██║     ╚██████╔╝   ██║          ██║     ██║     ██║  ");
	puts(" ╚════╝ ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝      ╚═════╝    ╚═╝          ╚═╝     ╚═╝     ╚═╝  ");
	puts("");
}

void special(){
	unsigned int test = 0;
	srand(time(NULL));

	test = (unsigned int)rand()%10;
	if(test == 7){
		puts("JAM: Lady Luck smiles at you.");
		user.number[0] += 20;
		user.LUK = 1;
	}else user.LUK = 0;

}

void init(){	//prologue
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	intro();
	
	puts("???: What's your name, bro?");
	printf(">> ");
	scanf("%19s",user.name);
	user.number[0] = strlen(user.name)*2;
	special();
}

void comment(){
	printf("\n%s's property %d$\n",user.name,user.number[0]);
	puts("1. Hit the JackPot");
	puts("2. Get money by Time");
	puts("3. Exit");
	printf(">> ");
}

void GET_FLAG(){
	FILE *fp = fopen("./flag","r");
	char flag[30];
	fscanf(fp,"%s",flag);
	printf("%s",flag);
	fclose(fp);
	exit(0);
}

void JackPot(){

	for(int i=1;i<=3;i++){
		srand(time(NULL));
		sleep(1);
		user.number[i] = (unsigned int)rand()%10;
		printf("[%d] ",user.number[i]);
	}printf("\n");
	
	if(user.number[1] == 7 && user.number[2] == 7 && user.number[3] == 7){
		puts("???: Congratulations. You're so lucky");
		user.number[0] += 50;
		if(user.LUK >= 3){
			puts("JAM: You're a very lucky person.");
			GET_FLAG();
		}else user.LUK++;

	}else{
		puts("???: That's too bad.");
		user.number[0] -= 10;
		if(user.number[0] < 0){
			puts("???: Get the beggar out of here!!!");
			exit(0);
		}
	}

}

void Get_Money(){
	unsigned int time=0;
	if(0 <= user.number[0] && user.number[0] <= 127){
		puts("???: How much do you need, kiddo?");
		printf(">> ");
		scanf("%d",&time);

		if(time > 10){
			puts("???: This is a gambling house, not a place to work!");
			puts("     Go gamble, brother.");
		}else{
			sleep(time/2);
			puts("???: See you again, XD");
			user.number[0] += time;

		}

		if(user.number[0] < 0 && user.LUK == 0){
			puts("???: You have a fat pocket, huh? I'll take it.");
			user.number[0] = 0;
		}

	}else{
		if(user.LUK > 0){
			puts("JAM: You made enough money to buy a gambling house.");
			puts("     You're such a great person.\n");
			GET_FLAG();
		}
	}
}

int main(){
	unsigned int sel = 0;
	init();
	alarm(300);
	while(1){
		comment();
		scanf("%d",&sel);
		switch(sel){
			case 1:
				JackPot();
				break;
			case 2:
				Get_Money();
				break;
			case 3:
				exit(0);
				break;
			default:
				puts("???: Stupid people are not accepted.");
				exit(0);
				break;
		}
	}

	return 0;
}





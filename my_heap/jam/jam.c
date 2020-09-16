// gcc -Wl,-z,relro,-z,now -fPIE -pie -o jam jam.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>


void jam_image(){
    puts("");
    puts("");
    puts("             @@@@@@@@@@@@@@@@@@@@@@@@                                                     ");
    puts("            @@                       @@,                                                  ");
    puts("           @@                          @@#                                                ");
    puts("          @@                             @@@                                               ");
    puts("         @@                    /@@@      @@                                               ");
    puts("        @@@@@    @@@@@@@@@@@@@@@  #@@@@@ @@                                               ");
    puts("         %@@  @@&@                        @@@                                             ");
    puts("         @@            @@@   @@@           @@@                                            ");
    puts("        @@@        @@. @@ @@@  @            @@                                            "); puts("        @@/          @@    ,@@@@@@@@         @@                                           ");
    puts("       /@@            #@@@         @@.       @@      @@@@@@@@@@@                          ");
    puts("        @@%          @@     *      @@       %@@           @@@(                            ");
    puts("         @@          @&            @@       @@            @@@,                            ");
    puts("         @@@          @@@     @    @      @@@             @@@                             ");
    puts("          @@@            @@@@/    @%     @@@              @@@    @@@      @@ ,@  @@@@     ");
    puts("            @@@               @@@@@     @@@       @@@    @@@   #@@ @@@/   @@@@@@@@  @@    ");
    puts("              @@                      @@@          @@@@@@@@,   @@ @@@@@*  @@   @@   @@    ");
    puts("                @@@@@@@@@@@@@@@@@@@@@@@@             @@@@@      (@/   @@#  @@       @@    ");
    puts("");
    puts("");
}   

static void install_seccomp()
{
        static unsigned char filter[] =
        {
                32,0,0,0,4,0,0,0,21,0,0,14,62,0,0,192,
                32,0,0,0,0,0,0,0,53,0,12,0,0,0,0,64,
                21,0,10,0,0,0,0,0,21,0,9,0,1,0,0,0,
                21,0,8,0,2,0,0,0,21,0,7,0,3,0,0,0,
                21,0,6,0,33,0,0,0,21,0,5,0,60,0,0,0,
                21,0,4,0,231,0,0,0,21,0,3,0,12,0,0,0,
                21,0,2,0,9,0,0,0,21,0,1,0,10,0,0,0,
                21,0,0,1,15,0,0,0,6,0,0,0,0,0,255,127,
                6,0,0,0,0,0,0,0
        };
        struct prog
        {
                unsigned short len;
                unsigned char *filter;
        }

        rule =
        {
                .len = sizeof(filter) >> 3,
                .filter = filter
        }; 
        if ( prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0 )
        {
                perror("prctl(PR_SET_NO_NEW_PRIVS)");
                exit(2);
        }

        if ( prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0 )
        {
                perror("prctl(PR_SET_SECCOMP)");
                exit(2);
        }
}

struct BOTTLE
{
        char name[0x8];
        char ingredient[0x18];
        char *description;
        struct bottle *next;
};

struct BOTTLE *bottle;
unsigned int bottle_cnt;

void my_init(){
        install_seccomp();
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
        bottle = malloc(sizeof(struct BOTTLE));
        strcpy(bottle->name,"KJM\x00");
        strcpy(bottle->ingredient,"Strawberry\x00");
        bottle->description = malloc(sizeof(char)*0x100);
        strcat(bottle->description,"\nThank you for trying even though you are having a hard time.\n");
        strcpy(bottle->description,"Thank you for trying even though you are busy.\n");
        strcat(bottle->description,"Thank you for your continued efforts.\n");
        strcat(bottle->description,"I hope you have a fresh day!\n");

        bottle->next = NULL;
        bottle_cnt = 0;
}

void command_menu(){
        puts("");
        puts("==================================================");
        puts("M ake     - make a jam ");
        puts("A dd      - add a description");
        puts("S how     - show all jam");
        puts("T ake     - take a your jam");
        puts("E rase    - erase a description of jam");
        puts("R estart  - restart making");
        printf("Your choice > ");
}

void make(){
        struct BOTTLE *p = NULL;
        int res;
        char tmp[0x10];
        if(bottle_cnt > 10){
                puts("You don't have bottle any more");
        }else{
                for(p = bottle;p->next;p=p->next);
                p->next = malloc(sizeof(struct BOTTLE)); 
                p = p->next;  
                p->next = NULL;       
                printf("Input name (length:7) > ");
                
                res = read(0,p->name,8);
                (p->name)[res-1] = '\x00';
              
                printf("Select ingredient (length:23) > ");
                res = read(0,p->ingredient,24);
                (p->ingredient)[res-1] = '\x00';
                bottle_cnt++;
                
        }
}

void add(){
        struct BOTTLE *p = NULL;
        char tmp[8];
        int res;
        int check = 0;
        
        printf("Input name > ");
        res = read(0,tmp,8);
        tmp[res-1] = '\x00';

        for(p = bottle;;p=(p->next)){
                if(strncmp(p->name,tmp,res) == 0)
                {
                        if(!(p->description)){
                                if(bottle_cnt == 1){
                                        puts("This is your first work. Be careful.");
                                        p->description = malloc(sizeof(char)*0x100);
                                }else p->description = malloc(sizeof(char)*0x30);
                        }

                        printf("Input description > ");
                        res = read(0,p->description,0x30);
                        p->description[res-1] = '\x00';
                        check++;
                }
                if(p->next == NULL) break;

        }
        
        if(!check)
                puts("There is no such jam here!");

}

void show(){
        struct BOTTLE *p = NULL;
        for(p = bottle;;p=p->next){
                puts("");
                printf("[ %s ]\n",p->name);
                printf("Ingredient : %s\n",p->ingredient);
                printf("description : %s\n",(!p->description) ? "Not entered or deleted" : p->description);

                if(p->next == NULL) break;
        }
}

void take(){
        puts("You died after eating your jam. That's too bad.");
        exit(-1);
}

void erase(){
        struct BOTTLE *p = NULL;
        char tmp[8];
        int res;
        int check = 0;
        
        printf("Input name > ");
        res = read(0,tmp,8);
        tmp[res-1] = '\x00';

        for(p = bottle;;p=(p->next)){
                if(strncmp(p->name,tmp,res) == 0)
                {
                        free(p->description);
                        puts("Complete");
                        check ++;
                        break;
                }
                if(p->next == NULL) break;
        }
        if(!check) puts("Failed");
}

void restart(){
        puts("If you were a master, you wouldn't have restarted...");
        puts("Cheer up with this picture !!!");
        jam_image();

        exit(0);
}

int main(){
    char choice;
	my_init();
        while(1){
                command_menu();
                scanf("%c",&choice);
                getchar();
                switch(choice){
                        case 'M':
                                make();
                                break;
                        case 'A':
                                add();
                                break;

                        case 'S':
                                show();
                                break; 

                        case 'T':
                                take();
                                break;

                        case 'E':
                                erase();
                                break;

                        case 'R':
                                restart();
                                                        
                        default:
                               break; 
                }
        }
}

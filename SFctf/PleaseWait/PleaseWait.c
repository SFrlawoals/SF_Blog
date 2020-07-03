#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>     //io.h
#pragma warning(disable:4996)

void start_comment() {
        puts("");
        puts("                                                               author : jam_m <woaalsdl12@gmail.com>");
        puts("");
        puts("@@@@@@@   @@@       @@@@@@@@   @@@@@@    @@@@@@   @@@@@@@@     @@@  @@@  @@@   @@@@@@   @@@  @@@@@@@");
        puts("@@@@@@@@  @@@       @@@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@@     @@@  @@@  @@@  @@@@@@@@  @@@  @@@@@@@ ");
        puts("@@!  @@@  @@!       @@!       @@!  @@@  !@@       @@!          @@!  @@!  @@!  @@!  @@@  @@!    @@! ");
        puts("!@!  @!@  !@!       !@!       !@!  @!@  !@!       !@!          !@!  !@!  !@!  !@!  @!@  !@!    !@!  ");
        puts("@!@@!@!   @!!       @!!!:!    @!@!@!@!  !!@@!!    @!!!:!       @!!  !!@  @!@  @!@!@!@!  !!@    @!!");
        puts("!!@!!!    !!!       !!!!!:    !!!@!!!!   !!@!!!   !!!!!:       !@!  !!!  !@!  !!!@!!!!  !!!    !!! ");
        puts("!!:       !!:       !!:       !!:  !!!       !:!  !!:          !!:  !!:  !!:  !!:  !!!  !!:    !!: ");
        puts(":!:        :!:      :!:       :!:  !:!      !:!   :!:          :!:  :!:  :!:  :!:  !:!  :!:    :!: ");
        puts(" ::        :: ::::   :: ::::  ::   :::  :::: ::    :: ::::      :::: :: :::   ::   :::   ::     :: ");
        puts(" :        : :: : :  : :: ::    :   : :  :: : :    : :: ::        :: :  : :     :   : :  :       :");
        puts("");
}

typedef struct TIMER{
        char *data;
        struct TIMER* next;
}Timer;

void init(Timer *t,int flag) {
        t->data = (char*)malloc(sizeof(char) * 0x30);
        if(flag){
                strcpy(t->data, "Hello World");
        }else{
                printf("%ds...\n", flag);
                read(0, t->data, 0x30);
        }
        t->next = NULL;
};

void time_flow(int i, Timer *t) {
        char* p;
        printf("%ds...\n", i);
        printf(">> ");
        while (t->next) {
                t = t->next;
        }

        t->next = (Timer*)malloc(sizeof(Timer));
        t->next->data = malloc(sizeof(char)*(i*0x10));
        t->next->next = NULL;
        read(0, t->next->data, i * 0x10);
        for (p=t->next->data;*p != '\n';p++);
        *p = 0;

}

void print_record(Timer *t) {
        Timer* tmp;
        int i = 0;
        puts("");
        puts("─────────────────  << RECORD >> ────────────────");
        while (t->next) {
                tmp = t->next;
                printf("%2d %s\n",i ,t->data);
                free(t->data);
                free(t);
                t = tmp;
                i++;
        }
        printf("%2d %s\n", i,t->data);
        free(t);
        puts("────────────────────────────────────────────────");
        puts("");
}

int main() {
        int i = 0,flag = 1;
        char buf[0x5];
        setvbuf(stdin,0,2,0);
        setvbuf(stdout,0,2,0);
        start_comment();
        alarm(10);
        Timer* t = (Timer*)malloc(sizeof(Timer));
        while(1){
                init(t,flag);
                for (i=1; i <= 10; i++)
                        time_flow(i, t);

                print_record(t);
                if(flag){
                        puts("\nConnecting to an unstable parallel world");
                        read(0, buf, 0x5);
                        printf(&buf);
                        flag = 0;
                }
        }
        return 0;
}



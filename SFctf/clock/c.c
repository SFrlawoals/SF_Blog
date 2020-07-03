#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define _CRT_SECURE_NO_WARNINGS
#pragma warning (disable:4996)
int* world = NULL;
//int count = 0;
//R* last;

typedef struct record { //real timeinfo
	char d[0x8];
	char *data;
	time_t save;
}r;
typedef struct RECORD {
	char d[0x8];
	struct record* r;
	struct RECORD* prev;
}R;

typedef struct time_list
{
	int count;
	time_t current;
	R* last;
}tl;

tl* time_list;

void comment(int flag);
void manual();
void show_time();
int alarm();
void world_time(time_t* tmp, int* flag);
void snap_shot();
void clock_back(time_t* tmp);
//void lucky_number(time_t current);

tl* new_time_list()
{
	tl* n;

	n = (tl*)malloc( sizeof(tl) );
	n->count = 0;
	n->current = time(0);
	n->last = NULL;

	return n;
}

R *new_record(char *data)
{
	R* n;

	n = (R*)malloc(sizeof(R));

	n->prev = NULL;
	n->r = (r*)malloc(sizeof(r));
	n->r->data = (char *)malloc(0x20);
	strcpy(n->r->data, data);

	n->r->save = time_list->current;
	time_list->count++;

	return n;
}

void print_list()
{
	R* ptr;

	ptr = time_list->last;
	while (ptr != NULL)
	{
		printf("data : %s\n", ptr->r->data);
		ptr = ptr->prev;
	}
}
int main() {
	time_t tmp=0;
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	time_list = new_time_list();
	time_list->last = new_record("Welcome");
	
	int sel, flag = 0,TF =1;
	while (TF) {
		time_list->current = time(0) - tmp;
		puts("");
		show_time();
		comment(flag);
		
		printf(">> ");
		scanf("%d", &sel);
		switch (sel){
		case 1:
			TF = alarm(); break;
		case 2:
			world_time(&tmp,&flag); break;
		case 3:
			snap_shot(); break;
		case 4:
			if (time_list->count != 0 ) clock_back(&tmp);
			else puts("No data");
			break;
		case 5:
			break;
			//lucky_number(); break;
		case 6:
			return 0;
		default:
			break;
		}
		//print_list();
	}

}

void comment(int flag) {

	puts("==================\n      M E N U      \n==================");
	puts("1. Alarm");
	puts("2. World time");
	puts("3. Snap shot");
	puts("4. Clock back");
	puts("5. Lucky number");
	puts("6. exit");


}
void show_time() {
	struct tm* t = localtime(&time_list->current);
	printf("%d-%d-%d ", 1900 + t->tm_year, t->tm_mon + 1, t->tm_mday);
	printf("%d:%d:%d\n", t->tm_hour, t->tm_min, t->tm_sec);
}
int alarm() {
	int sec;
	printf("input(second): ");
	scanf("%d", &sec);
	puts("Sleep...");
	sleep(sec);
	puts("Wake up !!!");
	return 0;
}
void world_time(time_t* tmp, int* flag) {
	int num = 0;
	if (tmp == NULL) return 0;
	else {
		printf("Longitude(-180~180): ");
		scanf("%d", &num);
		*tmp += ((int)num/15)*3600;
	}
}
void snap_shot() {
	char tmp[0x21];
	R* n;
	printf("comment(20): ");
	getchar();
	//gets(tmp);
	read(0,&tmp,0x20);
	
	n = new_record(tmp);
	n->prev = time_list->last;
	time_list->last = n;
	
	printf("Saving on %d ...", time_list->count - 1);
	puts("saved !!!");
}
void clock_back(time_t* tmp) {
	int num, i;
	R* ptr;
	printf("Input num: ");
	scanf("%d", &num);
	if (num<0 || num>time_list->count) {
		puts("No data");
		return 0;
	}

	ptr = time_list->last;
	for (i = 0; i < time_list->count - num-1; i++)
		ptr = ptr->prev;

	printf("tic... toc !!!\n");
	sleep(1);

	printf("memo: %s", ptr->r->data);
	printf("[%p]\n",ptr->r->data);

	*tmp += time_list->current - ptr->r->save;
	
	free(ptr->r->data);
//	free(ptr->r);
//	time_list->count--;	
}
/*
void lucky_number(time_t current) {
	int num = 0;
	char tmp[21];
	srand(current);
	num = rand() % 45;

	if (num == 7) {
		printf("You are lucky to pick 7 !!!\n");
		printf("How do you feel?\n>> ");
		scanf("%s", tmp);
	}
	else printf("Your lucky number is %d !!!\n", num);
}
*/
void manual() {
	puts("");
	puts("┌─────────────────────  << NOTICE >> ────────────────────┐");
	puts("│ 1.Enter the longitude of the country you want          │");
	puts("│  * Note that 180W is represented by -180               │");

	puts("└────────────────────────────────────────────────────────┘");
	puts("");


}

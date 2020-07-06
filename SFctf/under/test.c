#pragma warning(disable:4996)
#include <stdio.h>

void hunt( int*exp);
void level_up(int* exp, int *base_exp, int* re_quired, int* level);
void menu();

int main() {
	int n, exp=0,base_exp, level = 0, re_quired = 0;

	printf("Please Let Me Know Base EXP : ");
	scanf("%d", &base_exp);
	base_exp *= (level + 1);
	
	menu();

	for (;;) {
		scanf("%d", &n);
		if (n == 0) break;
		if (n == 1) {
			hunt(&exp); menu();
			re_quired = base_exp - exp;
		}
		else if (n == 2) {
			level_up(&exp, &base_exp, &re_quired, &level); menu();
		}
		else if (n == 3) {
			printf("REMAIN EXP FOR NEXT LEVEL : %d\n", re_quired);
			menu();
		}
		else {
			printf("BAD CHOICE\n"); break;
		}
	}
}
void menu()
{
	printf("<1. HUNT> <2. NOW_LEVEL> <3. REQUIRED_EXP>\n");
	printf(">> ");	
}
void hunt(int *exp) {
	int n;
	printf("HOW MUCH DID YOU HUNT? : ");
	scanf("%d", &n);
	*exp += n;	
	
}
void level_up(int* exp,int *base_exp,int* re_quired, int* level) {
	while (*exp >= *base_exp) {
		if (*exp >= * base_exp) {
			(*level)++; *exp = *exp - (*base_exp); *re_quired = *base_exp * 2 - *exp; *base_exp *= 2;	
		}
	}
	printf("CURRENT_LEVEL : %d\n", *level);
}

#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef struct pizza
{
	char *ing[8];
	char name[0x30];
} pizza;

char *ing_table[0x8];
pizza *pizza_table[0x8];

void init()
{
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 2, 0);
}

void err_exit(char *buf)
{
	write(1, buf, strlen(buf));
	exit(-1);
}

void print_menu()
{
	printf("1. add ingredient\n");
	printf("2. make pizza\n");
	printf("3. eat pizza\n");
	printf("> ");
}

int read_data(char *buf, unsigned int len)
{
	int res;

	res = read(0, buf, len);
	if ( res > 0 )
		buf[res-1] = '\x00';

	return res;
}

int read_int()
{
	char buf[0x8];
	int res;

	read_data(buf, 0x8);
	res = atol(buf);

	return res;	
}

void add_ing()
{
	int i, tidx;

	tidx = -1;
	for ( i = 0; i < 8; i++ )
		if ( ing_table[i] == 0 )
		{
			tidx = i;
			break;
		}
	if ( tidx == -1 )
	{
		printf("full! :(\n");
		return;
	}

	ing_table[tidx] = malloc(0x28);
	if ( ing_table[tidx] == 0 )
		err_exit("alloc failed :(\n");
	printf("ingredient name : ");
	read_data(ing_table[tidx], 0x20);

	printf("success!\n");
}

void make_pizza()
{
	int i, tidx, ting;
	
	tidx = -1;
	for ( i = 0; i < 8; i++ )
		if ( pizza_table[i] == 0 )
		{
			tidx = i;
			break;
		}
	if ( tidx == -1 )
	{
		printf("full! :(\n");
		return;
	}

	pizza_table[tidx] = malloc(0x88);
	if ( pizza_table[tidx] == 0 )
		err_exit("alloc failed :(\n");
	memset(pizza_table[tidx], 0, 0x40);
	for ( i = 0; i < 8; i++ )
	{
		printf("ing %d : ", i);
		ting = read_int();
		if ( ting < 0 || ting >= 8 )
			err_exit("oob :(\n");
		if ( ing_table[ting] == 0 )
			err_exit("no such ingredient :(\n");

		pizza_table[tidx]->ing[i] = ing_table[ting];
	}
	printf("name : ");
	read_data(pizza_table[tidx]->name, 0x30);
}

void angry_mario(pizza *p)
{
	int i;
	char *target_ing;

	target_ing = 0;
	for ( i = 0; i < 8; i++ )
		if ( p->ing[i] != 0 && strcmp(p->ing[i], "pineapple") != 0 )
		{
			target_ing = p->ing[i];
			break;
		}
	if ( target_ing == 0 )
		err_exit("i never admit only pineapple pizza.\ngetout !\n");
	
	for ( i = 0; i <= 8; i++ )
		if ( p->ing[i] != 0 && strcmp(p->ing[i], "pineapple") == 0 )
			memcpy(p->ing[i], target_ing, 0x20);
	printf("garbage pizza changed  :(\n");
}

void eat_pizza()
{
	int tpizza, i, cnt;
	pizza *p;
	
	printf("eat : ");
	tpizza = read_int();
	if ( tpizza < 0 || tpizza >= 8 )
		err_exit("oob :(\n");
	if ( pizza_table[tpizza] == 0 )
		err_exit("no such pizza :(\n");
	
	p = pizza_table[tpizza];
	
	cnt = 0;
	for ( i = 0; i < 8; i++ )
		if ( p->ing[i] != 0 && strcmp(p->ing[i], "pineapple") == 0 )
			cnt++;
	if ( cnt >= 1 )
		angry_mario(p);
	else
	{
		free(p);
		pizza_table[tpizza] = 0;
		printf("yummy!\n");
	}
}

int main()
{
	int choice;

	init();
	printf("Welcome to Mario's Pizza\n");
	printf("How can i help you?\n");
	while ( 1 )
	{
		print_menu();	
		choice = read_int();
		switch ( choice )
		{
			case 1:
				add_ing();
				break;
			case 2:
				make_pizza();
				break;
			case 3:
				eat_pizza();
				break;
			default:
				err_exit("you fool?\n");
		}
	}

	return 0;
}

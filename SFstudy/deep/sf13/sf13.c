// gcc -Wl,-z,relro,-z,now -fPIE -pie -o sf13 sf13.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>

unsigned int err_cnt;
char *alloc_table[0x10];

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

void err_exit(char *msg)
{
	write(1, msg, strlen(msg));
	exit(-1);
}

void read_data(char *buf, int len)
{
	int res;

	res = read(0, buf, len);
	if ( res <= 0 )
		if ( err_cnt >= 3 )
			err_exit("read err :(\n");
		else
			err_cnt++;
	if ( res > 0 && buf[res-1] == '\n' )
		buf[res-1] = '\x00';
}

long long read_int64()
{
	long long res;
	char buf[0x10];

	res = read(0, buf, 0x10);
	if ( res <= 0 ) 
		if ( err_cnt >= 3 )
			err_exit("read err :(\n");
		else
			err_cnt++;
	if ( res > 0 && buf[res-1] == '\n' )
		buf[res-1] = '\x00';
	res = atoll(buf);
	return res;
}

void print_menu()
{
	printf("\n");
	printf("SF Allocator\n");
	printf("1. alloc\n");
	printf("2. delete\n");
	printf("3. show\n");
	printf("4. exit\n");
	printf("> ");
}

void alloc()
{
	long long size;
	unsigned int j, len;
	char choice[0x8];
	char *tmp_buf, *i, *ptr;

	printf("size : ");
	size = read_int64();
	tmp_buf = calloc(1, size);

	printf("you can alloc multiple datas at once\n");
	printf("example input : aaa;bb;ccccc\n");
	printf("datas : ");
	read_data(tmp_buf, size);

	for ( i = strtok(tmp_buf, ";") ; i ; i = strtok(0, ";") )
	{
		printf("target data : %s\n", i);
		printf("want alloc?(y/n) ");
		read_data(choice, 0x2);
		if ( *choice == 'y' || *choice == 'Y' )
		{
			for ( j = 0; j < 0x10; j++ )
				if ( alloc_table[j] == 0 )
				{
					printf("size : ");
					len = read_int64();
					if ( len < strlen( i ) )
						err_exit("overflow :(\n");
					ptr = malloc( len );
					if ( ptr == 0 )
						err_exit("malloc failed :(\n");
					memset(ptr, 0, len);
					strncpy( ptr, i, len );
					alloc_table[j] = ptr;
					break;
				}

			if ( j == 0x10 )
				err_exit("full :(\n");
		}
	}
	
	printf("want free?(y/n) ");
	read_data(choice, 0x2);
	if ( *choice == 'y' || *choice == 'Y' )
		free(tmp_buf);

	printf("success!\n");
}

void delete()
{
	int idx;
	
	printf("index : ");
	idx = read_int64();

	if ( idx < 0 || idx >= 15 )
		err_exit("out of bounds :(\n");

	if ( alloc_table[idx] != 0 )
	{
		free(alloc_table[idx]);
		alloc_table[idx] = 0;
		printf("success!\n");
	}
	else
		err_exit("empty table :(\n");
}

void show()
{
	printf("not implemented :p\n");
}

void init()
{
	install_seccomp();
	setvbuf(stdout, 0, 2, 0);
	err_cnt = 0;
}

int main()
{
	int choice;

	init();
	while ( 1 )
	{
		print_menu();
		choice = read_int64();
		switch ( choice )
		{
			case 1:
				alloc();
				break;
			case 2:
				delete();
				break;
			case 3:
				show();
				break;
			case 4:
				printf("bye!\n");
				exit(0);
			default:
				err_exit("are you stupid? :(\n");
		}
	}
}

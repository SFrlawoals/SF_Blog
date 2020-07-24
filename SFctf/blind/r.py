from pwn import*
p=process('./e')
#p.recv(1)
tmp = u32(p.recv(4))
print(hex(tmp))
p.interactive()

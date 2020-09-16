from pwn import*

tmp = asm(shellcraft.open("/home/sf13/flag"))

print(str(tmp))

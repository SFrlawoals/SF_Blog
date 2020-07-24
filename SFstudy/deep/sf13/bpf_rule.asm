# THIS IS A SECCOMP BPF RULE FOR SF13 CHALL
A = arch
A == ARCH_X86_64 ? next : dead
A = sys_number
A >= 0x40000000 ? dead : next
A == read ? ok : next
A == write ? ok : next
A == open ? ok : next
A == close ? ok : next
A == dup2 ? ok : next
A == exit ? ok : next
A == exit_group ? ok : next
A == brk ? ok : next
A == mmap ? ok : next
A == mprotect ? ok : next
A == rt_sigreturn ? ok : dead
ok:
return ALLOW
dead:
return KILL

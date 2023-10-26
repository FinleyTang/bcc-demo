from bcc import BPF

prog = '''
    int kprobe__sys_clone(void *ctx){
        bpf_trace_printk("Hello");
        return 0;
    }
'''

BPF(text= prog).trace_print()


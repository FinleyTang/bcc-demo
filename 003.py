from bcc import BPF

BPF(text='int kprobe__do_sys_open(void *ctx) { bpf_trace_printk("Hello, World!\\n"); return 0; }').trace_print()

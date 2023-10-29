#!/usr/bin/python3

from bcc import BPF
import argparse

# BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>

int trace_exec(struct pt_regs *ctx) {
    char comm[16];
    bpf_get_current_comm(&comm, sizeof(comm));
    char cmd[256];
    bpf_probe_read_user_str(&cmd, sizeof(cmd), (void *)PT_REGS_PARM1(ctx));
    
    bpf_trace_printk("Command executed by PID %d (comm %s): %s\\n", bpf_get_current_pid_tgid() >> 32, comm, cmd);
    return 0;
};
"""

# Parse command line arguments
parser = argparse.ArgumentParser(description="Monitor command execution using eBPF")
args = parser.parse_args()

# Load the BPF program
bpf = BPF(text=bpf_text)

# Attach the BPF program to the 'execve' syscall
bpf.attach_kprobe(event=bpf.get_syscall_fnname("execve"), fn_name="trace_exec")

# Print trace messages as they occur
print("Monitoring command execution. Press Ctrl+C to exit.")
try:
    bpf.trace_print()
except KeyboardInterrupt:
    pass
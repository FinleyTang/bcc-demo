from bcc import BPF

# 编写eBPF程序
# program = """
# #include <uapi/linux/ptrace.h>
# #include <linux/sched.h>
#
# int trace_open(struct pt_regs *ctx)
# {
#     u32 pid = bpf_get_current_pid_tgid();
#     char comm[TASK_COMM_LEN];
#     bpf_get_current_comm(&comm, sizeof(comm));
#     char filename[256];
#     bpf_probe_read_user_str(&filename, sizeof(filename), (void *)PT_REGS_PARM1(ctx));
#     bpf_trace_printk("File opened by PID %d (%s): %s\\n", pid, comm, filename);
#     return 0;
# }
# """

prog2 = '''
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

int trace_open(struct pt_regs* ctx)
{
    u32 pid = bpf_get_current_pid_tgid();
    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));
    char filename[256];
    bpf_probe_read_user_str(&filename, sizeof(filename), (void *)PT_REGS_PARM2(ctx));
    bpf_trace_printk("File opened by PID: %d  process:%s filename: %s\\n", pid, comm, filename);
    return 0;
}
'''

# 创建BPF对象并加载程序
b = BPF(text=prog2)
b.attach_kprobe(event="do_sys_open", fn_name="trace_open")
# b.attach_kprobe(event="do_filp_open", fn_name="trace_open")
# b.attach_kprobe(event="do_sys_openat2", fn_name="trace_open")
# b.attach_kprobe(event="do_sys_openat", fn_name="trace_open")
# b.attach_kprobe(event="do_sys_open_execat", fn_name="trace_open")

# 打印结果
b.trace_print()

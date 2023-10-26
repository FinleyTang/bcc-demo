## setup
i'm using ubuntu 20.04
```
sudo apt-get install bpfcc-tools linux-headers-$(uname -r)
```

## 001 Hello World
```commandline
BPF(text='int kprobe__sys_clone(void *ctx) { bpf_trace_printk("Hello, World!\\n"); return 0; }').trace_print()
```


kprobe__sys_clone()： 这是通过kprobe进行内核函数动态跟踪的快捷方法。如果C语言函数名称以"kprobe__"作为前缀，则函数名其余部分则表示将要被跟踪的内核函数接口(名)

## 002 program format
```commandline
from bcc import BPF

prog = '''
    int kprobe__sys_clone(void *ctx){
        bpf_trace_printk("Hello");
        return 0;
    }
'''

BPF(text= prog).trace_print()

```


## 003 do_sys_open
要跟踪其他内核函数，你需要知道相应函数的名称。在Linux内核中，可以通过查看内核源代码或者相关文档来获取函数名称。

对于监控文件打开操作，你可以使用以下步骤来确定相应的内核函数名称：

了解文件打开的系统调用：文件打开操作通常使用系统调用进行，你可以查阅相关的系统调用文档，例如在Linux中，文件打开操作使用的是open()系统调用。

查找系统调用对应的内核函数：系统调用会在内核中找到对应的处理函数。你可以查看内核源代码中的系统调用表，根据系统调用号找到对应的处理函数。

跟踪内核函数：一旦找到了文件打开操作对应的内核函数，你可以使用kprobe进行动态跟踪。以文件打开操作为例，假设对应的内核函数为do_sys_open()，你可以使用kprobe来跟踪该函数，方法类似于kprobe__do_sys_open()。

请注意，对于特定的内核版本或不同的操作系统，函数名称可能会有所不同。因此，在具体情况下，请查阅相关的文档或者参考相应内核版本的源代码来获取准确的函数名称。
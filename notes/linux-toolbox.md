# Linux toolbox

## Key ideas

Seven packages cover the main ways a Linux box goes wrong: **processes, resources, network, DNS and system calls**.

| Package | Main commands | Use it to answer |
|---|---|---|
| **procps** | `ps`, `top`, `free`, `uptime`, `kill`, `pgrep`, `vmstat` | What's running? Who's eating CPU or memory? |
| **sysstat** | `iostat`, `mpstat`, `pidstat`, `sar` | Which resource is saturated over time: per CPU, disk, per process? |
| **iproute2** | `ip`, `ss` | Interfaces, IPs, routes, listening sockets. Replaces `ifconfig`, `route` and `netstat`. |
| **tcpdump** | `tcpdump` | What packets are actually on the wire? Are replies coming back? |
| **dnsutils** | `dig`, `nslookup` | What does this name resolve to, which server answered, what's the TTL? |
| **strace** | `strace` | What system calls is the program making? What's it stuck waiting on? |
| **python3** | `python3` | Scripting: quick tools during an incident. |

## Triage order for a slow or sick box

1. **Overloaded?** `uptime`, `top`
2. **Which resource?** `vmstat 1` → `iostat -x 1`, `mpstat -P ALL 1`
3. **Network?** `ip a`, `ss -s`, `dig`, `tcpdump`
4. **One process?** `pidstat 1` → `strace -p <pid>`

This follows Netflix's "Linux performance analysis in 60 seconds".

## Interview one-liners

| Question | Answer |
|---|---|
| Is the service listening on its port? | `ss -tlnp` |
| CPU is low but the app is slow | Check disk: `iostat -x 1` (look at `%util`, `await`) |
| App hangs with no logs | `strace -p <pid>` shows the syscall it's blocked in |
| Where does traffic to an IP go? | `ip route get <ip>` |
| Is it DNS? | `dig <name>` and compare with `dig @8.8.8.8 <name>` |
| Are packets leaving and replies coming back? | `tcpdump -i <iface> host <ip>` |

## Checking what's installed

| Command | Tells you |
|---|---|
| `command -v tcpdump` | Path of the command if it's on `$PATH`; prints nothing if not |
| `dpkg -l tcpdump` | Package status. A line starting `ii` means installed. |
| `dpkg -S /usr/bin/ss` | Which package owns a file (`ss` → iproute2) |
| `apt list --installed \| grep <name>` | Search installed packages |

A command can be missing even when `apt install` "finished": a typo or a missing package name in a long install line is easy to miss. Always verify.

## Finding help on any machine

- `man <command>`: full manual. Press `/` to search, `q` to quit.
- `apropos <keyword>`: find a command when you don't know its name.
- `<command> --help`: quick flag summary.

## Self-test

1. Which tool shows whether a port is listening? Which one shows packets?
2. A process hangs with no log output. What do I run first, and what am I looking for?
3. Name the 4 triage steps in order, with one command each.
4. Which package gives me `iostat`? What does it tell me that `top` doesn't?
5. Why run `apt update` before `apt install` in a fresh container?

## References

- [Brendan Gregg: Linux performance tools](https://www.brendangregg.com/linuxperf.html)
- [Netflix: Linux performance analysis in 60 seconds](https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55)
- [Julia Evans' zines](https://wizardzines.com/) (strace, tcpdump, DNS)

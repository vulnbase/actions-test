import re
import sys

def dump_pid(pid, perms='rw'):
    sys.stderr.write(f"PID = {pid}\n")
    with open("/proc/%d/maps" % pid, 'r') as maps_file:
        with open("/proc/%d/mem" % pid, 'rb', 0) as mem_file:
            for line in maps_file.readlines(): 
                m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r][-w])', line)
                if m.group(3) == perms: 
                    sys.stderr.write(f"  OK: {line}")
                    start = int(m.group(1), 16)
                    if start > 0xFFFFFFFFFFFF:
                        continue
                    end = int(m.group(2), 16)
                    mem_file.seek(start)
                    chunk = mem_file.read(end - start)
                    sys.stdout.buffer.write(chunk)
                else:
                    sys.stderr.write(f"PASS: {line}")

if __name__ == "__main__":
    dump_pid(int(sys.argv[1]))
import time
import subprocess
import psutil

def get_top_cpu_processes(sort_by='cpu', limit=5):
    processes = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    top_processes = sorted(processes, key=lambda x: x[2], reverse=True)[:limit]
    print(f"Top {limit} processes by {sort_by} usage:")
    for pid, name, cpu in top_processes:
        print(f"PID: {pid}, Name: {name}, CPU: {cpu}%")

def get_top_mem_processes(sort_by='mem', limit=5):
    processes = [(p.info['pid'], p.info['name'], p.info['memory_percent']) for p in psutil.process_iter(['pid', 'name', 'memory_percent'])]
    top_processes = sorted(processes, key=lambda x: x[2], reverse=True)[:limit]
    print(f"Top {limit} processes by {sort_by} usage:")
    for pid, name, mem in top_processes:
        print(f"PID: {pid}, Name: {name}, Memory: {mem}%")

def get_process_info(pid):
    try:
        p = psutil.Process(pid)
        print(f"Process info for PID {pid}:")
        print(f"Name: {p.name()}")
        print(f"Status: {p.status()}")
        print(f"CPU Usage: {p.cpu_percent()}%")
        print(f"Memory Usage: {p.memory_percent()}%")
        print(f"Threads: {p.num_threads()}")
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}")
def search_process(name=None, pid=None):
    if name:
        for p in psutil.process_iter(['pid', 'name']):
            if p.info['name'] == name:
                get_process_info(p.info['pid'])
    elif pid:
        get_process_info(pid)
    else:
        print("Please provide a process name or PID to search for.")

def kill_process(pid=None, name=None):
    if pid:
        try:
            p = psutil.Process(pid)
            p.terminate()
            print(f"Process with PID {pid} terminated.")
        except psutil.NoSuchProcess:
            print(f"No process found with PID {pid}")
    elif name:
        for p in psutil.process_iter(['pid', 'name']):
            if p.info['name'] == name:
                try:
                    psutil.Process(p.info['pid']).terminate()
                    print(f"Process with name {name} and PID {p.info['pid']} terminated.")
                except psutil.NoSuchProcess:
                    print(f"No process found with name {name}")
    else:
        print("Please provide a process PID or name to terminate.")

def monitor_process(pid=None, name=None, interval=5):
    while True:
        if pid:
            try:
                p = psutil.Process(pid)
                print(f"PID: {pid}, CPU Usage: {p.cpu_percent()}%, Memory Usage: {p.memory_percent()}%")
            except psutil.NoSuchProcess:
                print(f"No process found with PID {pid}")
        elif name:
            for p in psutil.process_iter(['pid', 'name']):
                if p.info['name'] == name:
                    try:
                        proc = psutil.Process(p.info['pid'])
                        print(f"Name: {name}, PID: {p.info['pid']}, CPU Usage: {proc.cpu_percent()}%, Memory Usage: {proc.memory_percent()}%")
                    except psutil.NoSuchProcess:
                        print(f"No process found with name {name}")
        else:
            print("Please provide a process PID or name to monitor.")
        time.sleep(interval)

if __name__ == "__main__":
    while True:
        print('\nchoose an options:')
        print('1. Get Top CPU Processes')
        print('2. Get top Memory Process')
        print('3. Get process Information')
        print('4. Search Process')
        print('5. Kill Process')
        print('6. Monitor Process')
        print('7. Exit')
        choice = input("Enter your choice:").strip()
        print(f"Your choice: '{choice}'") # Debug print to check the input
        
        if choice == "1.":
            get_top_cpu_processes()
        elif choice == "2.":
            get_top_mem_processes()
        elif choice == "3.": 
            pid = input("Enter the PID: ").strip()
        if pid.isdigit():
            get_process_info(int(pid))
        elif choice == "4.":
            name_or_pid = input("Enter the name or PID of the Process:").strip()
            if name_or_pid.isdigit():
                search_process(pid=(name_or_pid))
            else:
                search_process(name=(name_or_pid))
        elif choice == "5.":
            name_or_pid = input("Enter the name or PID of the Process:").strip()
            if name_or_pid.isdigit():
                kill_process(pid=(name_or_pid))
            else:
                kill_process(name=(name_or_pid))
            kill_process()
        elif choice == "6.":
           name_or_pid = input("Enter process name or PID: ").strip() 
           interval = input("Enter the monitoring interval in seconds: ").strip() 
           if name_or_pid.isdigit(): 
            if interval.isdigit(): 
                monitor_process(pid=int(name_or_pid), interval=int(interval))
            if name_or_pid.isdigit():
                monitor_process(pid=(name_or_pid), interval=interval)
            else:
                monitor_process(name=(name_or_pid), interval=interval)
        elif choice == '7':
            break
        else: 
            print("Invalid choice. Please try again.")
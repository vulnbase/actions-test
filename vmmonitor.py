from __future__ import print_function
from scapy.all import *
import time
from datetime import datetime
import random

__version__ = "0.0.3"

start_time = time.time()
hosts = {}
scan_queue = []
scan_ports = [5900]
log_level = 2

def log(msg, level=2):
    if level >= log_level:
        print(f"[{datetime.now().isoformat()}] ({int(time.time() - start_time)}) {msg}")

def check_port(address, port):
    pkt = sr1(IP(dst=address)/TCP(sport=random.randint(30000, 65535), dport=port, flags="S"), timeout=1, verbose=0)
    if pkt != None:
        if pkt.haslayer(TCP):
             if pkt[TCP].flags == 18:
                 return True
    return False


# Fixup function to extract dhcp_options by key
def get_option(dhcp_options, key):

    must_decode = ['hostname', 'domain', 'vendor_class_id']
    try:
        for i in dhcp_options:
            if i[0] == key:
                # If DHCP Server Returned multiple name servers
                # return all as comma seperated string.
                if key == 'name_server' and len(i) > 2:
                    return ",".join(i[1:])
                # domain and hostname are binary strings,
                # decode to unicode string before returning
                elif key in must_decode:
                    return i[1].decode()
                else:
                    return i[1]
    except:
        pass

def handle_dhcp_packet(packet):
    # Match DHCP discover
    if packet[DHCP].options[0][1] == 1:
        if not packet[Ether].src in hosts:
            hostname = get_option(packet[DHCP].options, 'hostname')
            if hostname is not None:
                log(f"New host {hostname} ({packet[Ether].src}) asked for an IP", level=1)
                hosts[packet[Ether].src] = {"hostname" : hostname, "address" : None}

def handle_arp_packet(packet):
    hwaddr = packet[ARP].hwsrc
    if hwaddr in hosts:
        # print(ARP(packet[ARP]).show())
        if str(packet[ARP].psrc).startswith("10."):
            if hosts[hwaddr]["address"] is None:
                hosts[hwaddr]["address"] = packet[ARP].psrc
                log(f"Address for {hosts[hwaddr]['hostname']} {packet[ARP].psrc}", level=1)
                scan_queue.append(hosts[hwaddr])

def handle_packet(packet):
    if ARP in packet:
        handle_arp_packet(packet)
    elif DHCP in packet:
        handle_dhcp_packet(packet)

def process():
    while True:
        if len(scan_queue):
            host = scan_queue.pop(0)
            results = []
            for port in scan_ports:
                results.append((port, check_port(host["address"], port)))

            log(f"{host['hostname']}[{host['address']}]:")
            for port, result in results:
                log(f"\t{host['address']}:{port} - {'Open' if result else 'Closed'}")
        time.sleep(0.4)

if __name__ == "__main__":
    t = AsyncSniffer(filter="(udp and (port 67 or 68)) or arp", prn=handle_packet, store=False)
    t.start()
    process()
    t.stop()

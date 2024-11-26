import os
import subprocess
from scapy.all import ARP, Ether, srp
import socket

def get_local_subnet():
    """
    Detecta la subred a la que está conectada la laptop.
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    subnet = local_ip.rsplit('.', 1)[0] + '.0/24'
    return subnet

def resolve_hostname(ip):
    """
    Realiza una consulta DNS inversa para resolver el nombre del host.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

def arp_scan(subnet):
    """
    Realiza un escaneo ARP en la subred especificada.
    """
    devices = []
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
    print(f"Enviando solicitud ARP en la subred: {subnet}")
    answered, _ = srp(arp_request, timeout=5, verbose=1)  # Aumenta el timeout

    for sent, received in answered:
        hostname = resolve_hostname(received.psrc)
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'hostname': hostname
        })
    return devices

def nmap_scan(subnet):
    """
    Realiza un escaneo utilizando nmap para obtener más detalles.
    """
    devices = []
    try:
        output = subprocess.check_output(["nmap", "-sn", subnet], universal_newlines=True)
        lines = output.split("\n")
        ip, mac = None, None
        for line in lines:
            if "Nmap scan report for" in line:
                ip = line.split()[-1]
            elif "MAC Address" in line:
                mac = line.split()[2]
                hostname = resolve_hostname(ip)
                devices.append({
                    'ip': ip,
                    'mac': mac,
                    'hostname': hostname
                })
    except subprocess.CalledProcessError:
        print("Error ejecutando nmap. Asegúrate de tenerlo instalado.")
    return devices

def discover_devices():
    """
    Detecta dispositivos en la red combinando escaneos ARP y Nmap.
    """
    subnet = get_local_subnet()
    print(f"Subred detectada: {subnet}")
    print(f"Realizando escaneo ARP en la subred: {subnet}")
    arp_devices = arp_scan(subnet)

    print(f"Realizando escaneo Nmap en la subred: {subnet}")
    nmap_devices = nmap_scan(subnet)

    # Unir resultados de ARP y Nmap
    all_devices = {dev['ip']: dev for dev in arp_devices}
    for dev in nmap_devices:
        if dev['ip'] not in all_devices:
            all_devices[dev['ip']] = dev
        else:
            all_devices[dev['ip']].update(dev)

    return list(all_devices.values())

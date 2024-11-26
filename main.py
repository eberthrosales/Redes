from discovery import discover_devices
from report import generate_report

def main():
    print("Iniciando reconocimiento de dispositivos en la red Wi-Fi...")
    devices = discover_devices()

    if devices:
        print(f"\nDispositivos encontrados: {len(devices)}\n")
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}, Nombre: {device['hostname'] or 'Desconocido'}")
        
        generate_report(devices)
        print("\nReporte generado exitosamente como 'device_report.csv'.")
    else:
        print("\nNo se encontraron dispositivos en la red.")

if __name__ == "__main__":
    main()

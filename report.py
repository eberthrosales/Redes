import csv

def generate_report(devices):
    """
    Genera un reporte en CSV con los dispositivos detectados.
    """
    with open('device_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['IP', 'MAC', 'Nombre']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for device in devices:
            writer.writerow({
                'IP': device['ip'],
                'MAC': device['mac'],
                'Nombre': device['hostname'] or 'Desconocido'
            })

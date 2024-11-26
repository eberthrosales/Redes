import pandas as pd
import matplotlib.pyplot as plt

def generate_report(data):
    # Convertir datos a DataFrame
    df = pd.DataFrame(data)
    df.to_csv("device_report.csv", index=False)
    print("Reporte guardado como 'device_report.csv'.")

    # Gráfica de categorías
    category_counts = df['Categoría'].value_counts()
    category_counts.plot(kind='bar', title='Dispositivos por Categoría', figsize=(8, 5))
    plt.ylabel('Cantidad')
    plt.xlabel('Categoría')
    plt.grid(axis='y')
    plt.show()

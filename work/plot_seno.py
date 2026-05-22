import matplotlib.pyplot as plt

table_x, table_y = [], []
signal_x, signal_y = [], []
section = None

with open("work/seno_data.csv") as f:
    for line in f:
        if line.startswith("# TABLE"):
            section = "table"
        elif line.startswith("# SIGNAL"):
            section = "signal"
        elif section == "table":
            i, v = line.strip().split(",")
            table_x.append(int(i)); table_y.append(float(v))
        elif section == "signal":
            i, v = line.strip().split(",")
            signal_x.append(int(i)); signal_y.append(float(v))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
fig.suptitle('Instrumento Seno: síntesis por búsqueda en tabla', fontweight='bold')

ax1.plot(table_x, table_y, 'o', color='steelblue', markersize=7)
ax1.set_title(f'Tabla almacenada ({len(table_x)} muestras, un período de seno)')
ax1.set_xlabel('Índice i'); ax1.set_ylabel('tbl[i]')
ax1.axhline(0, color='gray', lw=0.7); ax1.grid(True, alpha=0.3)

ax2.plot(signal_x, signal_y, '.', color='tomato', markersize=8)
ax2.set_title('Primera trama de señal generada (interpolación lineal)')
ax2.set_xlabel('Muestra'); ax2.set_ylabel('Amplitud')
ax2.axhline(0, color='gray', lw=0.7); ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('work/seno_tabla.png', dpi=150, bbox_inches='tight')
print("Gráfica guardada en work/seno_tabla.png")
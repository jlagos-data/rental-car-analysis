import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

#Conexion
conn = sqlite3.connect('rent_of_carv1.db')
df = pd.read_sql_query("SELECT * FROM reporte_tarifas", conn)   
conn.close()

df['pct_ocupacion'] = (df['ocupacion_del_dia'] / df['capacidad_total']) * 100

#RevPar (precio final dividido por capacidad del dia)
ingreso_diario = df.groupby(['fecha_recogida', 'categoria', 'capacidad_total'])['precio_final'].sum().reset_index()
ingreso_diario['revpar'] = ingreso_diario['precio_final'] / ingreso_diario['capacidad_total']

#ordenar los meses para los graficos
orden_meses = ['enero', 'febrero', 'marzo', 'abril', 
               'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

df['mes'] = pd.Categorical(df['mes'], categories=orden_meses, ordered=True)

#ingresos vs ocupacion mensual

resumen_mensual = df.groupby(['mes']).agg({
    'precio_final': 'sum',
    'pct_ocupacion': 'mean',
}).reset_index()

sns.set_style("whitegrid")
sns.set_palette("muted")

color_barras = "#2c3e50"    # azul petróleo
color_linea  = "#e74c3c"    # rojo carmesí
#graficos
fig, ax1 = plt.subplots(figsize=(12, 6))

#Barras de ingresos
sns.barplot(data=resumen_mensual, x='mes', y='precio_final', 
            color=color_barras, ax=ax1, alpha=0.8,
            edgecolor=None) 
ax1.set_ylabel('Ingresos totales (USD)', color=color_barras, fontsize=12)
ax1.set_yticks(range(0, int(resumen_mensual['precio_final'].max())+2000, 2000))
ax1.tick_params(axis='y', labelcolor=color_barras, labelsize=10)

#ocupacion %
ax2 = ax1.twinx()
sns.lineplot(data=resumen_mensual, x='mes', y='pct_ocupacion', 
             marker='o', color=color_linea, ax=ax2, linewidth=2, ci=None)
ax2.set_ylabel('Ocupacion Promedio (%)', color=color_linea, fontsize=12)
ax2.set_ylim(0, 110)
ax2.set_yticks(range(0, 110, 10))
ax2.tick_params(axis='y', labelcolor=color_linea, labelsize=10)


plt.title('Relacion ingresos totales vs (%) de ocupacion por mes', fontsize=16, fontweight='bold')
ax1.set_xticklabels(orden_meses, rotation=45)
plt.tight_layout()
plt.show()

#Analisis RevPar
#agrupamos por fecha y categoria para tener el ingreso diario real
daily_stats = df.groupby(['fecha_recogida', 'mes', 'categoria']).agg({
    'precio_final': 'sum',
    'capacidad_total': 'max'
}).reset_index()

#calculamos el revpar diario
daily_stats['revpar_diario'] = daily_stats['precio_final'] / daily_stats['capacidad_total']

#promediamos por mes para el grafico
revpar_mensual = daily_stats.groupby(['mes', 'categoria'])['revpar_diario'].mean().reset_index()


#grafico evolucion de rentabilidad (revpar)
plt.figure(figsize=(12, 6))
sns.lineplot(data=revpar_mensual, x='mes', y='revpar_diario', hue='categoria', ci=None, marker='o', linewidth=2.5)
plt.title('Rentabilidad por unidad (RevPar) a lo largo de 2025', fontsize=14, fontweight='bold')
plt.ylabel('USD por auto disponible (diario)', fontsize=12)
plt.xlabel('Mes', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(title='Categoria de vehiculo', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(range(0, 15, 1))
plt.tight_layout()
plt.show()


#Conteo de escasez critica
#agregamos la ocupacion al daily_stats
daily_stats = df.groupby(['fecha_recogida', 'mes', 'categoria']).agg({
    'precio_final': 'sum',
    'capacidad_total': 'max',
    'ocupacion_del_dia': 'max'
}).reset_index()

#Definimos un 90% de ocupacion como escasez critica
daily_stats['escasez_critica'] = daily_stats['ocupacion_del_dia'] >= (0.9 * daily_stats['capacidad_total'])

#contamos cuantos dias ocurrio esto por mes y catergoria
conteo_escasez = daily_stats[daily_stats['escasez_critica'] == True].groupby(['mes', 'categoria']).size().unstack().fillna(0)

#grafico mapa de calor
plt.figure(figsize=(12, 6))
sns.heatmap(conteo_escasez.reindex(orden_meses), annot=True, cmap='YlOrRd', fmt='g')

plt.title('Dias por mes con escasez critica (ocupacion >= 90%)', fontsize=14, fontweight='bold')
plt.ylabel('mes', fontsize=12)
plt.xlabel('categoria', fontsize=12)
plt.show()

dias_escasez = daily_stats[daily_stats['escasez_critica'] == True]
ingreso_real_escasez = dias_escasez['precio_final'].sum()

#Simulamos un aumento de 10% (multiplicador de escasez critica)
#Estimamos que si hubieramos cobrado un 10% adicional, las personas igual habrian alquilado (por ser escasez)
ingreso_potencial = ingreso_real_escasez['precio_final'] * 1.10
ganancia_perdida = ingreso_potencial - ingreso_real_escasez

print(" ANALISIS DE OPORTUNIDAD ")
print(f"Ingreso total en días de escasez: ${ingreso_real_escasez:,.2f}")
print(f"Ganancia adicional estimada (con +10% de precio): ${ganancia_perdida:,.2f}")
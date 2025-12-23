import pandas as pd
import numpy as np
import datetime
import sqlite3

#Precios base de los vehiculos
precios_base={
    'Economico': 50,
    'Intermedio': 65,
    'Camioneta': 85
}

# capacidad total de nuestra empresa
stock_categoria = {
    'Economico': 80,
    'Intermedio': 60,
    'Camioneta': 40
}

#Multiplicadores de estacionalidad
multiplicador_temporada={
    'alta': 1.35,
    'baja':  0.80,
    'semana': 0.95,
    'fin de semana': 1.10
}

temp_alta = [2, 7, 8, 12]
temp_baja = [1, 5, 9, 10]

def calcular_multiplicador_estacionalidad(fecha):
    mes = fecha.month
    if mes in temp_alta:
        return multiplicador_temporada['alta']
    elif mes in temp_baja:
        return multiplicador_temporada['baja']
    else:
        dia_de_semana = fecha.weekday()
        if dia_de_semana < 4:
            return multiplicador_temporada['semana']
        else:
            return multiplicador_temporada['fin de semana']
        

def calcular_multiplicador_antelacion(dias_antelacion):
    if dias_antelacion < 7:
        return 1.10
    elif 7 <= dias_antelacion < 21:
        return 0.90
    else:
        return 1
    

#calendario simulado
fechas = pd.date_range(start='2025-01-01', end='2025-12-15', freq='D') 
numero_registros = 4000
fechas_aleatorias = np.random.choice(fechas, numero_registros)


#dataframe con los precios de los vehiculos diario
df = pd.DataFrame({
    'fecha_recogida': fechas_aleatorias,
    # categoria al azar para cada dia
    'categoria': np.random.choice(list(precios_base.keys()), len(fechas_aleatorias)),
    #generar antelacion (dias 1 a 30)
    'reserva_antelacion': np.random.randint(1, 30, len(fechas_aleatorias))
})

#Logica de inventario consistente
pizarra_inventario = df[['fecha_recogida', 'categoria']].drop_duplicates()


df['mes']= df['fecha_recogida'].dt.month
#diccionario traductor de meses
meses_nombres = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
    7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
}
df['mes'] = df['mes'].map(meses_nombres)
df['precios_base']= df['categoria'].map(precios_base)
df['multiplicador_estacionalidad'] = df['fecha_recogida'].apply(calcular_multiplicador_estacionalidad)
df['multiplicador_antelacion'] = df['reserva_antelacion'].apply(calcular_multiplicador_antelacion)

# Asignar capacidad y ocupacion fija a cada fila de la pizarra
pizarra_inventario['capacidad_total'] = pizarra_inventario['categoria'].map(stock_categoria)
pizarra_inventario['ocupacion_del_dia'] = pizarra_inventario['capacidad_total'].apply(lambda x: np.random.randint(int(x*0.5), x + 1))
df = pd.merge(df, pizarra_inventario, on=['fecha_recogida', 'categoria'], how='left')

# Asignnar disponibilidad restante
df['disponibilidad_restante'] = df['capacidad_total'] - df['ocupacion_del_dia']

df['precio_final'] = (df['precios_base'] * df['multiplicador_estacionalidad'] * df['multiplicador_antelacion']).round(2)

#verificacion de valores nulos
nulos = df.isnull().sum().sum()
if (nulos == 0):
    print('No hay valores nulos en el dataframe')
else:
    print(f'Hay {nulos} valores nulos en el dataframe')

#Eliminacion de duplicados
filas_antes= len(df)
df = df.drop_duplicates()
filas_despues = len(df)
print(f'Eliminados {filas_antes - filas_despues} duplicados')

#orden de las columnas
nuevo_orden = [
    'fecha_recogida', 
    'mes', 
    'categoria', 
    'reserva_antelacion', 
    'capacidad_total', 
    'ocupacion_del_dia', 
    'disponibilidad_restante',
    'precios_base', 
    'multiplicador_estacionalidad', 
    'multiplicador_antelacion', 
    'precio_final'
]
df = df[nuevo_orden].copy()
#Ordenar el dataframe por fecha
df = df.sort_values('fecha_recogida')

#exportacion de los datos

#formato csv
df.to_csv('reporte_tarifas.csv', encoding='utf-8', index=False)

#formato sql
conexion=sqlite3.connect('rent_of_carv1.db')

df.to_sql('reporte_tarifas', conexion, if_exists='replace', index=False)

conexion.close()
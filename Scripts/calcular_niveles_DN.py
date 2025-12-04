"""
Script para calcular niveles según metodología DN (Día Normal)
Versión: 1.1 - 2025-12-04 19:55
Cambios: Añadidos cálculos Three Days según calculosDN.md líneas 29-53
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calcular_niveles_DN.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rutas
INPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/Datos_Diarios_por_Año.xlsx")
OUTPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/Datos_Diarios_DN_Niveles.xlsx")

def cargar_datos_diarios():
    """Carga todos los años de datos diarios"""
    logger.info("Cargando datos diarios...")

    xl = pd.ExcelFile(INPUT_FILE)
    hojas_años = [h for h in xl.sheet_names if h not in ['RESUMEN']]

    dfs = []
    for hoja in hojas_años:
        df = pd.read_excel(xl, hoja)
        dfs.append(df)

    df_completo = pd.concat(dfs, ignore_index=True)
    df_completo['Date'] = pd.to_datetime(df_completo['Date'])
    df_completo = df_completo.sort_values('Date').reset_index(drop=True)

    logger.info(f"Datos cargados: {len(df_completo)} registros de {df_completo['Date'].min()} a {df_completo['Date'].max()}")
    return df_completo

def calcular_niveles_DN_oneday(df):
    """
    Calcula niveles según metodología DN - One Day
    Según calculosDN.md líneas 3-27
    """
    logger.info("Calculando niveles DN One Day...")

    # Inicializar columnas
    df['Q1'] = np.nan
    df['Q4'] = np.nan
    df['Range'] = np.nan
    df['Half_Range'] = np.nan
    df['NR2'] = np.nan
    df['Z2H'] = np.nan
    df['Z2L'] = np.nan
    df['Z3H'] = np.nan
    df['Z3L'] = np.nan
    df['TCH'] = np.nan
    df['TCL'] = np.nan
    df['TVH'] = np.nan
    df['TVL'] = np.nan
    df['Std1'] = np.nan
    df['Std2'] = np.nan
    df['Std3'] = np.nan
    df['Std4'] = np.nan
    df['Std5'] = np.nan
    df['Std1_neg'] = np.nan
    df['Std2_neg'] = np.nan
    df['Std3_neg'] = np.nan
    df['Std4_neg'] = np.nan
    df['Std5_neg'] = np.nan
    df['1D_pos'] = np.nan
    df['1D_neg'] = np.nan

    # Calcular desde el segundo día (necesitamos el día anterior)
    for i in range(1, len(df)):
        # Q1 y Q4 del día anterior (ONE DAY)
        Q1 = df.loc[i-1, 'High']
        Q4 = df.loc[i-1, 'Low']

        # Range
        range_val = Q1 - Q4
        half_range = range_val / 2

        # NR2 (Nivel de Referencia 2)
        NR2 = Q1 - half_range

        # Niveles según calculosDN.md
        Z2H = NR2 + (range_val * 0.159)
        Z2L = NR2 + (range_val * 0.125)
        Z3H = NR2 - (range_val * 0.125)
        Z3L = NR2 - (range_val * 0.159)

        TCH = Q1 - (range_val * 0.125)
        TCL = Q1 - (range_val * 0.159)
        TVH = Q4 + (range_val * 0.159)
        TVL = Q4 + (range_val * 0.125)

        # Desviaciones estándar por encima de Q1
        Std1 = Q1 + (range_val * 0.125)
        Std2 = Q1 + (range_val * 0.159)
        Std3 = Q1 + (range_val * 0.25)
        Std4 = Q1 + (range_val * 0.341)
        Std5 = Q1 + (range_val * 0.375)

        # Desviaciones estándar por debajo de Q4
        Std1_neg = Q4 - (range_val * 0.125)
        Std2_neg = Q4 - (range_val * 0.159)
        Std3_neg = Q4 - (range_val * 0.25)
        Std4_neg = Q4 - (range_val * 0.341)
        Std5_neg = Q4 - (range_val * 0.375)

        # 1D+ y 1D-
        OneD_pos = Q1 + half_range
        OneD_neg = Q4 - half_range

        # Guardar en DataFrame
        df.loc[i, 'Q1'] = Q1
        df.loc[i, 'Q4'] = Q4
        df.loc[i, 'Range'] = range_val
        df.loc[i, 'Half_Range'] = half_range
        df.loc[i, 'NR2'] = NR2
        df.loc[i, 'Z2H'] = Z2H
        df.loc[i, 'Z2L'] = Z2L
        df.loc[i, 'Z3H'] = Z3H
        df.loc[i, 'Z3L'] = Z3L
        df.loc[i, 'TCH'] = TCH
        df.loc[i, 'TCL'] = TCL
        df.loc[i, 'TVH'] = TVH
        df.loc[i, 'TVL'] = TVL
        df.loc[i, 'Std1'] = Std1
        df.loc[i, 'Std2'] = Std2
        df.loc[i, 'Std3'] = Std3
        df.loc[i, 'Std4'] = Std4
        df.loc[i, 'Std5'] = Std5
        df.loc[i, 'Std1_neg'] = Std1_neg
        df.loc[i, 'Std2_neg'] = Std2_neg
        df.loc[i, 'Std3_neg'] = Std3_neg
        df.loc[i, 'Std4_neg'] = Std4_neg
        df.loc[i, 'Std5_neg'] = Std5_neg
        df.loc[i, '1D_pos'] = OneD_pos
        df.loc[i, '1D_neg'] = OneD_neg

    logger.info(f"Niveles DN One Day calculados para {len(df)-1} días")
    return df

def calcular_niveles_DN_threedays(df):
    """
    Calcula niveles según metodología DN - Three Days
    Según calculosDN.md líneas 29-53
    """
    logger.info("Calculando niveles DN Three Days...")

    # Inicializar columnas con sufijo _3D
    df['Q1_3D'] = np.nan
    df['Q4_3D'] = np.nan
    df['Range_3D'] = np.nan
    df['High_3D'] = np.nan
    df['Low_3D'] = np.nan
    df['Half_Range_3D'] = np.nan
    df['NR2_3D'] = np.nan
    df['Z2H_3D'] = np.nan
    df['Z2L_3D'] = np.nan
    df['Z3H_3D'] = np.nan
    df['Z3L_3D'] = np.nan
    df['TCH_3D'] = np.nan
    df['TCL_3D'] = np.nan
    df['TVH_3D'] = np.nan
    df['TVL_3D'] = np.nan
    df['Std1_3D'] = np.nan
    df['Std2_3D'] = np.nan
    df['Std3_3D'] = np.nan
    df['Std4_3D'] = np.nan
    df['Std5_3D'] = np.nan
    df['Std1_neg_3D'] = np.nan
    df['Std2_neg_3D'] = np.nan
    df['Std3_neg_3D'] = np.nan
    df['Std4_neg_3D'] = np.nan
    df['Std5_neg_3D'] = np.nan
    df['1D_pos_3D'] = np.nan
    df['1D_neg_3D'] = np.nan

    # Calcular desde el cuarto día (necesitamos 3 días anteriores)
    for i in range(3, len(df)):
        # High y Low de los últimos 3 días
        High_3D = df.loc[i-3:i-1, 'High'].max()
        Low_3D = df.loc[i-3:i-1, 'Low'].min()

        # Range de 3 días
        range_3d = High_3D - Low_3D
        half_range_3d = range_3d / 2

        # NR2 = Q1 - half_range (según línea 37 de calculosDN.md)
        # Pero primero necesitamos Q1, que es NR2 + half_range (línea 31)
        # Esto significa que NR2 es el punto medio entre High_3D y Low_3D
        NR2_3D = Low_3D + half_range_3d

        # Q1 y Q4 según líneas 31-32
        Q1_3D = NR2_3D + half_range_3d
        Q4_3D = NR2_3D - half_range_3d

        # Niveles según calculosDN.md (idénticos a One Day pero con range_3d)
        Z2H_3D = NR2_3D + (range_3d * 0.159)
        Z2L_3D = NR2_3D + (range_3d * 0.125)
        Z3H_3D = NR2_3D - (range_3d * 0.125)
        Z3L_3D = NR2_3D - (range_3d * 0.159)

        TCH_3D = Q1_3D - (range_3d * 0.125)
        TCL_3D = Q1_3D - (range_3d * 0.159)
        TVH_3D = Q4_3D + (range_3d * 0.159)
        TVL_3D = Q4_3D + (range_3d * 0.125)

        # Desviaciones estándar
        Std1_3D = Q1_3D + (range_3d * 0.125)
        Std2_3D = Q1_3D + (range_3d * 0.159)
        Std3_3D = Q1_3D + (range_3d * 0.25)
        Std4_3D = Q1_3D + (range_3d * 0.341)
        Std5_3D = Q1_3D + (range_3d * 0.375)

        Std1_neg_3D = Q4_3D - (range_3d * 0.125)
        Std2_neg_3D = Q4_3D - (range_3d * 0.159)
        Std3_neg_3D = Q4_3D - (range_3d * 0.25)
        Std4_neg_3D = Q4_3D - (range_3d * 0.341)
        Std5_neg_3D = Q4_3D - (range_3d * 0.375)

        # 1D+ y 1D-
        OneD_pos_3D = Q1_3D + half_range_3d
        OneD_neg_3D = Q4_3D - half_range_3d

        # Guardar en DataFrame
        df.loc[i, 'High_3D'] = High_3D
        df.loc[i, 'Low_3D'] = Low_3D
        df.loc[i, 'Q1_3D'] = Q1_3D
        df.loc[i, 'Q4_3D'] = Q4_3D
        df.loc[i, 'Range_3D'] = range_3d
        df.loc[i, 'Half_Range_3D'] = half_range_3d
        df.loc[i, 'NR2_3D'] = NR2_3D
        df.loc[i, 'Z2H_3D'] = Z2H_3D
        df.loc[i, 'Z2L_3D'] = Z2L_3D
        df.loc[i, 'Z3H_3D'] = Z3H_3D
        df.loc[i, 'Z3L_3D'] = Z3L_3D
        df.loc[i, 'TCH_3D'] = TCH_3D
        df.loc[i, 'TCL_3D'] = TCL_3D
        df.loc[i, 'TVH_3D'] = TVH_3D
        df.loc[i, 'TVL_3D'] = TVL_3D
        df.loc[i, 'Std1_3D'] = Std1_3D
        df.loc[i, 'Std2_3D'] = Std2_3D
        df.loc[i, 'Std3_3D'] = Std3_3D
        df.loc[i, 'Std4_3D'] = Std4_3D
        df.loc[i, 'Std5_3D'] = Std5_3D
        df.loc[i, 'Std1_neg_3D'] = Std1_neg_3D
        df.loc[i, 'Std2_neg_3D'] = Std2_neg_3D
        df.loc[i, 'Std3_neg_3D'] = Std3_neg_3D
        df.loc[i, 'Std4_neg_3D'] = Std4_neg_3D
        df.loc[i, 'Std5_neg_3D'] = Std5_neg_3D
        df.loc[i, '1D_pos_3D'] = OneD_pos_3D
        df.loc[i, '1D_neg_3D'] = OneD_neg_3D

    logger.info(f"Niveles DN Three Days calculados para {len(df)-3} días")
    return df

def calcular_estadisticas_touches_3d(df):
    """Calcula estadísticas de toques en niveles Q1_3D y Q4_3D"""
    logger.info("Calculando estadísticas de toques Three Days...")

    df['Toca_Q1_3D'] = (df['High'] >= df['Q1_3D']) & pd.notna(df['Q1_3D'])
    df['Toca_Q4_3D'] = (df['Low'] <= df['Q4_3D']) & pd.notna(df['Q4_3D'])
    df['Toca_Q1_y_Q4_3D'] = df['Toca_Q1_3D'] & df['Toca_Q4_3D']
    df['Toca_solo_Q1_3D'] = df['Toca_Q1_3D'] & ~df['Toca_Q4_3D']
    df['Toca_solo_Q4_3D'] = ~df['Toca_Q1_3D'] & df['Toca_Q4_3D']

    df['Puntos_Sobre_Q1_3D'] = np.where(df['High'] > df['Q1_3D'], df['High'] - df['Q1_3D'], 0)
    df['Puntos_Bajo_Q4_3D'] = np.where(df['Low'] < df['Q4_3D'], df['Q4_3D'] - df['Low'], 0)

    return df

def calcular_estadisticas_cierres_3d(df):
    """Calcula estadísticas de cierres respecto a niveles 3D"""
    logger.info("Calculando estadísticas de cierres Three Days...")

    df['Q1_3D_Cierre_Debajo'] = (df['Close'] < df['Q1_3D']) & pd.notna(df['Q1_3D'])
    df['Q1_3D_Cierre_Arriba_Igual'] = (df['Close'] >= df['Q1_3D']) & pd.notna(df['Q1_3D'])

    df['Q4_3D_Cierre_Arriba'] = (df['Close'] > df['Q4_3D']) & pd.notna(df['Q4_3D'])
    df['Q4_3D_Cierre_Abajo_Igual'] = (df['Close'] <= df['Q4_3D']) & pd.notna(df['Q4_3D'])

    return df

def calcular_estadisticas_superacion_3d(df):
    """Calcula estadísticas cuando toca ambos niveles 3D"""
    logger.info("Calculando estadísticas de superación Three Days...")

    df['Cierre_Sobre_Q1_Ambos_3D'] = df['Toca_Q1_y_Q4_3D'] & (df['Close'] > df['Q1_3D'])
    df['Cierre_Bajo_Q4_Ambos_3D'] = df['Toca_Q1_y_Q4_3D'] & (df['Close'] < df['Q4_3D'])
    df['Cierre_Entre_Niveles_Ambos_3D'] = df['Toca_Q1_y_Q4_3D'] & (df['Close'] >= df['Q4_3D']) & (df['Close'] <= df['Q1_3D'])

    df['Puntos_Sobre_Q1_Ambos_3D'] = np.where(df['Cierre_Sobre_Q1_Ambos_3D'], df['Close'] - df['Q1_3D'], 0)
    df['Puntos_Bajo_Q4_Ambos_3D'] = np.where(df['Cierre_Bajo_Q4_Ambos_3D'], df['Q4_3D'] - df['Close'], 0)

    return df

def calcular_estadisticas_touches(df):
    """Calcula estadísticas de toques en niveles Q1 y Q4"""
    logger.info("Calculando estadísticas de toques...")

    df['Toca_Q1'] = (df['High'] >= df['Q1']) & pd.notna(df['Q1'])
    df['Toca_Q4'] = (df['Low'] <= df['Q4']) & pd.notna(df['Q4'])
    df['Toca_Q1_y_Q4'] = df['Toca_Q1'] & df['Toca_Q4']
    df['Toca_solo_Q1'] = df['Toca_Q1'] & ~df['Toca_Q4']
    df['Toca_solo_Q4'] = ~df['Toca_Q1'] & df['Toca_Q4']

    # Puntos sobre Q1 y bajo Q4
    df['Puntos_Sobre_Q1'] = np.where(df['High'] > df['Q1'], df['High'] - df['Q1'], 0)
    df['Puntos_Bajo_Q4'] = np.where(df['Low'] < df['Q4'], df['Q4'] - df['Low'], 0)

    return df

def calcular_estadisticas_cierres(df):
    """Calcula estadísticas de cierres respecto a niveles"""
    logger.info("Calculando estadísticas de cierres...")

    # Cierre respecto a Q1
    df['Q1_Cierre_Debajo'] = (df['Close'] < df['Q1']) & pd.notna(df['Q1'])
    df['Q1_Cierre_Arriba_Igual'] = (df['Close'] >= df['Q1']) & pd.notna(df['Q1'])

    # Cierre respecto a Q4
    df['Q4_Cierre_Arriba'] = (df['Close'] > df['Q4']) & pd.notna(df['Q4'])
    df['Q4_Cierre_Abajo_Igual'] = (df['Close'] <= df['Q4']) & pd.notna(df['Q4'])

    return df

def calcular_estadisticas_superacion(df):
    """Calcula estadísticas cuando toca ambos niveles"""
    logger.info("Calculando estadísticas de superación...")

    # Cuando toca ambos niveles
    df['Cierre_Sobre_Q1_Ambos'] = df['Toca_Q1_y_Q4'] & (df['Close'] > df['Q1'])
    df['Cierre_Bajo_Q4_Ambos'] = df['Toca_Q1_y_Q4'] & (df['Close'] < df['Q4'])
    df['Cierre_Entre_Niveles_Ambos'] = df['Toca_Q1_y_Q4'] & (df['Close'] >= df['Q4']) & (df['Close'] <= df['Q1'])

    # Puntos cuando toca ambos
    df['Puntos_Sobre_Q1_Ambos'] = np.where(df['Cierre_Sobre_Q1_Ambos'], df['Close'] - df['Q1'], 0)
    df['Puntos_Bajo_Q4_Ambos'] = np.where(df['Cierre_Bajo_Q4_Ambos'], df['Q4'] - df['Close'], 0)

    return df

def crear_hoja_resumen_touches(df):
    """Crea resumen de estadísticas de toques"""
    datos_validos = df[pd.notna(df['Q1'])]

    total = len(datos_validos)
    toca_q1 = datos_validos['Toca_Q1'].sum()
    toca_q4 = datos_validos['Toca_Q4'].sum()
    toca_ambos = datos_validos['Toca_Q1_y_Q4'].sum()
    toca_solo_q1 = datos_validos['Toca_solo_Q1'].sum()
    toca_solo_q4 = datos_validos['Toca_solo_Q4'].sum()

    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Analizados',
            'Toca Q1',
            'Toca Q4',
            'Toca Q1 y Q4',
            'Toca solo Q1',
            'Toca solo Q4',
            'Promedio Puntos Sobre Q1',
            'Promedio Puntos Bajo Q4'
        ],
        'Cantidad': [
            total,
            toca_q1,
            toca_q4,
            toca_ambos,
            toca_solo_q1,
            toca_solo_q4,
            datos_validos['Puntos_Sobre_Q1'].mean(),
            datos_validos['Puntos_Bajo_Q4'].mean()
        ],
        'Porcentaje': [
            100.0,
            (toca_q1 / total * 100) if total > 0 else 0,
            (toca_q4 / total * 100) if total > 0 else 0,
            (toca_ambos / total * 100) if total > 0 else 0,
            (toca_solo_q1 / total * 100) if total > 0 else 0,
            (toca_solo_q4 / total * 100) if total > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    return resumen

def crear_hoja_analisis_cierres(df):
    """Crea análisis de cierres"""
    datos_validos = df[pd.notna(df['Q1'])]

    total = len(datos_validos)

    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Analizados',
            'Q1: Cierre Debajo',
            'Q1: Cierre Arriba/Igual',
            'Q4: Cierre Arriba',
            'Q4: Cierre Abajo/Igual'
        ],
        'Cantidad': [
            total,
            datos_validos['Q1_Cierre_Debajo'].sum(),
            datos_validos['Q1_Cierre_Arriba_Igual'].sum(),
            datos_validos['Q4_Cierre_Arriba'].sum(),
            datos_validos['Q4_Cierre_Abajo_Igual'].sum()
        ],
        'Porcentaje': [
            100.0,
            (datos_validos['Q1_Cierre_Debajo'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Q1_Cierre_Arriba_Igual'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Q4_Cierre_Arriba'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Q4_Cierre_Abajo_Igual'].sum() / total * 100) if total > 0 else 0
        ]
    })

    return resumen

def crear_hoja_analisis_superacion(df):
    """Crea análisis de superación cuando toca ambos niveles"""
    datos_ambos = df[df['Toca_Q1_y_Q4']]

    total = len(datos_ambos)

    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Toca Ambos Niveles',
            'Cierre Sobre Q1',
            'Cierre Bajo Q4',
            'Cierre Entre Niveles',
            'Promedio Puntos Sobre Q1',
            'Promedio Puntos Bajo Q4'
        ],
        'Cantidad': [
            total,
            datos_ambos['Cierre_Sobre_Q1_Ambos'].sum(),
            datos_ambos['Cierre_Bajo_Q4_Ambos'].sum(),
            datos_ambos['Cierre_Entre_Niveles_Ambos'].sum(),
            datos_ambos['Puntos_Sobre_Q1_Ambos'].mean() if total > 0 else 0,
            datos_ambos['Puntos_Bajo_Q4_Ambos'].mean() if total > 0 else 0
        ],
        'Porcentaje': [
            100.0,
            (datos_ambos['Cierre_Sobre_Q1_Ambos'].sum() / total * 100) if total > 0 else 0,
            (datos_ambos['Cierre_Bajo_Q4_Ambos'].sum() / total * 100) if total > 0 else 0,
            (datos_ambos['Cierre_Entre_Niveles_Ambos'].sum() / total * 100) if total > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    return resumen

def crear_hoja_analisis_ambos_niveles(df):
    """Crea análisis detallado de días que tocan ambos niveles"""
    datos_ambos = df[df['Toca_Q1_y_Q4']].copy()

    columnas_relevantes = [
        'Date', 'Open', 'High', 'Low', 'Close',
        'Q1', 'Q4', 'Range', 'NR2',
        'Puntos_Sobre_Q1', 'Puntos_Bajo_Q4',
        'Cierre_Sobre_Q1_Ambos', 'Cierre_Bajo_Q4_Ambos', 'Cierre_Entre_Niveles_Ambos'
    ]

    return datos_ambos[columnas_relevantes]

def crear_hoja_detalle_ambos_niveles(df):
    """Crea detalle completo de días que tocan ambos niveles"""
    datos_ambos = df[df['Toca_Q1_y_Q4']].copy()
    return datos_ambos

def crear_hoja_resumen_touches_3d(df):
    """Crea resumen de estadísticas de toques Three Days"""
    datos_validos = df[pd.notna(df['Q1_3D'])]

    total = len(datos_validos)
    toca_q1 = datos_validos['Toca_Q1_3D'].sum()
    toca_q4 = datos_validos['Toca_Q4_3D'].sum()
    toca_ambos = datos_validos['Toca_Q1_y_Q4_3D'].sum()
    toca_solo_q1 = datos_validos['Toca_solo_Q1_3D'].sum()
    toca_solo_q4 = datos_validos['Toca_solo_Q4_3D'].sum()

    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Analizados (3D)',
            'Toca Q1_3D',
            'Toca Q4_3D',
            'Toca Q1_3D y Q4_3D',
            'Toca solo Q1_3D',
            'Toca solo Q4_3D',
            'Promedio Puntos Sobre Q1_3D',
            'Promedio Puntos Bajo Q4_3D'
        ],
        'Cantidad': [
            total,
            toca_q1,
            toca_q4,
            toca_ambos,
            toca_solo_q1,
            toca_solo_q4,
            datos_validos['Puntos_Sobre_Q1_3D'].mean(),
            datos_validos['Puntos_Bajo_Q4_3D'].mean()
        ],
        'Porcentaje': [
            100.0,
            (toca_q1 / total * 100) if total > 0 else 0,
            (toca_q4 / total * 100) if total > 0 else 0,
            (toca_ambos / total * 100) if total > 0 else 0,
            (toca_solo_q1 / total * 100) if total > 0 else 0,
            (toca_solo_q4 / total * 100) if total > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    return resumen

def crear_hoja_analisis_cierres_3d(df):
    """Crea análisis de cierres Three Days"""
    datos_validos = df[pd.notna(df['Q1_3D'])]

    total = len(datos_validos)

    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Analizados (3D)',
            'Q1_3D: Cierre Debajo',
            'Q1_3D: Cierre Arriba/Igual',
            'Q4_3D: Cierre Arriba',
            'Q4_3D: Cierre Abajo/Igual'
        ],
        'Cantidad': [
            total,
            datos_validos['Q1_3D_Cierre_Debajo'].sum(),
            datos_validos['Q1_3D_Cierre_Arriba_Igual'].sum(),
            datos_validos['Q4_3D_Cierre_Arriba'].sum(),
            datos_validos['Q4_3D_Cierre_Abajo_Igual'].sum()
        ],
        'Porcentaje': [
            100.0,
            (datos_validos['Q1_3D_Cierre_Debajo'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Q1_3D_Cierre_Arriba_Igual'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Q4_3D_Cierre_Arriba'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Q4_3D_Cierre_Abajo_Igual'].sum() / total * 100) if total > 0 else 0
        ]
    })

    return resumen

def crear_hoja_analisis_superacion_3d(df):
    """Crea análisis de superación Three Days cuando toca ambos niveles"""
    datos_ambos = df[df['Toca_Q1_y_Q4_3D']]

    total = len(datos_ambos)

    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Toca Ambos Niveles (3D)',
            'Cierre Sobre Q1_3D',
            'Cierre Bajo Q4_3D',
            'Cierre Entre Niveles',
            'Promedio Puntos Sobre Q1_3D',
            'Promedio Puntos Bajo Q4_3D'
        ],
        'Cantidad': [
            total,
            datos_ambos['Cierre_Sobre_Q1_Ambos_3D'].sum(),
            datos_ambos['Cierre_Bajo_Q4_Ambos_3D'].sum(),
            datos_ambos['Cierre_Entre_Niveles_Ambos_3D'].sum(),
            datos_ambos['Puntos_Sobre_Q1_Ambos_3D'].mean() if total > 0 else 0,
            datos_ambos['Puntos_Bajo_Q4_Ambos_3D'].mean() if total > 0 else 0
        ],
        'Porcentaje': [
            100.0,
            (datos_ambos['Cierre_Sobre_Q1_Ambos_3D'].sum() / total * 100) if total > 0 else 0,
            (datos_ambos['Cierre_Bajo_Q4_Ambos_3D'].sum() / total * 100) if total > 0 else 0,
            (datos_ambos['Cierre_Entre_Niveles_Ambos_3D'].sum() / total * 100) if total > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    return resumen

def main():
    logger.info("="*60)
    logger.info("INICIANDO CÁLCULO DE NIVELES DN")
    logger.info("="*60)

    # 1. Cargar datos
    df = cargar_datos_diarios()

    # 2. Calcular niveles DN One Day
    df = calcular_niveles_DN_oneday(df)

    # 3. Calcular niveles DN Three Days
    df = calcular_niveles_DN_threedays(df)

    # 4. Calcular estadísticas One Day
    df = calcular_estadisticas_touches(df)
    df = calcular_estadisticas_cierres(df)
    df = calcular_estadisticas_superacion(df)

    # 5. Calcular estadísticas Three Days
    df = calcular_estadisticas_touches_3d(df)
    df = calcular_estadisticas_cierres_3d(df)
    df = calcular_estadisticas_superacion_3d(df)

    # 6. Crear hojas de resumen One Day
    resumen_touches = crear_hoja_resumen_touches(df)
    analisis_cierres = crear_hoja_analisis_cierres(df)
    analisis_superacion = crear_hoja_analisis_superacion(df)
    analisis_ambos = crear_hoja_analisis_ambos_niveles(df)
    detalle_ambos = crear_hoja_detalle_ambos_niveles(df)

    # 7. Crear hojas de resumen Three Days
    resumen_touches_3d = crear_hoja_resumen_touches_3d(df)
    analisis_cierres_3d = crear_hoja_analisis_cierres_3d(df)
    analisis_superacion_3d = crear_hoja_analisis_superacion_3d(df)

    # 8. Guardar en Excel
    logger.info(f"Guardando resultados en {OUTPUT_FILE}")
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Datos_Completos', index=False)

        # Hojas One Day
        resumen_touches.to_excel(writer, sheet_name='1D_Resumen_Touches', index=False)
        analisis_cierres.to_excel(writer, sheet_name='1D_Analisis_Cierres', index=False)
        analisis_superacion.to_excel(writer, sheet_name='1D_Analisis_Superacion', index=False)
        analisis_ambos.to_excel(writer, sheet_name='1D_Analisis_Ambos', index=False)
        detalle_ambos.to_excel(writer, sheet_name='1D_Detalle_Ambos', index=False)

        # Hojas Three Days
        resumen_touches_3d.to_excel(writer, sheet_name='3D_Resumen_Touches', index=False)
        analisis_cierres_3d.to_excel(writer, sheet_name='3D_Analisis_Cierres', index=False)
        analisis_superacion_3d.to_excel(writer, sheet_name='3D_Analisis_Superacion', index=False)

    logger.info("="*60)
    logger.info("PROCESO COMPLETADO EXITOSAMENTE")
    logger.info(f"Archivo generado: {OUTPUT_FILE}")
    logger.info("="*60)

    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN DE TOQUES - ONE DAY")
    print("="*60)
    print(resumen_touches.to_string(index=False))

    print("\n" + "="*60)
    print("ANÁLISIS DE CIERRES - ONE DAY")
    print("="*60)
    print(analisis_cierres.to_string(index=False))

    print("\n" + "="*60)
    print("ANÁLISIS DE SUPERACIÓN (Ambos Niveles) - ONE DAY")
    print("="*60)
    print(analisis_superacion.to_string(index=False))

    print("\n" + "="*60)
    print("RESUMEN DE TOQUES - THREE DAYS")
    print("="*60)
    print(resumen_touches_3d.to_string(index=False))

    print("\n" + "="*60)
    print("ANÁLISIS DE CIERRES - THREE DAYS")
    print("="*60)
    print(analisis_cierres_3d.to_string(index=False))

    print("\n" + "="*60)
    print("ANÁLISIS DE SUPERACIÓN (Ambos Niveles) - THREE DAYS")
    print("="*60)
    print(analisis_superacion_3d.to_string(index=False))

if __name__ == "__main__":
    main()

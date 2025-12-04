"""
Script para filtrar datos del año 2025 y crear hojas de estadísticas
Versión: 1.0 - 2025-12-04 20:05
Cambios: Creación inicial - filtra año 2025 del archivo Datos_Diarios_DN_Niveles.xlsx
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('filtrar_datos_2025_DN.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

INPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/Datos_Diarios_DN_Niveles.xlsx")

def crear_estadisticas_2025(df_2025):
    """Crea todas las estadísticas para el año 2025"""

    # Resumen Touches One Day
    datos_validos = df_2025[pd.notna(df_2025['Q1'])]
    total = len(datos_validos)

    resumen_1d = pd.DataFrame({
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
            datos_validos['Toca_Q1'].sum(),
            datos_validos['Toca_Q4'].sum(),
            datos_validos['Toca_Q1_y_Q4'].sum(),
            datos_validos['Toca_solo_Q1'].sum(),
            datos_validos['Toca_solo_Q4'].sum(),
            datos_validos['Puntos_Sobre_Q1'].mean(),
            datos_validos['Puntos_Bajo_Q4'].mean()
        ],
        'Porcentaje': [
            100.0,
            (datos_validos['Toca_Q1'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Toca_Q4'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Toca_Q1_y_Q4'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Toca_solo_Q1'].sum() / total * 100) if total > 0 else 0,
            (datos_validos['Toca_solo_Q4'].sum() / total * 100) if total > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    # Análisis Cierres One Day
    analisis_cierres_1d = pd.DataFrame({
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

    # Análisis Superación One Day
    datos_ambos = df_2025[df_2025['Toca_Q1_y_Q4']]
    total_ambos = len(datos_ambos)

    analisis_superacion_1d = pd.DataFrame({
        'Estadistica': [
            'Total Dias Toca Ambos Niveles',
            'Cierre Sobre Q1',
            'Cierre Bajo Q4',
            'Cierre Entre Niveles',
            'Promedio Puntos Sobre Q1',
            'Promedio Puntos Bajo Q4'
        ],
        'Cantidad': [
            total_ambos,
            datos_ambos['Cierre_Sobre_Q1_Ambos'].sum() if total_ambos > 0 else 0,
            datos_ambos['Cierre_Bajo_Q4_Ambos'].sum() if total_ambos > 0 else 0,
            datos_ambos['Cierre_Entre_Niveles_Ambos'].sum() if total_ambos > 0 else 0,
            datos_ambos['Puntos_Sobre_Q1_Ambos'].mean() if total_ambos > 0 else 0,
            datos_ambos['Puntos_Bajo_Q4_Ambos'].mean() if total_ambos > 0 else 0
        ],
        'Porcentaje': [
            100.0,
            (datos_ambos['Cierre_Sobre_Q1_Ambos'].sum() / total_ambos * 100) if total_ambos > 0 else 0,
            (datos_ambos['Cierre_Bajo_Q4_Ambos'].sum() / total_ambos * 100) if total_ambos > 0 else 0,
            (datos_ambos['Cierre_Entre_Niveles_Ambos'].sum() / total_ambos * 100) if total_ambos > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    # Resumen Touches Three Days
    datos_validos_3d = df_2025[pd.notna(df_2025['Q1_3D'])]
    total_3d = len(datos_validos_3d)

    resumen_3d = pd.DataFrame({
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
            total_3d,
            datos_validos_3d['Toca_Q1_3D'].sum(),
            datos_validos_3d['Toca_Q4_3D'].sum(),
            datos_validos_3d['Toca_Q1_y_Q4_3D'].sum(),
            datos_validos_3d['Toca_solo_Q1_3D'].sum(),
            datos_validos_3d['Toca_solo_Q4_3D'].sum(),
            datos_validos_3d['Puntos_Sobre_Q1_3D'].mean(),
            datos_validos_3d['Puntos_Bajo_Q4_3D'].mean()
        ],
        'Porcentaje': [
            100.0,
            (datos_validos_3d['Toca_Q1_3D'].sum() / total_3d * 100) if total_3d > 0 else 0,
            (datos_validos_3d['Toca_Q4_3D'].sum() / total_3d * 100) if total_3d > 0 else 0,
            (datos_validos_3d['Toca_Q1_y_Q4_3D'].sum() / total_3d * 100) if total_3d > 0 else 0,
            (datos_validos_3d['Toca_solo_Q1_3D'].sum() / total_3d * 100) if total_3d > 0 else 0,
            (datos_validos_3d['Toca_solo_Q4_3D'].sum() / total_3d * 100) if total_3d > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    # Análisis Cierres Three Days
    analisis_cierres_3d = pd.DataFrame({
        'Estadistica': [
            'Total Dias Analizados (3D)',
            'Q1_3D: Cierre Debajo',
            'Q1_3D: Cierre Arriba/Igual',
            'Q4_3D: Cierre Arriba',
            'Q4_3D: Cierre Abajo/Igual'
        ],
        'Cantidad': [
            total_3d,
            datos_validos_3d['Q1_3D_Cierre_Debajo'].sum(),
            datos_validos_3d['Q1_3D_Cierre_Arriba_Igual'].sum(),
            datos_validos_3d['Q4_3D_Cierre_Arriba'].sum(),
            datos_validos_3d['Q4_3D_Cierre_Abajo_Igual'].sum()
        ],
        'Porcentaje': [
            100.0,
            (datos_validos_3d['Q1_3D_Cierre_Debajo'].sum() / total_3d * 100) if total_3d > 0 else 0,
            (datos_validos_3d['Q1_3D_Cierre_Arriba_Igual'].sum() / total_3d * 100) if total_3d > 0 else 0,
            (datos_validos_3d['Q4_3D_Cierre_Arriba'].sum() / total_3d * 100) if total_3d > 0 else 0,
            (datos_validos_3d['Q4_3D_Cierre_Abajo_Igual'].sum() / total_3d * 100) if total_3d > 0 else 0
        ]
    })

    # Análisis Superación Three Days
    datos_ambos_3d = df_2025[df_2025['Toca_Q1_y_Q4_3D']]
    total_ambos_3d = len(datos_ambos_3d)

    analisis_superacion_3d = pd.DataFrame({
        'Estadistica': [
            'Total Dias Toca Ambos Niveles (3D)',
            'Cierre Sobre Q1_3D',
            'Cierre Bajo Q4_3D',
            'Cierre Entre Niveles',
            'Promedio Puntos Sobre Q1_3D',
            'Promedio Puntos Bajo Q4_3D'
        ],
        'Cantidad': [
            total_ambos_3d,
            datos_ambos_3d['Cierre_Sobre_Q1_Ambos_3D'].sum() if total_ambos_3d > 0 else 0,
            datos_ambos_3d['Cierre_Bajo_Q4_Ambos_3D'].sum() if total_ambos_3d > 0 else 0,
            datos_ambos_3d['Cierre_Entre_Niveles_Ambos_3D'].sum() if total_ambos_3d > 0 else 0,
            datos_ambos_3d['Puntos_Sobre_Q1_Ambos_3D'].mean() if total_ambos_3d > 0 else 0,
            datos_ambos_3d['Puntos_Bajo_Q4_Ambos_3D'].mean() if total_ambos_3d > 0 else 0
        ],
        'Porcentaje': [
            100.0,
            (datos_ambos_3d['Cierre_Sobre_Q1_Ambos_3D'].sum() / total_ambos_3d * 100) if total_ambos_3d > 0 else 0,
            (datos_ambos_3d['Cierre_Bajo_Q4_Ambos_3D'].sum() / total_ambos_3d * 100) if total_ambos_3d > 0 else 0,
            (datos_ambos_3d['Cierre_Entre_Niveles_Ambos_3D'].sum() / total_ambos_3d * 100) if total_ambos_3d > 0 else 0,
            np.nan,
            np.nan
        ]
    })

    return {
        '2025_1D_Resumen_Touches': resumen_1d,
        '2025_1D_Analisis_Cierres': analisis_cierres_1d,
        '2025_1D_Analisis_Superacion': analisis_superacion_1d,
        '2025_3D_Resumen_Touches': resumen_3d,
        '2025_3D_Analisis_Cierres': analisis_cierres_3d,
        '2025_3D_Analisis_Superacion': analisis_superacion_3d
    }

def main():
    logger.info("="*60)
    logger.info("FILTRANDO DATOS DEL AÑO 2025")
    logger.info("="*60)

    # Leer archivo completo
    logger.info(f"Leyendo archivo: {INPUT_FILE}")
    df = pd.read_excel(INPUT_FILE, sheet_name='Datos_Completos')

    # Convertir Date a datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Filtrar año 2025
    df_2025 = df[df['Date'].dt.year == 2025].copy()
    logger.info(f"Registros del año 2025: {len(df_2025)}")
    logger.info(f"Rango de fechas: {df_2025['Date'].min()} a {df_2025['Date'].max()}")

    # Crear estadísticas del 2025
    logger.info("Calculando estadísticas para 2025...")
    estadisticas_2025 = crear_estadisticas_2025(df_2025)

    # Leer todas las hojas existentes
    logger.info("Leyendo hojas existentes...")
    with pd.ExcelFile(INPUT_FILE) as xls:
        hojas_existentes = {sheet: pd.read_excel(xls, sheet) for sheet in xls.sheet_names}

    # Agregar nuevas hojas con datos del 2025
    hojas_existentes['Datos_2025'] = df_2025
    hojas_existentes.update(estadisticas_2025)

    # Guardar archivo actualizado
    logger.info(f"Guardando archivo actualizado con hojas del 2025...")
    with pd.ExcelWriter(INPUT_FILE, engine='openpyxl', mode='w') as writer:
        for nombre_hoja, df_hoja in hojas_existentes.items():
            df_hoja.to_excel(writer, sheet_name=nombre_hoja, index=False)

    logger.info("="*60)
    logger.info("PROCESO COMPLETADO")
    logger.info(f"Archivo actualizado: {INPUT_FILE}")
    logger.info(f"Nuevas hojas agregadas:")
    logger.info("  - Datos_2025")
    for nombre in estadisticas_2025.keys():
        logger.info(f"  - {nombre}")
    logger.info("="*60)

    # Mostrar resúmenes
    print("\n" + "="*60)
    print("RESUMEN ONE DAY - AÑO 2025")
    print("="*60)
    print(estadisticas_2025['2025_1D_Resumen_Touches'].to_string(index=False))

    print("\n" + "="*60)
    print("RESUMEN THREE DAYS - AÑO 2025")
    print("="*60)
    print(estadisticas_2025['2025_3D_Resumen_Touches'].to_string(index=False))

if __name__ == "__main__":
    main()

"""
Script para filtrar días con distancias mínimas entre niveles DN y EM21
Versión: 1.0 - 2025-12-06 20:45
Cambios: Filtra días donde distancia Q1 o Q4 <= 50 puntos
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('filtrar_distancias_minimas.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

INPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/2025.xlsx")
OUTPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/2025_actualizado.xlsx")
DISTANCIA_MAX = 50  # puntos

def filtrar_distancias_q1(df):
    """Filtra días donde la distancia entre Q1 es <= 50 puntos"""
    logger.info(f"Filtrando días con distancia Q1 <= {DISTANCIA_MAX} puntos...")

    # Filtrar
    df_filtrado = df[df['Distancia_Q1'] <= DISTANCIA_MAX].copy()

    logger.info(f"Encontrados {len(df_filtrado)} días con distancia Q1 <= {DISTANCIA_MAX} puntos")

    # Seleccionar columnas relevantes
    columnas_relevantes = [
        'Date',
        'Open_DN', 'High_DN', 'Low_DN', 'Close_DN',
        'Q1_DN', 'EMH_EM21',
        'Q1_Mayor', 'Q1_Menor', 'Distancia_Q1',
        'Q1_Mayor_es_DN',
        'Entre_Q1', 'Rompe_Q1_Mayor',
        'Rompe_Q1_Mayor_y_Cierra_Arriba', 'Rompe_Q1_Mayor_y_Cierra_Debajo',
        'Entre_Q1_y_Cierra_Zona', 'Entre_Q1_y_Cierra_Debajo_Menor'
    ]

    # Verificar que todas las columnas existen
    columnas_existentes = [col for col in columnas_relevantes if col in df_filtrado.columns]

    resultado = df_filtrado[columnas_existentes].copy()

    # Ordenar por distancia ascendente
    resultado = resultado.sort_values('Distancia_Q1')

    return resultado

def filtrar_distancias_q4(df):
    """Filtra días donde la distancia entre Q4 es <= 50 puntos"""
    logger.info(f"Filtrando días con distancia Q4 <= {DISTANCIA_MAX} puntos...")

    # Filtrar
    df_filtrado = df[df['Distancia_Q4'] <= DISTANCIA_MAX].copy()

    logger.info(f"Encontrados {len(df_filtrado)} días con distancia Q4 <= {DISTANCIA_MAX} puntos")

    # Seleccionar columnas relevantes
    columnas_relevantes = [
        'Date',
        'Open_DN', 'High_DN', 'Low_DN', 'Close_DN',
        'Q4_DN', 'EML_EM21',
        'Q4_Mayor', 'Q4_Menor', 'Distancia_Q4',
        'Q4_Mayor_es_DN',
        'Entre_Q4', 'Rompe_Q4_Menor',
        'Rompe_Q4_Menor_y_Cierra_Debajo', 'Rompe_Q4_Menor_y_Cierra_Arriba',
        'Entre_Q4_y_Cierra_Zona', 'Entre_Q4_y_Cierra_Arriba_Mayor'
    ]

    # Verificar que todas las columnas existen
    columnas_existentes = [col for col in columnas_relevantes if col in df_filtrado.columns]

    resultado = df_filtrado[columnas_existentes].copy()

    # Ordenar por distancia ascendente
    resultado = resultado.sort_values('Distancia_Q4')

    return resultado

def crear_resumen_filtrados(df_q1, df_q4):
    """Crea resumen de los días filtrados"""

    resumen = pd.DataFrame({
        'Metrica': [
            f'Días con distancia Q1 <= {DISTANCIA_MAX} puntos',
            'Distancia Q1 mínima',
            'Distancia Q1 máxima (de los filtrados)',
            'Distancia Q1 promedio (de los filtrados)',
            '',
            f'Días con distancia Q4 <= {DISTANCIA_MAX} puntos',
            'Distancia Q4 mínima',
            'Distancia Q4 máxima (de los filtrados)',
            'Distancia Q4 promedio (de los filtrados)',
            '',
            'Días que cumplen ambos criterios (Q1 y Q4)'
        ],
        'Valor': [
            len(df_q1),
            df_q1['Distancia_Q1'].min() if len(df_q1) > 0 else np.nan,
            df_q1['Distancia_Q1'].max() if len(df_q1) > 0 else np.nan,
            df_q1['Distancia_Q1'].mean() if len(df_q1) > 0 else np.nan,
            np.nan,
            len(df_q4),
            df_q4['Distancia_Q4'].min() if len(df_q4) > 0 else np.nan,
            df_q4['Distancia_Q4'].max() if len(df_q4) > 0 else np.nan,
            df_q4['Distancia_Q4'].mean() if len(df_q4) > 0 else np.nan,
            np.nan,
            len(set(df_q1['Date'].tolist()) & set(df_q4['Date'].tolist()))
        ]
    })

    return resumen

def main():
    logger.info("="*60)
    logger.info("FILTRADO DE DISTANCIAS MÍNIMAS")
    logger.info("="*60)

    # 1. Cargar datos completos
    logger.info(f"Leyendo {INPUT_FILE}")
    df = pd.read_excel(INPUT_FILE, sheet_name='Datos_Completos')
    df['Date'] = pd.to_datetime(df['Date'])

    logger.info(f"Total de registros: {len(df)}")

    # 2. Filtrar días con distancias mínimas
    df_q1_filtrado = filtrar_distancias_q1(df)
    df_q4_filtrado = filtrar_distancias_q4(df)

    # 3. Crear resumen
    resumen = crear_resumen_filtrados(df_q1_filtrado, df_q4_filtrado)

    # 4. Leer todas las hojas existentes
    logger.info("Leyendo hojas existentes del archivo...")
    with pd.ExcelFile(INPUT_FILE) as xls:
        hojas_existentes = {sheet: pd.read_excel(xls, sheet) for sheet in xls.sheet_names}

    # 5. Agregar nuevas hojas
    hojas_existentes['Q1_Distancia_Minima'] = df_q1_filtrado
    hojas_existentes['Q4_Distancia_Minima'] = df_q4_filtrado
    hojas_existentes['Resumen_Distancias_Minimas'] = resumen

    # 6. Guardar todo de nuevo
    logger.info(f"Guardando archivo actualizado en {OUTPUT_FILE}")
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl', mode='w') as writer:
        for nombre_hoja, df_hoja in hojas_existentes.items():
            df_hoja.to_excel(writer, sheet_name=nombre_hoja, index=False)

    logger.info("="*60)
    logger.info("PROCESO COMPLETADO")
    logger.info(f"Archivo generado: {OUTPUT_FILE}")
    logger.info(f"Nuevas hojas agregadas:")
    logger.info("  - Q1_Distancia_Minima")
    logger.info("  - Q4_Distancia_Minima")
    logger.info("  - Resumen_Distancias_Minimas")
    logger.info("="*60)

    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN DE DISTANCIAS MÍNIMAS")
    print("="*60)
    print(resumen.to_string(index=False))

    print("\n" + "="*60)
    print(f"DÍAS CON DISTANCIA Q1 <= {DISTANCIA_MAX} PUNTOS")
    print("="*60)
    if len(df_q1_filtrado) > 0:
        print(df_q1_filtrado[['Date', 'Q1_DN', 'EMH_EM21', 'Distancia_Q1']].to_string(index=False))
    else:
        print("No se encontraron días con esta condición")

    print("\n" + "="*60)
    print(f"DÍAS CON DISTANCIA Q4 <= {DISTANCIA_MAX} PUNTOS")
    print("="*60)
    if len(df_q4_filtrado) > 0:
        print(df_q4_filtrado[['Date', 'Q4_DN', 'EML_EM21', 'Distancia_Q4']].to_string(index=False))
    else:
        print("No se encontraron días con esta condición")

if __name__ == "__main__":
    main()

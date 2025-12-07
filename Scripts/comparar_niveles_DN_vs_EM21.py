"""
Script para comparar niveles DN vs EM21 para el año 2025
Versión: 1.0 - 2025-12-04 20:30
Cambios: Creación inicial - Análisis comparativo de niveles Q1 y Q4
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('comparar_niveles_DN_vs_EM21.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rutas
DN_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/Datos_Diarios_DN_Niveles.xlsx")
EM21_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx")
OUTPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/2025.xlsx")

def cargar_datos_2025():
    """Carga los datos del año 2025 de ambos archivos"""
    logger.info("Cargando datos del año 2025...")

    # Cargar DN (hoja específica del 2025)
    df_dn = pd.read_excel(DN_FILE, sheet_name='Datos_2025')
    df_dn['Date'] = pd.to_datetime(df_dn['Date'])

    # Cargar EM21 (archivo completo es solo 2025)
    df_em21 = pd.read_excel(EM21_FILE, sheet_name='Sheet1')
    df_em21['Date'] = pd.to_datetime(df_em21['Date'])

    logger.info(f"DN: {len(df_dn)} registros")
    logger.info(f"EM21: {len(df_em21)} registros")

    # Verificar que tengan las mismas fechas
    if not df_dn['Date'].equals(df_em21['Date']):
        logger.warning("Las fechas no coinciden exactamente, haciendo merge por fecha")
        df_merged = pd.merge(df_dn, df_em21, on='Date', suffixes=('_DN', '_EM21'), how='inner')
    else:
        # Renombrar columnas para distinguir
        df_dn.columns = [f"{col}_DN" if col != 'Date' else col for col in df_dn.columns]
        df_em21.columns = [f"{col}_EM21" if col != 'Date' else col for col in df_em21.columns]
        df_merged = pd.merge(df_dn, df_em21, on='Date', how='inner')

    logger.info(f"Datos fusionados: {len(df_merged)} registros")
    return df_merged

def calcular_distancias_q1(df):
    """Calcula distancias entre niveles Q1 de DN y EM21"""
    logger.info("Calculando distancias entre Q1...")

    # Identificar cuál Q1 es mayor
    df['Q1_Mayor'] = df[['Q1_DN', 'EMH_EM21']].max(axis=1)
    df['Q1_Menor'] = df[['Q1_DN', 'EMH_EM21']].min(axis=1)
    df['Distancia_Q1'] = df['Q1_Mayor'] - df['Q1_Menor']
    df['Q1_Mayor_es_DN'] = df['Q1_DN'] > df['EMH_EM21']

    media_distancia = df['Distancia_Q1'].mean()
    logger.info(f"Distancia media entre Q1: {media_distancia:.2f} puntos")

    return df, media_distancia

def calcular_distancias_q4(df):
    """Calcula distancias entre niveles Q4 de DN y EM21"""
    logger.info("Calculando distancias entre Q4...")

    # Identificar cuál Q4 es mayor (más alto)
    df['Q4_Mayor'] = df[['Q4_DN', 'EML_EM21']].max(axis=1)
    df['Q4_Menor'] = df[['Q4_DN', 'EML_EM21']].min(axis=1)
    df['Distancia_Q4'] = df['Q4_Mayor'] - df['Q4_Menor']
    df['Q4_Mayor_es_DN'] = df['Q4_DN'] > df['EML_EM21']

    media_distancia = df['Distancia_Q4'].mean()
    logger.info(f"Distancia media entre Q4: {media_distancia:.2f} puntos")

    return df, media_distancia

def analizar_comportamiento_q1(df):
    """Analiza el comportamiento del precio respecto a los Q1"""
    logger.info("Analizando comportamiento respecto a Q1...")

    # Usar columnas High y Close del DN (son las mismas en ambos archivos)
    high = df['High_DN']
    close = df['Close_DN']

    # Condiciones para Q1
    df['Entre_Q1'] = (high < df['Q1_Mayor']) & (high >= df['Q1_Menor'])
    df['Rompe_Q1_Mayor'] = high >= df['Q1_Mayor']
    df['No_Alcanza_Q1_Menor'] = high < df['Q1_Menor']

    # Para los que rompen Q1_Mayor
    df['Rompe_Q1_Mayor_y_Cierra_Arriba'] = df['Rompe_Q1_Mayor'] & (close > df['Q1_Mayor'])
    df['Rompe_Q1_Mayor_y_Cierra_Debajo'] = df['Rompe_Q1_Mayor'] & (close <= df['Q1_Mayor'])

    # Para los que quedan entre ambos Q1
    df['Entre_Q1_y_Cierra_Zona'] = df['Entre_Q1'] & (close >= df['Q1_Menor']) & (close <= df['Q1_Mayor'])
    df['Entre_Q1_y_Cierra_Debajo_Menor'] = df['Entre_Q1'] & (close < df['Q1_Menor'])
    df['Entre_Q1_y_Cierra_Arriba_Mayor'] = df['Entre_Q1'] & (close > df['Q1_Mayor'])

    # Contar
    total = len(df)
    stats = {
        'Total_Dias': total,
        'Entre_Q1': df['Entre_Q1'].sum(),
        'Rompe_Q1_Mayor': df['Rompe_Q1_Mayor'].sum(),
        'No_Alcanza_Q1_Menor': df['No_Alcanza_Q1_Menor'].sum(),
        'Rompe_Q1_Mayor_y_Cierra_Arriba': df['Rompe_Q1_Mayor_y_Cierra_Arriba'].sum(),
        'Rompe_Q1_Mayor_y_Cierra_Debajo': df['Rompe_Q1_Mayor_y_Cierra_Debajo'].sum(),
        'Entre_Q1_y_Cierra_Zona': df['Entre_Q1_y_Cierra_Zona'].sum(),
        'Entre_Q1_y_Cierra_Debajo_Menor': df['Entre_Q1_y_Cierra_Debajo_Menor'].sum(),
        'Entre_Q1_y_Cierra_Arriba_Mayor': df['Entre_Q1_y_Cierra_Arriba_Mayor'].sum()
    }

    # Crear DataFrame de resumen
    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Analizados',
            'Precio entre ambos Q1',
            'Rompe Q1 más alto',
            'No alcanza Q1 más bajo',
            '',
            'De los que rompen Q1 alto:',
            '  - Cierran arriba del Q1 alto',
            '  - Cierran debajo del Q1 alto',
            '',
            'De los que quedan entre Q1:',
            '  - Cierran en la zona (entre Q1)',
            '  - Cierran debajo del Q1 bajo',
            '  - Cierran arriba del Q1 alto'
        ],
        'Cantidad': [
            stats['Total_Dias'],
            stats['Entre_Q1'],
            stats['Rompe_Q1_Mayor'],
            stats['No_Alcanza_Q1_Menor'],
            np.nan,
            np.nan,
            stats['Rompe_Q1_Mayor_y_Cierra_Arriba'],
            stats['Rompe_Q1_Mayor_y_Cierra_Debajo'],
            np.nan,
            np.nan,
            stats['Entre_Q1_y_Cierra_Zona'],
            stats['Entre_Q1_y_Cierra_Debajo_Menor'],
            stats['Entre_Q1_y_Cierra_Arriba_Mayor']
        ],
        'Porcentaje': [
            100.0,
            (stats['Entre_Q1'] / total * 100) if total > 0 else 0,
            (stats['Rompe_Q1_Mayor'] / total * 100) if total > 0 else 0,
            (stats['No_Alcanza_Q1_Menor'] / total * 100) if total > 0 else 0,
            np.nan,
            np.nan,
            (stats['Rompe_Q1_Mayor_y_Cierra_Arriba'] / stats['Rompe_Q1_Mayor'] * 100) if stats['Rompe_Q1_Mayor'] > 0 else 0,
            (stats['Rompe_Q1_Mayor_y_Cierra_Debajo'] / stats['Rompe_Q1_Mayor'] * 100) if stats['Rompe_Q1_Mayor'] > 0 else 0,
            np.nan,
            np.nan,
            (stats['Entre_Q1_y_Cierra_Zona'] / stats['Entre_Q1'] * 100) if stats['Entre_Q1'] > 0 else 0,
            (stats['Entre_Q1_y_Cierra_Debajo_Menor'] / stats['Entre_Q1'] * 100) if stats['Entre_Q1'] > 0 else 0,
            (stats['Entre_Q1_y_Cierra_Arriba_Mayor'] / stats['Entre_Q1'] * 100) if stats['Entre_Q1'] > 0 else 0
        ]
    })

    return df, resumen

def analizar_comportamiento_q4(df):
    """Analiza el comportamiento del precio respecto a los Q4"""
    logger.info("Analizando comportamiento respecto a Q4...")

    low = df['Low_DN']
    close = df['Close_DN']

    # Condiciones para Q4
    df['Entre_Q4'] = (low > df['Q4_Menor']) & (low <= df['Q4_Mayor'])
    df['Rompe_Q4_Menor'] = low <= df['Q4_Menor']
    df['No_Alcanza_Q4_Mayor'] = low > df['Q4_Mayor']

    # Para los que rompen Q4_Menor (más bajo)
    df['Rompe_Q4_Menor_y_Cierra_Debajo'] = df['Rompe_Q4_Menor'] & (close < df['Q4_Menor'])
    df['Rompe_Q4_Menor_y_Cierra_Arriba'] = df['Rompe_Q4_Menor'] & (close >= df['Q4_Menor'])

    # Para los que quedan entre ambos Q4
    df['Entre_Q4_y_Cierra_Zona'] = df['Entre_Q4'] & (close >= df['Q4_Menor']) & (close <= df['Q4_Mayor'])
    df['Entre_Q4_y_Cierra_Arriba_Mayor'] = df['Entre_Q4'] & (close > df['Q4_Mayor'])
    df['Entre_Q4_y_Cierra_Debajo_Menor'] = df['Entre_Q4'] & (close < df['Q4_Menor'])

    # Contar
    total = len(df)
    stats = {
        'Total_Dias': total,
        'Entre_Q4': df['Entre_Q4'].sum(),
        'Rompe_Q4_Menor': df['Rompe_Q4_Menor'].sum(),
        'No_Alcanza_Q4_Mayor': df['No_Alcanza_Q4_Mayor'].sum(),
        'Rompe_Q4_Menor_y_Cierra_Debajo': df['Rompe_Q4_Menor_y_Cierra_Debajo'].sum(),
        'Rompe_Q4_Menor_y_Cierra_Arriba': df['Rompe_Q4_Menor_y_Cierra_Arriba'].sum(),
        'Entre_Q4_y_Cierra_Zona': df['Entre_Q4_y_Cierra_Zona'].sum(),
        'Entre_Q4_y_Cierra_Arriba_Mayor': df['Entre_Q4_y_Cierra_Arriba_Mayor'].sum(),
        'Entre_Q4_y_Cierra_Debajo_Menor': df['Entre_Q4_y_Cierra_Debajo_Menor'].sum()
    }

    # Crear DataFrame de resumen
    resumen = pd.DataFrame({
        'Estadistica': [
            'Total Dias Analizados',
            'Precio entre ambos Q4',
            'Rompe Q4 más bajo',
            'No alcanza Q4 más alto',
            '',
            'De los que rompen Q4 bajo:',
            '  - Cierran debajo del Q4 bajo',
            '  - Cierran arriba del Q4 bajo',
            '',
            'De los que quedan entre Q4:',
            '  - Cierran en la zona (entre Q4)',
            '  - Cierran arriba del Q4 alto',
            '  - Cierran debajo del Q4 bajo'
        ],
        'Cantidad': [
            stats['Total_Dias'],
            stats['Entre_Q4'],
            stats['Rompe_Q4_Menor'],
            stats['No_Alcanza_Q4_Mayor'],
            np.nan,
            np.nan,
            stats['Rompe_Q4_Menor_y_Cierra_Debajo'],
            stats['Rompe_Q4_Menor_y_Cierra_Arriba'],
            np.nan,
            np.nan,
            stats['Entre_Q4_y_Cierra_Zona'],
            stats['Entre_Q4_y_Cierra_Arriba_Mayor'],
            stats['Entre_Q4_y_Cierra_Debajo_Menor']
        ],
        'Porcentaje': [
            100.0,
            (stats['Entre_Q4'] / total * 100) if total > 0 else 0,
            (stats['Rompe_Q4_Menor'] / total * 100) if total > 0 else 0,
            (stats['No_Alcanza_Q4_Mayor'] / total * 100) if total > 0 else 0,
            np.nan,
            np.nan,
            (stats['Rompe_Q4_Menor_y_Cierra_Debajo'] / stats['Rompe_Q4_Menor'] * 100) if stats['Rompe_Q4_Menor'] > 0 else 0,
            (stats['Rompe_Q4_Menor_y_Cierra_Arriba'] / stats['Rompe_Q4_Menor'] * 100) if stats['Rompe_Q4_Menor'] > 0 else 0,
            np.nan,
            np.nan,
            (stats['Entre_Q4_y_Cierra_Zona'] / stats['Entre_Q4'] * 100) if stats['Entre_Q4'] > 0 else 0,
            (stats['Entre_Q4_y_Cierra_Arriba_Mayor'] / stats['Entre_Q4'] * 100) if stats['Entre_Q4'] > 0 else 0,
            (stats['Entre_Q4_y_Cierra_Debajo_Menor'] / stats['Entre_Q4'] * 100) if stats['Entre_Q4'] > 0 else 0
        ]
    })

    return df, resumen

def crear_resumen_distancias(media_q1, media_q4, df):
    """Crea resumen de distancias entre niveles"""

    resumen = pd.DataFrame({
        'Metrica': [
            'Distancia Media Q1 (DN vs EM21)',
            'Distancia Máxima Q1',
            'Distancia Mínima Q1',
            '',
            'Distancia Media Q4 (DN vs EM21)',
            'Distancia Máxima Q4',
            'Distancia Mínima Q4',
            '',
            'Días donde Q1_DN > EMH_EM21',
            'Días donde Q4_DN > EML_EM21'
        ],
        'Valor': [
            media_q1,
            df['Distancia_Q1'].max(),
            df['Distancia_Q1'].min(),
            np.nan,
            media_q4,
            df['Distancia_Q4'].max(),
            df['Distancia_Q4'].min(),
            np.nan,
            df['Q1_Mayor_es_DN'].sum(),
            df['Q4_Mayor_es_DN'].sum()
        ],
        'Porcentaje': [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            (df['Q1_Mayor_es_DN'].sum() / len(df) * 100),
            (df['Q4_Mayor_es_DN'].sum() / len(df) * 100)
        ]
    })

    return resumen

def main():
    logger.info("="*60)
    logger.info("COMPARACIÓN NIVELES DN vs EM21 - AÑO 2025")
    logger.info("="*60)

    # 1. Cargar datos
    df = cargar_datos_2025()

    # 2. Calcular distancias
    df, media_q1 = calcular_distancias_q1(df)
    df, media_q4 = calcular_distancias_q4(df)

    # 3. Analizar comportamientos
    df, resumen_q1 = analizar_comportamiento_q1(df)
    df, resumen_q4 = analizar_comportamiento_q4(df)

    # 4. Crear resumen de distancias
    resumen_distancias = crear_resumen_distancias(media_q1, media_q4, df)

    # 5. Guardar resultados
    logger.info(f"Guardando resultados en {OUTPUT_FILE}")
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Datos_Completos', index=False)
        resumen_distancias.to_excel(writer, sheet_name='Resumen_Distancias', index=False)
        resumen_q1.to_excel(writer, sheet_name='Analisis_Q1', index=False)
        resumen_q4.to_excel(writer, sheet_name='Analisis_Q4', index=False)

    logger.info("="*60)
    logger.info("PROCESO COMPLETADO")
    logger.info(f"Archivo generado: {OUTPUT_FILE}")
    logger.info("="*60)

    # Mostrar resultados
    print("\n" + "="*60)
    print("RESUMEN DE DISTANCIAS")
    print("="*60)
    print(resumen_distancias.to_string(index=False))

    print("\n" + "="*60)
    print("ANÁLISIS DE COMPORTAMIENTO - Q1")
    print("="*60)
    print(resumen_q1.to_string(index=False))

    print("\n" + "="*60)
    print("ANÁLISIS DE COMPORTAMIENTO - Q4")
    print("="*60)
    print(resumen_q4.to_string(index=False))

if __name__ == "__main__":
    main()

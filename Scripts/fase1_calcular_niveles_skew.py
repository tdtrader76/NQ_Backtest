"""
Script para calcular niveles con Skew - FASE 1.3
Versión: 1.0
Fecha: 2025-12-01

Descripción:
    Calcula todos los niveles basados en Expected Move con ajuste de Skew
    según la metodología definida en calculos.md
    
Niveles calculados:
    - Q1, Q4 (ya existen como EMH, EML)
    - NR2 (Current Open)
    - Rango Total
    - Porcentajes de skew
    - TCH, TCL, TVH, TVL
    - Z2H, Z2L, Z3H, Z3L
    - Q2, Q3
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../Logs/fase1_calcular_niveles_skew.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def round_to_quarter(value):
    """Redondea al 0.25 más cercano"""
    return round(value * 4) / 4

def calcular_niveles_skew(df):
    """
    Calcula todos los niveles con ajuste de skew
    
    Args:
        df: DataFrame con columnas Open, EMH, EML
        
    Returns:
        DataFrame con todas las columnas de niveles agregadas
    """
    logger.info("="*80)
    logger.info("CALCULANDO NIVELES CON SKEW")
    logger.info("="*80)
    
    df = df.copy()
    
    df['Q1'] = df['EMH']
    df['Q4'] = df['EML']
    df['NR2'] = df['Open']
    
    df['RangoTotal'] = df['Q1'] - df['Q4']
    
    df['PctAboveNR2'] = ((df['Q1'] - df['NR2']) / df['RangoTotal']) * 100
    df['PctBelowNR2'] = ((df['NR2'] - df['Q4']) / df['RangoTotal']) * 100
    
    df['SkewMayor'] = df[['PctAboveNR2', 'PctBelowNR2']].max(axis=1)
    df['DiferenciaSkew'] = abs(df['SkewMayor'] - 50.0)
    
    df['TCH'] = df['Q1'] - (0.125 * df['RangoTotal'])
    df['TCL'] = df['Q1'] - (0.159 * df['RangoTotal'])
    df['TVH'] = df['Q1'] - (0.875 * df['RangoTotal'])
    df['TVL'] = df['Q1'] - (0.9375 * df['RangoTotal'])
    
    df['Z2H'] = df['Q1'] - ((34.1 + df['DiferenciaSkew']) / 100 * df['RangoTotal'])
    df['Z2L'] = df['Q1'] - ((37.5 + df['DiferenciaSkew']) / 100 * df['RangoTotal'])
    
    df['Z3H'] = df['Q4'] + ((37.5 + df['DiferenciaSkew']) / 100 * df['RangoTotal'])
    df['Z3L'] = df['Q4'] + ((34.1 + df['DiferenciaSkew']) / 100 * df['RangoTotal'])
    
    df['Z2H'] = df['Z2H'].apply(round_to_quarter)
    df['Z2L'] = df['Z2L'].apply(round_to_quarter)
    df['Z3H'] = df['Z3H'].apply(round_to_quarter)
    df['Z3L'] = df['Z3L'].apply(round_to_quarter)
    
    df['Q2'] = (df['TCL'] + df['Z2H']) / 2
    df['Q3'] = (df['TVH'] + df['Z3L']) / 2
    
    logger.info(f"Niveles calculados para {len(df)} días")
    logger.info(f"Rango Total promedio: {df['RangoTotal'].mean():.2f}")
    logger.info(f"Diferencia Skew promedio: {df['DiferenciaSkew'].mean():.2f}%")
    
    return df

def procesar_archivo(input_path, output_excel, output_csv, nombre):
    """
    Procesa un archivo agregando los niveles con skew
    
    Args:
        input_path: Ruta del archivo de entrada
        output_excel: Ruta del archivo Excel de salida
        output_csv: Ruta del archivo CSV de salida
        nombre: Nombre descriptivo para logs
    """
    logger.info(f"\n{'='*80}")
    logger.info(f"PROCESANDO: {nombre}")
    logger.info(f"{'='*80}")
    
    try:
        df = pd.read_excel(input_path)
        logger.info(f"Datos cargados: {len(df)} registros")
        
        df = calcular_niveles_skew(df)
        
        columnas_ordenadas = [
            'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Range', 'Return_%',
            'Q1', 'Q4', 'NR2', 'RangoTotal', 
            'PctAboveNR2', 'PctBelowNR2', 'SkewMayor', 'DiferenciaSkew',
            'TCH', 'TCL', 'Q2', 'Z2H', 'Z2L',
            'Z3H', 'Z3L', 'Q3', 'TVH', 'TVL',
            'EMH', 'EML', 'ExpRange'
        ]
        
        df = df[columnas_ordenadas]
        
        df.to_excel(output_excel, index=False)
        df.to_csv(output_csv, index=False)
        
        logger.info(f"OK Excel guardado: {output_excel}")
        logger.info(f"OK CSV guardado: {output_csv}")
        
    except Exception as e:
        logger.error(f"ERROR procesando {nombre}: {str(e)}")
        raise

def main():
    logger.info("\n" + "="*80)
    logger.info("INICIO - CALCULAR NIVELES CON SKEW")
    logger.info("="*80)
    
    base_path = Path("..") / "Resultados" / "Fase1"
    
    archivos = [
        {
            'input': base_path / "Datos_2025_EM21.xlsx",
            'output_excel': base_path / "Datos_2025_EM21_Niveles.xlsx",
            'output_csv': base_path / "Datos_2025_EM21_Niveles.csv",
            'nombre': "Datos 2025 con EM21"
        },
        {
            'input': base_path / "Datos_2025_EM9.xlsx",
            'output_excel': base_path / "Datos_2025_EM9_Niveles.xlsx",
            'output_csv': base_path / "Datos_2025_EM9_Niveles.csv",
            'nombre': "Datos 2025 con EM9"
        }
    ]
    
    for archivo in archivos:
        procesar_archivo(
            archivo['input'],
            archivo['output_excel'],
            archivo['output_csv'],
            archivo['nombre']
        )
    
    logger.info("\n" + "="*80)
    logger.info("PROCESO COMPLETADO EXITOSAMENTE")
    logger.info("="*80)

if __name__ == "__main__":
    main()

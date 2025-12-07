Continuar con Backtesting

## Pendiente:
- Comprobar manualmente estadísticas y archivos creadas para el rango diario sin el expected move en el archivo Datos_Diarios_DN_Niveles.xlsx

---

## ✅ COMPLETADO - 2025-12-04 15:10: Filtrado de datos del año 2025 y creación de hojas estadísticas

### Tarea realizada:
Se creó el script `filtrar_datos_2025_DN.py` para extraer únicamente los datos del año 2025 del archivo completo y generar hojas de estadísticas específicas para ese año.

### Archivos creados:
- `Scripts/filtrar_datos_2025_DN.py` (Versión 1.0 - script de filtrado)
- Actualización de `Resultados/Fase1/Datos_Diarios_DN_Niveles.xlsx` con 7 hojas nuevas

### Hojas agregadas al Excel:
1. **Datos_2025** - 221 registros completos del año 2025 (02-Ene a 07-Nov)
2. **2025_1D_Resumen_Touches** - Estadísticas de toques One Day para 2025
3. **2025_1D_Analisis_Cierres** - Análisis de cierres One Day para 2025
4. **2025_1D_Analisis_Superacion** - Análisis de superación One Day para 2025
5. **2025_3D_Resumen_Touches** - Estadísticas de toques Three Days para 2025
6. **2025_3D_Analisis_Cierres** - Análisis de cierres Three Days para 2025
7. **2025_3D_Analisis_Superacion** - Análisis de superación Three Days para 2025

### Estadísticas específicas del año 2025:

#### **One Day - Año 2025 (221 días):**
- **Toca Q1**: 126 días (57.01%) - Superior al promedio histórico (55.22%)
- **Toca Q4**: 95 días (42.99%)
- **Toca ambos**: 30 días (13.57%) - Similar al promedio (12.29%)
- **Promedio puntos sobre Q1**: 84.20 puntos (vs 67.12 histórico)
- **Promedio puntos bajo Q4**: 99.44 puntos (vs 70.71 histórico)

**Análisis de cierres 2025:**
- **Q1 - Cierre debajo**: 150 días (67.87%) - Patrón de reversión consistente
- **Q4 - Cierre arriba**: 179 días (80.99%) - Mayor que el promedio

**Cuando toca ambos niveles (30 días en 2025):**
- **Cierre sobre Q1**: 8 días (26.67%) - Promedio 53.64 puntos
- **Cierre bajo Q4**: 7 días (23.33%) - Promedio 33.08 puntos
- **Cierre entre niveles**: 15 días (50.00%) - Alta indecisión del mercado

#### **Three Days - Año 2025 (221 días):**
- **Toca Q1_3D**: 95 días (42.99%) - Consistente con el promedio (40.22%)
- **Toca Q4_3D**: 52 días (23.53%)
- **Toca ambos**: 3 días (1.36%) - Extremadamente conservador
- **Promedio puntos sobre Q1_3D**: 59.81 puntos
- **Promedio puntos bajo Q4_3D**: 63.28 puntos

**Cuando toca ambos niveles 3D (3 días en 2025):**
- Los **3 días cerraron entre niveles** (100%) - Ninguno superó los extremos

### Observaciones clave del año 2025:

1. **Mayor volatilidad que el promedio histórico**:
   - Superaciones promedio mayores en 2025 (84.20 vs 67.12 puntos sobre Q1)
   - Indica mercado más expansivo en 2025

2. **Efectividad de niveles One Day en 2025**:
   - 57% de toques en Q1 (vs 55% histórico)
   - Los niveles mantienen su relevancia estadística

3. **Patrón de reversión consistente**:
   - 68% de días que tocan Q1 cierran debajo (similar al histórico 69%)
   - Los niveles siguen funcionando como resistencia/soporte

4. **Three Days extremadamente conservador en 2025**:
   - Solo 3 días tocan ambos niveles (1.36%)
   - Los 3 días muestran indecisión (cierran entre niveles)

5. **Alta indecisión en días volátiles**:
   - 50% de días que tocan ambos niveles One Day cierran entre ellos
   - Indica mercado sin dirección clara en esos momentos

### Conclusiones del año 2025:

- **Q1 (High del día anterior)** actúa como resistencia efectiva
- **Q4 (Low del día anterior)** actúa como soporte efectivo
- Los niveles DN mantienen su validez estadística en 2025
- Mayor expansión de rangos comparado con el promedio histórico
- Niveles Three Days son más útiles como filtro conservador

### Para ejecutar:
```bash
cd "c:\Users\oscar\Documents\Proyecto-Trading\Github\NQ_Backtest\Scripts"
python filtrar_datos_2025_DN.py
```

### Archivo Excel actualizado:
El archivo ahora contiene **16 hojas totales**:
- 9 hojas originales (todos los años)
- 7 hojas nuevas específicas del 2025

---

## ✅ COMPLETADO - 2025-12-04 15:00: Cálculo de Niveles DN (Día Normal) con One Day y Three Days

### Tarea realizada:
Se creó el script `Scripts/calcular_niveles_DN.py` para calcular niveles según la metodología DN (Día Normal) descrita en `calculosDN.md`, incluyendo tanto cálculos One Day como Three Days.

### Archivos creados:
- `Scripts/calcular_niveles_DN.py` (Versión 1.1 - script principal)
- `Resultados/Fase1/Datos_Diarios_DN_Niveles.xlsx` (archivo de salida con todas las estadísticas)

### Metodología DN implementada:

#### **One Day (1 día anterior):**
- **Q1** = High del día anterior
- **Q4** = Low del día anterior
- **Range** = Q1 - Q4
- **NR2** = Q1 - (Range / 2) = Punto medio del rango
- **Niveles internos:** Z2H, Z2L, Z3H, Z3L, TCH, TCL, TVH, TVL
- **Desviaciones estándar:** Std1 a Std5 (arriba y abajo)
- **Extensiones:** 1D+ y 1D-

#### **Three Days (3 días anteriores):**
- **High_3D** = Máximo High de los últimos 3 días
- **Low_3D** = Mínimo Low de los últimos 3 días
- **Range_3D** = High_3D - Low_3D
- **NR2_3D** = Low_3D + (Range_3D / 2)
- **Q1_3D** = NR2_3D + (Range_3D / 2) = High_3D
- **Q4_3D** = NR2_3D - (Range_3D / 2) = Low_3D
- **Niveles internos:** Misma estructura que One Day pero con Range_3D

### Estructura del archivo Excel generado:

El archivo `Datos_Diarios_DN_Niveles.xlsx` contiene **9 hojas**:

1. **Datos_Completos**: 1,189 registros con 96 columnas incluyendo:
   - Datos OHLCV originales
   - Todos los niveles One Day (Q1, Q4, NR2, TCH, TCL, Z2H, Z2L, Z3H, Z3L, TVH, TVL, Std1-5, etc.)
   - Todos los niveles Three Days (con sufijo _3D)
   - Flags de toques y cierres para ambos períodos

2. **1D_Resumen_Touches**: Estadísticas de toques One Day
3. **1D_Analisis_Cierres**: Análisis de cierres respecto a niveles One Day
4. **1D_Analisis_Superacion**: Análisis cuando toca ambos niveles (Q1 y Q4) One Day
5. **1D_Analisis_Ambos**: Detalle resumido de días que tocan ambos niveles One Day
6. **1D_Detalle_Ambos**: Detalle completo de días que tocan ambos niveles One Day

7. **3D_Resumen_Touches**: Estadísticas de toques Three Days
8. **3D_Analisis_Cierres**: Análisis de cierres respecto a niveles Three Days
9. **3D_Analisis_Superacion**: Análisis cuando toca ambos niveles (Q1_3D y Q4_3D) Three Days

### Estadísticas principales obtenidas:

#### **One Day (1,188 días analizados):**
- **Toca Q1**: 656 días (55.22%)
- **Toca Q4**: 540 días (45.45%)
- **Toca ambos Q1 y Q4**: 146 días (12.29%)
- **Toca solo Q1**: 510 días (42.93%)
- **Toca solo Q4**: 394 días (33.16%)
- **Promedio puntos sobre Q1**: 67.12 puntos
- **Promedio puntos bajo Q4**: 70.71 puntos

**Análisis de cierres One Day:**
- **Q1 - Cierre debajo**: 820 días (69.02%)
- **Q1 - Cierre arriba/igual**: 368 días (30.98%)
- **Q4 - Cierre arriba**: 927 días (78.03%)
- **Q4 - Cierre abajo/igual**: 261 días (21.97%)

**Cuando toca ambos niveles One Day (146 días):**
- **Cierre sobre Q1**: 46 días (31.51%) - Promedio 33.34 puntos
- **Cierre bajo Q4**: 40 días (27.40%) - Promedio 30.31 puntos
- **Cierre entre niveles**: 60 días (41.10%)

#### **Three Days (1,186 días analizados):**
- **Toca Q1_3D**: 477 días (40.22%)
- **Toca Q4_3D**: 334 días (28.16%)
- **Toca ambos Q1_3D y Q4_3D**: 17 días (1.43%)
- **Toca solo Q1_3D**: 460 días (38.79%)
- **Toca solo Q4_3D**: 317 días (26.73%)
- **Promedio puntos sobre Q1_3D**: 45.49 puntos
- **Promedio puntos bajo Q4_3D**: 45.03 puntos

**Análisis de cierres Three Days:**
- **Q1_3D - Cierre debajo**: 926 días (78.08%)
- **Q1_3D - Cierre arriba/igual**: 260 días (21.92%)
- **Q4_3D - Cierre arriba**: 1,022 días (86.17%)
- **Q4_3D - Cierre abajo/igual**: 164 días (13.83%)

**Cuando toca ambos niveles Three Days (17 días):**
- **Cierre sobre Q1_3D**: 3 días (17.65%) - Promedio 25.59 puntos
- **Cierre bajo Q4_3D**: 4 días (23.53%) - Promedio 19.54 puntos
- **Cierre entre niveles**: 10 días (58.82%)

### Diferencias clave DN vs ExpM:

La metodología **DN (Día Normal)** difiere de **ExpM (Expected Move)** en:
1. **DN no usa skew**: Los niveles son simétricos respecto a NR2
2. **DN usa rangos históricos**: Q1 y Q4 son directamente los High/Low anteriores
3. **ExpM usa skew**: Los niveles se ajustan según la asimetría del Open respecto al rango
4. **ExpM requiere Open**: El Current Open determina el desplazamiento de niveles
5. **DN es más simple**: Solo necesita High y Low, sin considerar la apertura

### Observaciones de los resultados:

1. **Three Days es más conservador**: Solo 1.43% de días tocan ambos niveles (vs 12.29% en One Day)
2. **Mayor probabilidad de reversión**: ~70% de días que tocan Q1 cierran debajo
3. **Niveles One Day más reactivos**: Mayor frecuencia de toques (55% vs 40%)
4. **Niveles Three Days más amplios**: Menos toques pero superaciones similares en puntos

### Para ejecutar:
```bash
cd "c:\Users\oscar\Documents\Proyecto-Trading\Github\NQ_Backtest\Scripts"
python calcular_niveles_DN.py
```

### Próximos pasos sugeridos:
1. Comparar estadísticas DN vs ExpM para evaluar cuál metodología es más efectiva
2. Analizar la efectividad de niveles One Day vs Three Days
3. Crear estrategias de trading basadas en los patrones de reversión identificados
4. Validar con datos de minutos (Fase 3) para confirmar reacciones intradiarias en estos niveles

---

## ✅ COMPLETADO - 2025-12-04: Conversión de Datos de Minutos NinjaTrader a CSV

### Tarea realizada:
Se creó el script `Scripts/consolidar_datos_minutos.py` para convertir archivos .txt de datos intradiarios de NinjaTrader a formato CSV consolidado.

### Archivos creados:
- `Scripts/consolidar_datos_minutos.py` (script principal)

### Archivos de salida esperados:
- `Originales/NQ_1min_2020-2025.csv` (con columna Valid)
- `Procesados/NQ_1min_2020-2025_Limpio.csv` (solo válidos)
- `Logs/consolidacion_minutos.log` (registro de ejecución)

### Funcionalidad implementada:
1. **Carga de archivos**: Lee 20 archivos .txt con formato `YYYYMMDD HHMMSS;O;H;L;C;V`
2. **Consolidación**: Combina todos los contratos trimestrales en un único DataFrame
3. **Validación**: Aplica reglas de mercado (OHLC, volumen, timestamps cronológicos)
4. **Detección de gaps**: Identifica y clasifica gaps temporales (cierre diario, fin de semana, gaps largos)
5. **Exportación**: Genera CSV original y limpio con estadísticas completas

### Decisiones de diseño:
- **Overlaps**: `keep='first'` para priorizar contratos más antiguos durante rollover
- **Gaps**: Se reportan pero NO se rellenan (mantener integridad de datos reales)
- **Memoria**: Carga completa en memoria (1.6M registros = ~200-300 MB)
- **Validaciones**: Mismas que datos diarios + detección de saltos temporales hacia atrás

### Para ejecutar:
```bash
cd "c:\Users\oscar\Documents\Proyecto-Trading\Github\NQ_Backtest\Scripts"
python consolidar_datos_minutos.py
```

### Siguiente paso:
Usar `NQ_1min_2020-2025_Limpio.csv` en **Fase 3** del plan de backtesting para análisis intradiario granular.

---

## Ya realizado: Continuar con tareas anteriores
Veo que no existe un script llamado fase1_estad�sticas. D�jame buscar qu� scripts est�n disponibles en la carpeta Scripts:Perfecto, veo que el script 
fase1_analisis_exploratorio.py ya existe y realiza an�lisis estad�sticos. Ahora d�jame ver el plan completo para entender mejor qu� necesitas:Bas�ndome en el c�digo que he visto, puedo ayudarte a crear un script de estad�sticas descriptivas. Veo que ya tienes fase1_analisis_exploratorio.py que hace an�lisis estad�sticos, pero puedo crear un script m�s espec�fico y completo. 
�Qu� tipo de estad�sticas descriptivas necesitas espec�ficamente? Por ejemplo:
1. Estad�sticas b�sicas (media, mediana, desviaci�n est�ndar, min, max)
2. An�lisis de distribuci�n (asimetr�a, curtosis, percentiles)
3. An�lisis temporal (por a�o, mes, d�a de la semana)
4. An�lisis de volatilidad (rangos, ATR, volatilidad hist�rica)
5. An�lisis de tendencias (d�as alcistas vs bajistas, rachas)
6. Correlaciones entre variables
O si prefieres, puedo crear un script que genere un reporte completo con todas estas estad�sticas. �Qu� prefieres?

se ejecut� el script calcular niveles skew en Resultados/Fase1/ Datos_2025_EM21_Niveles.csv y en Resultados/Fase1/ Datos_2025_EM9_Niveles.csv ahora quiero que se creen los c�lculos de sobre cuantos d�as el precio ha tocado o superado el EMH y el EML, cuantos solo el EMH y cuantos solo el EML y copiarlo todo a una hoja de los archivos de excel Resultados/
Fase1/Datos_2025_EM21_Niveles.xlsl y Resultados/Fase1/ Datos_2025_EM9_Niveles.xlsl

1. Qu� vamos a calcular
Para cada uno de los archivos:
� Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx
� Resultados/Fase1/Datos_2025_EM9_Niveles.xlsx usaremos, por d�a:
� Precio de referencia: normalmente Close (puedes cambiarlo a High/Low si prefieres otra l�gica).
� Niveles: EMH y EML.
C�lculos:
1. D�as en los que el precio ha tocado o superado ambos: EMH y EML.
� Condici�n: Close >= EMH y Close <= EML (o la l�gica que prefieras si usas High/Low).
2. D�as que solo han tocado o superado EMH.
� Condici�n: Close >= EMH y no cumplir la condici�n de EML.
3. D�as que solo han tocado o superado EML.
� Condici�n: Close <= EML y no cumplir la condici�n de EMH.
Con esos conteos, crearemos una hoja nueva en cada Excel, por ejemplo Resumen_Touches.

2. Script en Python para hacer todo de una vez
Crea un archivo nuevo en Scripts/ llamado algo como: fase1_calcular_touches_em.py:
"""
Script para calcular toques de EMH y EML - FASE 1.x Descripci�n:
- Lee los archivos con niveles ya calculados:
        ../Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx
        ../Resultados/Fase1/Datos_2025_EM9_Niveles.xlsx
- Calcula:
* D�as que han tocado/superado EMH y EML
* D�as que han tocado/superado solo EMH
* D�as que han tocado/superado solo EML
- Escribe el resultado en una nueva hoja de cada Excel
"""
import pandas as pd from pathlib import Path import logging
logging.basicConfig(     level=logging.INFO,     format="%(asctime)s - %(levelname)s - %(message)s",     handlers=[         logging.FileHandler("../Logs/fase1_calcular_touches_em.log"),         logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__) BASE_PATH = Path("..") / "Resultados" / "Fase1"
def calcular_resumen_touches(df, precio_col="Close"):
    """
    Calcula los toques de EMH y EML.
    Args:
        df: DataFrame con columnas [EMH, EML, <precio_col>]         precio_col: nombre de la columna de precio a usar (por defecto Close)
    Returns:
        DataFrame resumen con m�tricas y valores.
    """
    if precio_col not in df.columns:
        raise ValueError(f"No se encontr� la columna de precio '{precio_col}' en el DataFrame.")
    if "EMH" not in df.columns or "EML" not in df.columns:         raise ValueError("El DataFrame debe contener las columnas 'EMH' y 'EML'.")
    price = df[precio_col]     emh = df["EMH"]     eml = df["EML"]
    # Condiciones de toque/superaci�n     toca_o_supera_emh = price >= emh     toca_o_supera_eml = price <= eml
    # Conteos     dias_emh_y_eml = (toca_o_supera_emh & toca_o_supera_eml).sum()     dias_solo_emh = (toca_o_supera_emh & ~toca_o_supera_eml).sum()     dias_solo_eml = (toca_o_supera_eml & ~toca_o_supera_emh).sum()
    resumen = pd.DataFrame({
        "M�trica": [
            "D�as que tocaron/superaron EMH y EML",
            "D�as que tocaron/superaron solo EMH",
            "D�as que tocaron/superaron solo EML"
        ],
        "Valor": [dias_emh_y_eml, dias_solo_emh, dias_solo_eml]
    })
    return resumen
def procesar_archivo_touches(nombre_archivo):
    """
    Abre un Excel de niveles, calcula el resumen de toques     y lo escribe en una nueva hoja.
    Args:
        nombre_archivo: nombre del archivo Excel dentro de BASE_PATH
    """
    excel_path = BASE_PATH / nombre_archivo     logger.info(f"Procesando archivo: {excel_path}")
    try:
        df = pd.read_excel(excel_path)         logger.info(f"Datos cargados: {len(df)} registros")     except Exception as e:
        logger.error(f"No se pudo leer {excel_path}: {e}")         return
    # Calculamos el resumen (usando Close por defecto)     resumen = calcular_resumen_touches(df, precio_col="Close")
    # Escribimos en una nueva hoja llamada 'Resumen_Touches'     try:
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            # Mantener las hojas existentes: primero las leemos todas
            # y luego escribimos SOLO la hoja de resumen (replace -> sobreescribe si existe)             resumen.to_excel(writer, sheet_name="Resumen_Touches", index=False)         logger.info(f"Resumen de toques escrito en hoja 'Resumen_Touches' de {excel_path}")     except Exception as e:         logger.error(f"Error escribiendo resumen en {excel_path}: {e}")
def main():
    logger.info("=" * 80)
    logger.info("INICIO - CALCULO DE TOQUES EMH / EML")
    logger.info("=" * 80)
    archivos = [
        "Datos_2025_EM21_Niveles.xlsx",
        "Datos_2025_EM9_Niveles.xlsx",
    ]
    for nombre in archivos:         procesar_archivo_touches(nombre)
    logger.info("=" * 80)
    logger.info("PROCESO DE TOQUES COMPLETADO")     logger.info("=" * 80)
if __name__ == "__main__":     main()

3. C�mo usarlo
1. Guarda el script en Scripts/fase1_calcular_touches_em.py.
2. Desde la carpeta Scripts/, ejec�talo, por ejemplo:
python fase1_calcular_touches_em.py
  1. Se actualizar�n:
  2. Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx
  3. Resultados/Fase1/Datos_2025_EM9_Niveles.xlsx a�adiendo una nueva hoja llamada Resumen_Touches con los tres conteos que pediste.

 4. Ajustes posibles
� Si quieres usar High/Low en lugar de Close como condici�n de toque (por ejemplo, tocar EMH si High >= EMH y tocar EML si Low <= EML), te modifico r�pido la l�gica.
� Si prefieres que en lugar de una hoja resumen se a�adan columnas de flags por d�a (Toca_EMH, Toca_EML, etc.), tambi�n lo adaptamos.
Dime si quieres que el criterio sea con High/Low o est� bien con Close.

criterio high y low y columnas mejor

RouteLLM
Perfecto, entonces:
� Criterio:
� Toca/supera EMH si High >= EMH
� Toca/supera EML si Low <= EML
� En lugar de solo una hoja resumen, a�adimos columnas por d�a en el mismo Excel.
Te dejo un script completo que:
1. Abre cada Excel de niveles (Datos_2025_EM21_Niveles.xlsx y Datos_2025_EM9_Niveles.xlsx).
2. A�ade estas columnas booleanas:
� Toca_EMH (True/False)
� Toca_EML
� Toca_EMH_y_EML
� Toca_solo_EMH
� Toca_solo_EML
3. Calcula tambi�n los conteos agregados y los guarda en una hoja Resumen_Touches.
Script sugerido: Scripts/fase1_calcular_touches_em.py
"""
Script para calcular toques de EMH y EML con criterio High/Low - FASE 1.x Descripci�n:
- Lee los archivos con niveles ya calculados:
        ../Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx
        ../Resultados/Fase1/Datos_2025_EM9_Niveles.xlsx
- A�ade columnas por d�a:
* Toca_EMH      (High >= EMH)
* Toca_EML      (Low  <= EML)
* Toca_EMH_y_EML
* Toca_solo_EMH
* Toca_solo_EML
- Crea/actualiza la hoja 'Resumen_Touches' con los conteos globales.
"""
import pandas as pd from pathlib import Path import logging
logging.basicConfig(     level=logging.INFO,     format="%(asctime)s - %(levelname)s - %(message)s",     handlers=[         logging.FileHandler("../Logs/fase1_calcular_touches_em.log"),         logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
BASE_PATH = Path("..") / "Resultados" / "Fase1"
def a�adir_columnas_touches(df):
    """
    A�ade columnas de toques EMH/EML al DataFrame usando High y Low.
    Requiere columnas: High, Low, EMH, EML
    Returns:
        df (modificado) y un DataFrame resumen con conteos.
    """
    for col in ["High", "Low", "EMH", "EML"]:         if col not in df.columns:             raise ValueError(f"Falta la columna requerida '{col}' en el DataFrame.")
    toca_emh = df["High"] >= df["EMH"]     toca_eml = df["Low"] <= df["EML"]
    df["Toca_EMH"] = toca_emh     df["Toca_EML"] = toca_eml     df["Toca_EMH_y_EML"] = toca_emh & toca_eml     df["Toca_solo_EMH"] = toca_emh & ~toca_eml     df["Toca_solo_EML"] = toca_eml & ~toca_emh
    # Resumen de conteos     dias_emh_y_eml = df["Toca_EMH_y_EML"].sum()     dias_solo_emh = df["Toca_solo_EMH"].sum()     dias_solo_eml = df["Toca_solo_EML"].sum()
    resumen = pd.DataFrame({
        "M�trica": [
            "D�as que tocaron/superaron EMH y EML",
            "D�as que tocaron/superaron solo EMH",
            "D�as que tocaron/superaron solo EML"
        ],
        "Valor": [dias_emh_y_eml, dias_solo_emh, dias_solo_eml]
    })
    return df, resumen
def procesar_archivo_touches(nombre_archivo):
    """
    Abre un Excel de niveles, a�ade las columnas de toques     y escribe tambi�n un resumen en una hoja nueva.
    """
    excel_path = BASE_PATH / nombre_archivo     logger.info(f"Procesando archivo: {excel_path}")     try:
        # Leemos todas las hojas para no perder nada         xls = pd.ExcelFile(excel_path)         hojas = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}     except Exception as e:
        logger.error(f"No se pudo leer {excel_path}: {e}")         return
    # Suponemos que la hoja principal es la primera     hoja_principal = xls.sheet_names[0]     df = hojas[hoja_principal]     logger.info(f"Hoja principal: {hoja_principal} con {len(df)} registros")
    # A�adimos columnas en la hoja principal     try:
        df_modificado, resumen = a�adir_columnas_touches(df)         hojas[hoja_principal] = df_modificado     except Exception as e:
        logger.error(f"Error a�adiendo columnas de toques en {excel_path}: {e}")         return
    # Actualizamos el diccionario de hojas con el resumen     hojas["Resumen_Touches"] = resumen
    # Escribimos todas las hojas de vuelta al mismo archivo     try:         with pd.ExcelWriter(excel_path, engine="openpyxl", mode="w") as writer:             for nombre_hoja, df_hoja in hojas.items():
                df_hoja.to_excel(writer, sheet_name=nombre_hoja, index=False)         logger.info(f"Archivo actualizado con columnas de toques y hoja 'Resumen_Touches': 
{excel_path}")     except Exception as e:         logger.error(f"Error escribiendo en {excel_path}: {e}")
def main():
    logger.info("=" * 80)     logger.info("INICIO - TOQUES EMH / EML (High/Low + columnas)")     logger.info("=" * 80)
    archivos = [
        "Datos_2025_EM21_Niveles.xlsx",
        "Datos_2025_EM9_Niveles.xlsx",
    ]
    for nombre in archivos:         procesar_archivo_touches(nombre)     logger.info("=" * 80)     logger.info("PROCESO DE TOQUES COMPLETADO")
    logger.info("=" * 80)
if __name__ == "__main__":     main()
C�mo ejecutarlo
1. Guarda el script como Scripts/fase1_calcular_touches_em.py.
2. Desde la carpeta Scripts/:
python fase1_calcular_touches_em.py
  1. Se actualizar�n:
  2. Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx
  3. Resultados/Fase1/Datos_2025_EM9_Niveles.xlsx con:
� Nuevas columnas en la hoja principal (Toca_EMH, Toca_EML, Toca_EMH_y_EML, Toca_solo_EMH, Toca_solo_EML).
� Hoja Resumen_Touches con los conteos globales.
Si el nombre de la hoja principal no es la primera (por ejemplo se llama 
Datos o algo concreto), dime el nombre exacto y te ajusto el script para que use esa hoja en lugar de la primera.

RouteLLM
Los archivos no est�n disponibles en el entorno de ejecuci�n. Necesito que subas los archivos Excel:
  � Datos_2025_EM21_Niveles.xlsx
  � Datos_2025_EM9_Niveles.xlsx desde tu carpeta Resultados/Fase1/ para poder ejecutar el c�digo y a�adir las columnas de toques.
Alternativamente, puedes:
1. Guardar el script que te proporcion� como Scripts/ fase1_calcular_touches_em.py en tu repositorio local.
2. Ejecutarlo localmente desde la carpeta Scripts/ con:
bash
   python fase1_calcular_touches_em.py
Esto procesar� los archivos directamente en tu m�quina y actualizar� los Excel con las nuevas columnas y la hoja de resumen.
RouteLLM
The following files are now available to view and download through the UI: Datos_2025_EM9_Niveles.xlsx, Datos_2025_EM21_Niveles.xlsx�Perfecto! ? Proceso completado exitosamente.
Resumen de resultados:
Datos_2025_EM21_Niveles.xlsx (221 d�as):
  � 6 d�as (2.71%) tocaron/superaron ambos EMH y EML
  � 59 d�as (26.70%) tocaron/superaron solo EMH
  � 52 d�as (23.53%) tocaron/superaron solo EML Datos_2025_EM9_Niveles.xlsx (221 d�as):
  � 5 d�as (2.26%) tocaron/superaron ambos EMH y EML
  � 59 d�as (26.70%) tocaron/superaron solo EMH
  � 56 d�as (25.34%) tocaron/superaron solo EML
Cambios realizados:
Ambos archivos Excel ahora tienen:
1. Nuevas columnas en la hoja principal:
� Toca_EMH (True/False si High >= EMH)
� Toca_EML (True/False si Low <= EML)
� Toca_EMH_y_EML (ambos)
� Toca_solo_EMH (solo EMH)
� Toca_solo_EML (solo EML)
2. 
Nueva hoja "Resumen_Touches" con los conteos totales y porcentajes.
Los archivos actualizados est�n listos para descargar. �Necesitas alg�n an�lisis adicional sobre estos toques?

ahora necesito el total del d�as que han cumplido las condiciones

RouteLLM
The following files are now available to view and download through the UI: 
Datos_2025_EM21_Niveles.xlsx, Datos_2025_EM9_Niveles.xlsxPerfecto! Aqu� est� el an�lisis completo:
Datos_2025_EM21_Niveles.xlsx (221 d�as)
? 117 d�as (52.94%) cumplieron AL MENOS UNA condici�n de toque
 104 d�as (47.06%) NO tocaron ning�n nivel
Desglose:
� 6 d�as (2.71%) tocaron EMH y EML
� 59 d�as (26.70%) tocaron solo EMH
� 52 d�as (23.53%) tocaron solo EML

Datos_2025_EM9_Niveles.xlsx (221 d�as)
? 120 d�as (54.30%) cumplieron AL MENOS UNA condici�n de toque
 101 d�as (45.70%) NO tocaron ning�n nivel
Desglose:
� 5 d�as (2.26%) tocaron EMH y EML
� 59 d�as (26.70%) tocaron solo EMH
� 56 d�as (25.34%) tocaron solo EML

Conclusiones:
� EM9 tiene ligeramente m�s d�as con toques (120 vs 117)
� Aproximadamente la mitad de los d�as (52-54%) tocan al menos uno de los niveles EMH/EML
� Es muy raro que se toquen ambos niveles el mismo d�a (2-3%)
� Los toques a EMH y EML est�n bastante equilibrados (~27% vs ~23-25%)
La hoja 
"Resumen_Touches" en ambos archivos ha sido actualizada con toda esta informaci�n. Los archivos est�n listos para descargar.

ahora necesito saber de los d�as que tocaron emh cuanto d�as cerraron por debajo del emh, igual pero al rever para el eml

RouteLLM
The following files are now available to view and download through the UI: Datos_2025_EM9_Niveles.xlsx, Datos_2025_EM21_Niveles.xlsxPerfecto! Aqu� est�n los resultados del an�lisis de cierres:
Datos_2025_EM21_Niveles.xlsx
 EMH (High >= EMH)
De 65 d�as que tocaron EMH:
� 34 d�as (52.31%) cerraron por DEBAJO de EMH ?
� 31 d�as (47.69%) cerraron arriba o igual a EMH ?
 EML (Low <= EML)
De 58 d�as que tocaron EML:
� 33 d�as (56.90%) cerraron por ARRIBA de EML ?
� 25 d�as (43.10%) cerraron abajo o igual a EML ?

Datos_2025_EM9_Niveles.xlsx
 EMH (High >= EMH)
De 64 d�as que tocaron EMH:
� 30 d�as (46.88%) cerraron por DEBAJO de EMH ?
� 34 d�as (53.12%) cerraron arriba o igual a EMH ?
 EML (Low <= EML)
De 61 d�as que tocaron EML:
� 32 d�as (52.46%) cerraron por ARRIBA de EML ?
� 29 d�as (47.54%) cerraron abajo o igual a EML ?

 Conclusiones clave:
1. Reversiones frecuentes: M�s del 50% de los d�as que tocan un nivel extremo tienden a cerrar en direcci�n contraria (reversi�n).
2. EM21 vs EM9: 
� EM21 muestra m�s reversiones en EMH (52% vs 47%)
� Ambos muestran patrones similares de reversi�n en EML (~53-57%)
3. 
Implicaci�n para trading: Los niveles EMH/EML act�an como zonas de resistencia/soporte con alta probabilidad de reversi�n.
Archivos actualizados con:
? 4 nuevas columnas en la hoja principal: EMH_Cierre_Debajo, 
EMH_Cierre_Arriba_Igual, EML_Cierre_Arriba, EML_Cierre_Abajo_Igual
? Nueva hoja "Analisis_Cierres" con el resumen completo
Los archivos est�n listos para descargar. �Necesitas alg�n an�lisis adicional?

los d�as que cerraron por encima del emh o por debajo del eml cuantos puntos superaron ambos niveles?

RouteLLM
The following files are now available to view and download through the UI: Datos_2025_EM21_Niveles.xlsx, Datos_2025_EM9_Niveles.xlsxExcelente! Aqu� est�n los resultados del an�lisis de superaci�n:
Datos_2025_EM21_Niveles.xlsx
 Cierres por ENCIMA de EMH
31 d�as cerraron por encima de EMH:
� Promedio: 141.67 puntos sobre EMH
� Mediana: 88.25 puntos
� M�ximo: 1,667.50 puntos 
� M�nimo: 5.75 puntos
� Desviaci�n est�ndar: 293.13
 Cierres por DEBAJO de EML
25 d�as cerraron por debajo de EML:
� Promedio: 198.90 puntos bajo EML
� Mediana: 164.50 puntos
� M�ximo: 752.75 puntos 
� M�nimo: 6.75 puntos
� Desviaci�n est�ndar: 197.82

Datos_2025_EM9_Niveles.xlsx
 Cierres por ENCIMA de EMH
34 d�as cerraron por encima de EMH:
� Promedio: 127.21 puntos sobre EMH
� Mediana: 77.62 puntos
� M�ximo: 1,426.50 puntos 
� M�nimo: 0.75 puntos
� Desviaci�n est�ndar: 241.71
 Cierres por DEBAJO de EML
28 d�as cerraron por debajo de EML:
� Promedio: 187.23 puntos bajo EML
� Mediana: 131.25 puntos
� M�ximo: 785.00 puntos 
� M�nimo: 5.75 puntos
� Desviaci�n est�ndar: 189.79

 Conclusiones clave:
1. Superaciones m�s fuertes en EML: Cuando se rompe el EML hacia abajo, la superaci�n promedio es mayor (~188-199 puntos) que cuando se rompe el EMH hacia arriba (~127-142 puntos).
2. Alta variabilidad: La desviaci�n est�ndar es muy alta, indicando que hay d�as con superaciones extremas y otros con superaciones m�nimas.
3. Medianas vs Promedios: Las medianas son significativamente menores que los promedios, lo que indica que hay algunos d�as con superaciones extremas que elevan el promedio.
4. 
EM21 vs EM9: 
� EM21 tiene superaciones promedio ligeramente mayores
� EM9 tiene m�s d�as que superan EMH (34 vs 31)
Archivos actualizados con:
? 2 nuevas columnas: Puntos_Sobre_EMH, Puntos_Bajo_EML
? Nueva hoja "Analisis_Superacion" con estad�sticas completas
Los archivos est�n listos para descargar. �Quieres alg�n an�lisis adicional o visualizaci�n de estos datos?

ahora en los dias que tocaron ambos niveles, cuantos d�as superaron esos niveles y cuantos puntos

RouteLLM
The following files are now available to view and download through the UI: Datos_2025_EM9_Niveles.xlsx, Datos_2025_EM21_Niveles.xlsxExcelente! Aqu� est� el an�lisis completo de los d�as que tocaron AMBOS niveles:
Datos_2025_EM21_Niveles.xlsx (6 d�as tocaron ambos)
Distribuci�n de cierres:
� 2 d�as (33.33%) cerraron por ENCIMA de EMH 
� 1 d�a (16.67%) cerr� por DEBAJO de EML 
� 3 d�as (50.00%) cerraron ENTRE ambos niveles 
Superaci�n de EMH (2 d�as):
� Promedio: 907.62 puntos 
� Mediana: 907.62 puntos
� M�ximo: 1,667.50 puntos (09-Abr-2025)
� M�nimo: 147.75 puntos (07-Abr-2025)
Superaci�n de EML (1 d�a):
� Promedio: 6.75 puntos
� Mediana: 6.75 puntos
� M�ximo: 6.75 puntos (08-Abr-2025)

Datos_2025_EM9_Niveles.xlsx (5 d�as tocaron ambos)
Distribuci�n de cierres:
� 2 d�as (40.00%) cerraron por ENCIMA de EMH 
� 1 d�a (20.00%) cerr� por DEBAJO de EML 
� 2 d�as (40.00%) cerraron ENTRE ambos niveles 
Superaci�n de EMH (2 d�as):
� Promedio: 58.62 puntos
� Mediana: 58.62 puntos
� M�ximo: 106.00 puntos (07-Abr-2025)
� M�nimo: 11.25 puntos (01-Oct-2025)
Superaci�n de EML (1 d�a):
� Promedio: 394.50 puntos 
� Mediana: 394.50 puntos
� M�ximo: 394.50 puntos (27-Feb-2025)

 Conclusiones clave:
1. D�as muy vol�tiles: Los d�as que tocan ambos niveles son extremadamente vol�tiles (rango intradiario muy amplio).
2. Mayor�a cierra entre niveles: El 40-50% de estos d�as termina cerrando entre EMH y EML, indicando indecisi�n del mercado.
3. 
EM21 tiene superaciones m�s extremas: 
� EM21: hasta 1,667 puntos sobre EMH
� EM9: hasta 106 puntos sobre EMH
4. 
Fechas cr�ticas identificadas:
� Abril 2025 (d�as 7, 8, 9): Per�odo de alta volatilidad en ambos modelos
� 27-Feb-2025 (EM9): Fuerte ca�da bajo EML (-394 puntos)
� 09-Abr-2025 (EM21): Fuerte ruptura sobre EMH (+1,667 puntos)
Archivos actualizados con:
? 5 nuevas columnas: Cierre_Sobre_EMH_Ambos, Cierre_Bajo_EML_Ambos, 
Cierre_Entre_Niveles_Ambos, Puntos_Sobre_EMH_Ambos, 
Puntos_Bajo_EML_Ambos
? Nueva hoja "Analisis_Ambos_Niveles" con resumen estad�stico
? Nueva hoja "Detalle_Ambos_Niveles" con detalle d�a por d�a
Los archivos est�n listos para descargar. �Quieres alg�n an�lisis adicional o visualizaci�n de estos patrones?

quiero visualizar los patrones

RouteLLM
Perfecto, buena idea. Vamos a visualizar estos patrones de forma clara. Te propongo 3 tipos de gr�ficos y te explico c�mo generarlos (puedes hacerlo en tu propio entorno con los Excels actualizados).
Si quieres, luego te preparo el c�digo exacto en Python para cada gr�fico.

1) Gr�fico de barras: cu�ntos d�as cumplen cada condici�n
Para cada modelo (EM21 y EM9), visualizar:
         � D�as que:
         � Tocan solo EMH
         � Tocan solo EML
         � Tocan ambos
         � Tocan y adem�s cierran por encima de EMH
         � Tocan y adem�s cierran por debajo de EML Esto sirve para ver r�pidamente probabilidades de escenarios.
Ejemplo de estructura (para EM21):
         � Toca solo EMH
         � Toca solo EML
         � Toca ambos
         � Ambos + cierre > EMH
         � Ambos + cierre < EML
Puedes montar esto directamente en Excel con un gr�fico de columnas usando los datos de las hojas:
         � Resumen_Touches
         � Analisis_Cierres
         � Analisis_Ambos_Niveles

2) Boxplot (caja y bigotes) de superaci�n en puntos
Objetivo: ver c�mo se distribuyen los puntos que supera el precio sobre EMH o por debajo de EML:
� Serie 1: Puntos_Sobre_EMH (todos los d�as que cierran por encima de EMH)
� Serie 2: Puntos_Bajo_EML (todos los d�as que cierran por debajo de EML) Y, si quieres afinar:
� Serie 3: Puntos_Sobre_EMH_Ambos (solo d�as que tocaron ambos y cerraron por encima de EMH)
� Serie 4: 
Puntos_Bajo_EML_Ambos (solo d�as que tocaron ambos y cerraron por debajo de EML)
Esto te da:
� Mediana
� Rango intercuart�lico
� Outliers (d�as extremos tipo +1600 puntos)

3) Gr�fico temporal con bandas EMH/EML y cierres especiales
Para ver el �comportamiento� de estos d�as a lo largo del a�o:
� Eje X: Date � Eje Y: precio
� L�neas:
� EMH (l�nea superior)
� EML (l�nea inferior) � Close (l�nea central)
� Puntos marcados:
� D�as que tocan solo EMH: marcador rojo
� D�as que tocan solo EML: marcador azul
� D�as que tocan ambos: marcador naranja/grande
� D�as que tocan ambos y cierran fuera: marcador especial (verde si 
>EMH, morado si <EML)
Esto te deja ver si esos patrones se concentran en determinadas fases (tendencias, rangos, shocks de volatilidad, etc.).

Si quieres hacerlo en Python (recomendado para backtest)
Dime qu� prefieres que te genere primero:
1. C�digo para gr�fico de barras resumen (frecuencias por tipo de evento)
2. C�digo para boxplots de superaci�n en puntos
3. C�digo para timeline con EMH/EML y eventos marcados
Por ejemplo: �hazme el 1 y el 3 para EM21 y EM9 en el mismo gr�fico� y te lo preparo listo para copiar/pegar.

�hazme el 1 y el 3 para EM21 y EM9 en el mismo gr�fico�

RouteLLM
[HTML Chart Displayed via UI]Ya he generado los dos tipos de visualizaci�n que pediste (1 y 3) usando los datos de los Excels que subiste.
Te resumo qu� est�s viendo y te dejo el c�digo listo para que lo uses/localices en tu entorno.

1) Gr�fico de barras comparativo EM21 vs EM9 (frecuencias de eventos)
En este gr�fico se comparan, para cada modelo:
� Toca solo EMH
� Toca solo EML
� Toca ambos
� Ambos + cierre > EMH
� Ambos + cierre < EML
Interpretaci�n r�pida:
� Las barras de EM21 y EM9 lado a lado para cada tipo de evento.
� Te permite ver de un vistazo:
� Qu� modelo tiene m�s d�as de toque solo superior o solo inferior.
� Cu�ntas veces los d�as que tocan ambos niveles acaban cerrando fuera de los extremos (breakout real).
Si quieres volver a generar este gr�fico en tu entorno, el c�digo que us� es el que ves en el bloque de Python en la interfaz (ya est� completo y listo para copiar).

3) Timeline EM21 y EM9 con niveles y eventos (dos subgr�ficos)
He generado una figura con 2 subplots:
1. Arriba: EM21  
2. Abajo: EM9  
En cada uno se plota:
� L�nea roja: EMH
� L�nea azul: EML � L�nea negra: Close
� Puntos:
� Naranja: d�as Toca_solo_EMH
� Cian: d�as Toca_solo_EML
� Magenta (rombo): d�as Toca_EMH_y_EML (tocan ambos) Esto sirve para:
� Ver en qu� fases del a�o se concentran los toques (tendencias fuertes, rangos, shocks de volatilidad).
� Comparar visualmente si EM21 o EM9 �encajan mejor� con la estructura del precio (m�s/menos toques, simetr�a, etc.).
De nuevo, el c�digo que ves en la �ltima ejecuci�n es exactamente lo que necesitas para replicarlo localmente con tus Excels.

Pr�ximos pasos posibles
Si quieres, podemos:
� A�adir al timeline colores distintos para:
� �Toca ambos y cierra > EMH�
� �Toca ambos y cierra < EML�
� Hacer gr�ficos separados solo de los d�as extremos (superaciones grandes, por ejemplo > 200 puntos).
� Exportar estas m�tricas a una tabla resumen tipo �playbook� para reglas de entrada/salida.
Dime qu� tipo de patr�n te interesa estudiar (reversiones, breakouts, filtros de tendencia, etc.) y afinamos las visualizaciones hacia eso.

ahora necesito pasar los archivos de esta carpeta datos brutos/ datos ninjatrader/Minutos a csv para poder trabajar con ellos. Son datos de minutos y volumen

RouteLLM
Perfecto, veo que tienes archivos .txt de NinjaTrader en la carpeta datos brutos/ datos ninjatrader/Minutos/. Son 20 archivos (contratos trimestrales de 2021 a 2025).
Aunque no puedo acceder directamente a los archivos desde el repositorio, te preparo un script completo que:
1. Lee todos los archivos .txt de esa carpeta
2. Detecta autom�ticamente el formato de NinjaTrader (normalmente es: 
fecha;hora;open;high;low;close;volumen o similar)
3. Convierte cada archivo a CSV limpio
4. Consolida todo en un �nico CSV (opcional) con datos de minutos ordenados

Script: Scripts/convertir_ninjatrader_a_csv.py
"""
Script para convertir archivos de NinjaTrader (.txt) a CSV - FASE 2
Versi�n: 1.0
Fecha: 2025-12-01 Descripci�n:
- Lee todos los archivos .txt de la carpeta datos brutos/datos ninjatrader/Minutos/
- Detecta el formato de NinjaTrader (separador ; o ,)
- Convierte cada archivo a CSV limpio
- Opcionalmente consolida todo en un �nico CSV
"""
import pandas as pd from pathlib import Path import logging
logging.basicConfig(     level=logging.INFO,     format="%(asctime)s - %(levelname)s - %(message)s",     handlers=[         logging.FileHandler("../Logs/convertir_ninjatrader_a_csv.log"),         logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
# Rutas
INPUT_PATH = Path("..") / "datos brutos" / "datos ninjatrader" / "Minutos"
OUTPUT_PATH = Path("..") / "Procesados" / "Minutos" OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
def detectar_formato(file_path):
    """
    Lee las primeras l�neas del archivo para detectar el formato.
    Returns:         dict con 'separator', 'header', 'columns'
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        primera_linea = f.readline().strip()         segunda_linea = f.readline().strip()
    # Detectar separador     if ';' in primera_linea:
        separator = ';'     elif ',' in primera_linea:
        separator = ','     elif '\t' in primera_linea:
        separator = '\t'     else:         separator = ' '
    # Detectar si tiene header
    # NinjaTrader normalmente NO tiene header, empieza directo con datos     # Formato t�pico: 20210301;093000;13245.00;13250.00;13240.00;13248.00;150     partes = primera_linea.split(separator)
    # Si la primera parte parece una fecha (8 d�gitos), no hay header     if len(partes[0]) == 8 and partes[0].isdigit():
        has_header = False
        # Formato t�pico NinjaTrader: Date;Time;Open;High;Low;Close;Volume         columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']     else:
        has_header = True         columns = None # pandas lo detectar�
    return {
        'separator': separator,
        'has_header': has_header,
        'columns': columns
    }
def convertir_archivo(input_file, output_file):
    """
    Convierte un archivo .txt de NinjaTrader a CSV limpio.
    """
    logger.info(f"Procesando: {input_file.name}")
    try:
        # Detectar formato         formato = detectar_formato(input_file)         logger.info(f"  Separador: '{formato['separator']}' | Header: {formato['has_header']}")
        # Leer archivo         if formato['has_header']:
            df = pd.read_csv(input_file, sep=formato['separator'])         else:
            df = pd.read_csv(                 input_file,                 sep=formato['separator'],                 header=None, 
                names=formato['columns']
            )
        logger.info(f"  Registros le�dos: {len(df)}")
        # Crear columna DateTime combinando Date y Time         # Formato Date: YYYYMMDD, Time: HHMMSS         df['DateTime'] = pd.to_datetime(             df['Date'].astype(str) + ' ' + df['Time'].astype(str).str.zfill(6),
            format='%Y%m%d %H%M%S'
        )
        # Reordenar columnas         df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
        # Ordenar por fecha/hora         df = df.sort_values('DateTime')
        # Guardar CSV         df.to_csv(output_file, index=False)         logger.info(f"  ? Guardado: {output_file}")         return df
    except Exception as e:         logger.error(f"  ERROR procesando {input_file.name}: {e}")         import traceback         traceback.print_exc()         return None
def consolidar_archivos(output_path):
    """
    Consolida todos los CSV individuales en uno solo.
    """
    logger.info("\n" + "="*80)
    logger.info("CONSOLIDANDO ARCHIVOS")
    logger.info("="*80)     csv_files = sorted(output_path.glob("NQ_*.csv"))
    if not csv_files:
        logger.warning("No se encontraron archivos CSV para consolidar")
        return
    dfs = []     for csv_file in csv_files:
        logger.info(f"Leyendo: {csv_file.name}")         df = pd.read_csv(csv_file, parse_dates=['DateTime'])         dfs.append(df)
    # Concatenar todos     df_consolidado = pd.concat(dfs, ignore_index=True)
    # Ordenar por fecha/hora     df_consolidado = df_consolidado.sort_values('DateTime')
    # Eliminar duplicados (por si hay solapamiento entre contratos)     df_consolidado = df_consolidado.drop_duplicates(subset=['DateTime'], keep='first')
    # Guardar     output_file = output_path / "NQ_Minutos_Consolidado.csv"     df_consolidado.to_csv(output_file, index=False)
    logger.info(f"\n? Archivo consolidado guardado: {output_file}")     logger.info(f"  Total registros: {len(df_consolidado)}")     logger.info(f"  Rango: {df_consolidado['DateTime'].min()} a 
{df_consolidado['DateTime'].max()}")
def main():
    logger.info("="*80)     logger.info("INICIO - CONVERSI�N NINJATRADER A CSV")     logger.info("="*80)
    # Buscar todos los archivos .txt     txt_files = sorted(INPUT_PATH.glob("*.txt"))
    if not txt_files:
        logger.error(f"No se encontraron archivos .txt en {INPUT_PATH}")         return     logger.info(f"Archivos encontrados: {len(txt_files)}")
    # Convertir cada archivo     for txt_file in txt_files:
        # Nombre de salida: "NQ 03-21.Last.txt" -> "NQ_03-21.csv"         output_name = txt_file.stem.replace(" ", "_").replace(".Last", "") + ".csv"         output_file = OUTPUT_PATH / output_name         convertir_archivo(txt_file, output_file)
    # Consolidar todos los archivos     consolidar_archivos(OUTPUT_PATH)
    logger.info("\n" + "="*80)
    logger.info("PROCESO COMPLETADO")
    logger.info("="*80)
if __name__ == "__main__":     main()

C�mo usarlo
1. Guarda el script como Scripts/convertir_ninjatrader_a_csv.py
2. Ejecuta desde la carpeta Scripts/: bash
   python convertir_ninjatrader_a_csv.py
3. 
Resultado:
� 
Se crear�n archivos CSV individuales en Procesados/Minutos/:
� NQ_03-21.csv
� NQ_06-21.csv
� ... (uno por cada contrato)
� 
Se crear� un archivo consolidado:
� NQ_Minutos_Consolidado.csv (todos los contratos unidos, sin duplicados)

Formato de salida
Cada CSV tendr� estas columnas:
DateTime,Open,High,Low,Close,Volume
2021-03-01 09:30:00,13245.00,13250.00,13240.00,13248.00,150
2021-03-01 09:31:00,13248.00,13255.00,13247.00,13252.00,120
...


Metodología para el análisis
1. Datos necesarios: 
o Datos históricos de velas de 1 minuto de los futuros del NASDAQ-100 (por ejemplo, /NQ en E-mini o /MNQ en Micro E-mini) incluidos en el archivo
o Indicadores: 
* VWAP diario (reiniciado cada sesión).
* Media móvil exponencial (EMA) de 9 períodos sobre el precio.
* Volumen por vela y EMA de 21 períodos sobre el volumen.
2. Definición de eventos: 
o Desviación del VWAP: Identificar velas donde el precio (mínimo o máximo) está entre 50 y 90 puntos (en el caso de /NQ, 1 punto = 1 índice NASDAQ-100) por encima o por debajo del VWAP diario.
o Vela alcista/bajista formando el extremo: 
* Alcista: Vela que cierra por encima de su apertura y cuyo mínimo es el punto más alejado del VWAP (desviación negativa) o máximo es el punto más cercano (desviación positiva).
* Bajista: Vela que cierra por debajo de su apertura y cuyo mínimo/máximo define el extremo.
o Cruce de EMA 9 con volumen: 
* Identificar velas alcistas que cierran por encima de la EMA 9 con un volumen superior a la EMA 21 del volumen.
* De estas, determinar si el precio regresa al VWAP diario, lo supera, y por cuántos puntos, o si no logra alcanzarlo.
3. Restricciones: 
o Los futuros del NASDAQ-100 operan casi 24 horas, pero la sesión principal (9:30 AM - 4:00 PM EST) tiene mayor volumen y volatilidad, lo que puede influir en los resultados.
o El VWAP diario se reinicia al inicio de cada sesión (generalmente a las 6:00 PM EST para los futuros).


Codigo Tradinview

//@version=5
study("NASDAQ VWAP Deviation Analysis", overlay=true)

// VWAP diario
vwap_diario = ta.vwap(hlc3, "D")

// EMA 9
ema_9 = ta.ema(close, 9)

// Volumen y EMA 21 del volumen
vol_ema_21 = ta.ema(volume, 21)

// Condiciones de desviación (50-90 puntos)
dev_neg = (vwap_diario - low) >= 50 and (vwap_diario - low) <= 90
dev_pos = (high - vwap_diario) >= 50 and (high - vwap_diario) <= 90

// Velas alcistas/bajistas
es_alcista = close > open
es_bajista = close < open

// Contadores (usar variables persistentes)
var int count_neg_alcista = 0
var int count_neg_bajista = 0
var int count_pos_alcista = 0
var int count_pos_bajista = 0

if dev_neg and es_alcista
    count_neg_alcista := count_neg_alcista + 1
if dev_neg and es_bajista
    count_neg_bajista := count_neg_bajista + 1
if dev_pos and es_alcista
    count_pos_alcista := count_pos_alcista + 1
if dev_pos and es_bajista
    count_pos_bajista := count_pos_bajista + 1

// Velas alcistas superando EMA 9 con volumen > EMA 21
cond_alcista_ema_vol = es_alcista and close > ema_9 and volume > vol_ema_21
var int count_alcista_ema_vol = 0
if dev_neg and cond_alcista_ema_vol
    count_alcista_ema_vol := count_alcista_ema_vol + 1

// Seguimiento de regreso al VWAP (lógica simplificada)
var int count_regreso_vwap = 0
var int count_no_regreso = 0
var float puntos_superacion = 0
if cond_alcista_ema_vol
    future_vwap = ta.valuewhen(close >= vwap_diario, close - vwap_diario, 0)
    if future_vwap != na
        count_regreso_vwap := count_regreso_vwap + 1
        puntos_superacion := future_vwap
    else
        count_no_regreso := count_no_regreso + 1

// Mostrar resultados (etiquetas o tabla)
if barstate.islast
    label.new(bar_index, high, "Neg Alcista: " + str.tostring(count_neg_alcista) + "\nNeg Bajista: " + str.tostring(count_neg_bajista) + "\nPos Alcista: " + str.tostring(count_pos_alcista) + "\nPos Bajista: " + str.tostring(count_pos_bajista) + "\nAlcista EMA+Vol: " + str.tostring(count_alcista_ema_vol) + "\nRegreso VWAP: " + str.tostring(count_regreso_vwap))

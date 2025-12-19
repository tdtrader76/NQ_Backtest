Idea para backtesting basada en paper Push-response anomalies in high-frequency S&P 500 price series

 - Según el paper, siempre que hay un impulso ámplio en pocos minutos este revertirá de manera significativa,
   pero hay que esperar un tiempo para ver que esto pasa. Lado correcto de la V?
 - Identifica movimiento fuerte como recorrido de más de 3 desviaciones estandar  
 - Desviaciones estandar se miden del movimiento, si este tiene 400 ticks o 100 puntos usan formula de 
   impulso - media / desviación estandar (crear calculadora?)
   
   
   
   156,75 impulso
   108 retroceso
   
   
   
  Estado	    EV 5 min    EV 15/30    EV 30/1D	Sentimiento
	1			Negativo	Negativo	Negativo	Máximo pesimismo (suelos)
	2			Positivo	Negativo	Negativo	Rebote técnico
	3			Negativo	Positivo	Negativo	Consolidación
	4			Positivo	Positivo	Negativo	Recuperación
	5			Negativo	Negativo	Positivo	Corrección
	6			Positivo	Negativo	Positivo	Tendencia alcista
	7			Negativo	Positivo	Positivo	Toma de ganancias
	8			Positivo	Positivo	Positivo	Máxima euforia (techos)
	
	El modelo predice continuamente los niveles de precio donde el EV cambiará de signo:

	T2: Transición de 2 niveles de estado (ej. Estado 7 → Estado 5)
	T4: Transición de 4 niveles de estado (ej. Estado 8 → Estado 4)
	
	Señales de Tendencia:
Signal 1 (Uptrend): Picos y valles del EV suben junto con el precio → optimismo generalizado
Signal 2 (Downtrend): Picos y valles del EV bajan con el precio → pesimismo
Señales de Reversión:
Signal 3 (Reverse to Uptrend): Durante bajada, EV hace valle igual/menor pero precio hace valle MÁS ALTO → market makers optimistas
Signal 4 (Reverse to Downtrend): Durante subida, EV hace pico igual/mayor pero precio hace pico MÁS BAJO → market makers pesimistas
Señales de Traders Informados:
Signal 5 (Selling): EV cae en máximo del mercado → toma de ganancias
Signal 6 (Buying): EV sube en mínimo del mercado → compra de oportunidad
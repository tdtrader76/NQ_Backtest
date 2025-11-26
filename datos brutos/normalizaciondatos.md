
ts_event,rtype,publisher_id,instrument_id,open,high,low,close,volume,symbol
2020-10-09T03:15:00.000000000Z,33,1,4378,11587.250000000,11587.250000000,11587.250000000,11587.250000000,3,NQH1



## Se deben transformar los datos a este formato:

 **Comprobar que las columnas open,high,low,close tienen todas número de 5 cifras y dos decimales.

date | time | open | high | low | close | volume | symbol
2020-10-09,03:15:00,11587.25,11587.25,11587.25,11587.25,3,NQ 03-20 




**la columna "symbol" se reemplaza por el mes y el año. El año se toma de la fecha y el més según la siguiente lista:
	
	-H = Marzo (March)
	-M = Junio (June)
	-U = Septiembre (September)
	-Z = Diciembre (December)


# En excel no usar . para los miles y las columnas separadas por ; Los puntos del decimal serán comas. 

date		time		open		high		low		close		volume
09/10/2020	3:15:00         11587.25	11587.25	11587.25	11587.25	3

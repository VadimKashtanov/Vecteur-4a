import time
import datetime
import requests

from os import system

from datetime import datetime

unix_ms_vers_date = lambda ums: datetime.fromtimestamp(
	int(ums/1000)
).strftime('%Y-%m-%d %H:%M:%S')

ARONDIRE_AU_MODULO = lambda x,mod: (x + (mod - (x%mod)) if x%mod!=0 else x)

ARONDIRE_AU_MODULO_SUPERIEUR = lambda x,mod: ARONDIRE_AU_MODULO(x+mod,mod)

milliseconde = lambda la: int(la * 1000   )*1
seconde      = lambda la: int(la          )*1000
heure        = lambda la: int(la*1000)#int(la / (60*60))*1000*60*60

requette_bitget = lambda de, a, SYMBOLE, d: eval(
	requests.get(
		f"https://api.bitget.com/api/mix/v1/market/history-candles?symbol={SYMBOLE}_UMCBL&granularity={d}&startTime={de}&endTime={a}&productType=usdt-futures"
	).text
)

HEURES_PAR_REQUETTE = 100

def DONNEES_BITGET(__HEURES, d):
	assert d in ('1H', '1m', '15m')
	print(f"L'intervalle choisie est : {d}")
	print(f"Demande de {__HEURES} elements de {d}")
	#assert d == '15m'
	#
	HEURES = ARONDIRE_AU_MODULO_SUPERIEUR(__HEURES, HEURES_PAR_REQUETTE)
	#
	correspondance_millisecondes = {
		'1H'  : 60*60*1000,
		'15m' : 15*60*1000,
		'1m'  :  1*60*1000
	}
	#
	la = heure(time.time())
	heures_voulues = [
		la - correspondance_millisecondes[d]*i
		for i in range(ARONDIRE_AU_MODULO(HEURES, HEURES_PAR_REQUETTE))
	][::-1]

	donnees_BTCUSDT = []

	REQUETTES = int(len(heures_voulues) / HEURES_PAR_REQUETTE)
	print(f"Extraction de {len(heures_voulues)} {d} depuis api.bitget.com ...")
	#
	depart = time.time()
	for i in range(REQUETTES):
		paquet_heures_btc = requette_bitget(
			heures_voulues[ i   *HEURES_PAR_REQUETTE  ],
			heures_voulues[(i+1)*HEURES_PAR_REQUETTE-1],
			"BTCUSDT",
			d
		)
		donnees_BTCUSDT += paquet_heures_btc

		if i % 1 == 0:
			pourcent = i*HEURES_PAR_REQUETTE/len(heures_voulues)
			print(f"[{round(pourcent*100,2)}%],   len(paquet_heures_btc)={len(paquet_heures_btc)}, (btc,)  reste={(round((time.time()-depart)/pourcent*(1-pourcent)/60) if pourcent!=0 else 0)} mins   len(donnees_BTCUSDT)={len(donnees_BTCUSDT)}")

	print(f"HEURES VOULUES = {len(heures_voulues)}, len(donnees_BTCUSDT)={len(donnees_BTCUSDT)}")

	return donnees_BTCUSDT[-__HEURES:]

#	Ancien site : https://www.CryptoDataDownload.com

def faire_un_csv(donnees_BTCUSDT, NOM="bitgetBTCUSDT"):
	csv = """https://www.bitget.com/api-doc/contract/market/Get-History-Candle-Data
Unix,Date,Symbol,Open,High,Low,Close,Volume,Volume Base Asset,tradecount\n"""

	for ums,o,h,l,c,vB,vU in donnees_BTCUSDT[::-1]:
		date = unix_ms_vers_date(float(ums))
		csv += f'0,{date},{NOM},{o},{h},{l},{c},{vU},{vB},0\n'

	return csv

if __name__ == "__main__":
	import struct as st
	with open("structure_generale.bin", 'rb') as co:
		bins = co.read()
		(I,) = st.unpack('I', bins[:4])
		elements = st.unpack('I', bins[4:])
		#
		MEGA_T, = elements
	#
	#
	intervalles = {
		'1H'  : (2024-2019) * 364 * 24,
		'15m' : (2024-2020) * 365 * 24 * 4
	}
	CHOIX = '1H'
	assert intervalles[CHOIX] % MEGA_T == 0
	#
	#
	from CONTEXTE import *

	HEURES = intervalles[CHOIX] + DEPART
	#
	#
	donnees = DONNEES_BITGET(HEURES, d=CHOIX)
	csv     = faire_un_csv(donnees, NOM="BTCUSDT")
	with open("prixs/BTCUSDT_bitget_2020_2024.csv", 'w') as co:
		co.write(csv)

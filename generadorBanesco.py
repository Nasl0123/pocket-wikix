#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
sys.path.insert(0, 'libs')
import pdftables_api
import xlrd
import xlwt
import logging

def limpiar_banesco(texto):
    if type(texto) == float:
        if texto < 1:
            return str(texto*100)+'%'
        return 'RD$'+str(texto)
    return texto.encode('utf-8').replace(',','').replace('RDS','RD$').replace("USS", "US$").replace('US$','USD$').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")

def formatear_banesco(result):
	book = xlrd.open_workbook(file_contents=result)
	sheet = book.sheet_by_index(0)
	test = ""
	for row in range(4,25):
		for col in range(0,8):
			try:
				celda = limpiar_banesco(sheet.cell_value(row,col))
				if sheet.cell_value(row,col) == "" and not("///" in sheet.cell_value(row,0) or "///" in sheet.cell_value(row,1) or "///" in sheet.cell_value(row,2)):
					test = test + "RD$ 0,"
				else:
					if "RD$" in celda or "USD$" in celda or "%" in celda or "Carta de" in celda:
						test = test + celda + ","
			except:
				pass

	return test

def sacar_entero(cadena):
    if type(cadena) == float or type(cadena) == int:
        return int(cadena)
    else:
        for e in cadena:
            if e.isdigit() == False and e != ".":
                cadena = cadena.replace(e,"")
    return int(float(cadena))

def agregar_valores(rows,dicts,positions,efectivo_fila):
	dicts = dicts
	datos = {}
	postitions = positions
	datos["emision"] = rows["fila1"]
	datos["emision_tarjeta_adicional"] = rows["fila2"]
	datos["renovacion_titular"] = rows['fila3'] 
	datos["renovacion_adicional"] = rows['fila4']
	datos["reposicion_plastico"] = rows['fila5']
	datos["proteccion"] = rows['fila6']
	datos["mora_rd"] = rows['fila7']
	datos["mora_us"] = rows['fila8']
	datos["tasa_interes_rd"] =  rows["fila9"]
	datos["tasa_interes_us"] = rows["fila10"]
	datos["avance_efectivo"] = rows[efectivo_fila]

	for tarjeta in dicts:
		if tarjeta == "flotilla":
			for tarj in dicts[tarjeta]:
				for dato in datos:
					try:

						dicts[tarjeta][tarj][dato] = datos[dato][positions[tarjeta]].split(",")[positions[tarjeta+"_"+tarj]]

					except:
						dicts[tarjeta][tarj][dato] = "RD$ 0"
		else:

			for dato in datos:
				

				try:
					dicts[tarjeta][dato] = datos[dato][positions[tarjeta]]
				except:
					logging.error(tarjeta)

	return dicts

	








def Pos_mirada(cuadro):
	x = (cuadro[x1]+cuadro[x2])/2
	y = (cuadro[y1]+cuadro[y2])/2
	return x,y

def Pos_centro(cuadro):
	x = (cuadro[x1]+cuadro[x2])/2
	y = (cuadro[y1]+cuadro[y2])/2
	return x,y

def Mirada(posM,posC):
	return posM-posC

def promedio(lista):
	total = 0
	for x in lista:
		total += x
	return total/len(lista)
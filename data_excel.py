import xlwt

class DataExcel(object):

    def __init__(self):
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet('data sheet')
        self.ws.write(0, 0, "tiempo")
        #self.ws.write(0, 0, "clasificador")
        self.ws.write(0, 1, "caras")
        #self.ws.write(0, 2, "tiempo")
        self.ws.write(0, 2, "carasMirando")
        #
        self.row = 1

    def data_to_excel(self, contador, clasificador, caras, tiempo_ejecucion):
        self.ws.write(self.row, 0, clasificador)
        self.ws.write(self.row, 1, caras)
        self.ws.write(self.row, 2, tiempo_ejecucion)
        self.row += contador
        self.wb.save('data_face_vision.xls')

    def faces_to_excel2(self, move_row, tiempo, caras):
        self.ws.write(self.row, 0, tiempo)
        self.ws.write(self.row, 1, caras)
        self.row += move_row
        self.wb.save('data_face_vision.xls')

    def faces_to_excel(self, move_row, tiempo, caras, carasMirando):
        self.ws.write(self.row, 0, tiempo)
        self.ws.write(self.row, 1, caras)
        self.ws.write(self.row, 2, carasMirando)
        self.row += move_row
        self.wb.save('data_face_vision.xls')
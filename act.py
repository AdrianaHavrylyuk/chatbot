#- * - coding: utf - 8 -*-
from fpdf import FPDF
from datetime import datetime

months = {
    1: 'cічня',
    2: 'лютого',
    3: 'березня',
    4: 'квітня',
    5: 'травня',
    6: 'червня',
    7: 'липня',
    8: 'серпня',
    9: 'вересня',
    10: 'жовтня',
    11: 'листопада',
    12: 'грудня'
}
class ACT_PDF(FPDF):
    def header(self):
        self.set_xy(0, 4)
        self.set_font('Arial_Cyr_B', 'B', size=9)
        self.cell(210, 8.5, 'АКТ', 0, 1, align='C')

        today = datetime.today()
        current_month = today.month
        datem = months[current_month]
        self.set_font('Arial_Cyr_B', 'B', size=8)
        self.cell(0, 0, '№ 1/5 від  _____ ' + datem + ' 2023 р.', 0, 1, align='C')
        self.set_font('Arial_Cyr', '', size=8)
        self.cell(0, 9, 'Здачі-прийняття робіт (надання послуг)', 0, 1, align='C')
        self.set_xy(10, 25)
        self.multi_cell(190, 3.5, 'Ми, представники постачальника Комунальне підприємство "Міськводоканал" Мукачівської міської ради в особі директора Олег КАЗИБРІД з одного боку та представник споживача +++ з іншого боку, склали цей акт про те, що згідно договору №2 від 21.01.2021 постачальником були надані послуги.  ', border=0, align='L')

    def footer(self):
        self.set_font('Arial_Cyr', '', size=8)
        self.multi_cell(190, 3.5, 'Надані послуги виконані в повному обсязі. До якості послуг замовник претензій не має. Акт свідчить про сприйняття робіт і служить підставою для розрахінків з Виконавцем', border=0, align='L')
        self.cell(0, 5, 'Виконавець _______________', 0, 1)
        self.cell(0, 5, 'Цей акт складено з метою проведення розрахунків між сторонами. Цей акт складено у двох примірниках, що мають однакову юридичну силу. ', 0, 1)
        self.cell(110, 5, 'Директор', 0, 0)
        self.cell(30, 5, 'Від Замовника:', 0, 1)
        self.cell(110, 5, 'М.П._________________ Олег КАЗИБРІД', 0, 0)
        self.cell(30, 5, 'М.П._________________ ', 0, 1)
        self.cell(110, 5, '"      " ____________________ p.', 0, 0)
        self.cell(30, 5, '"      " ____________________ p.', 0, 1)

    def table(self):
        self.set_xy(11, 40)
        self.set_font('Arial_Cyr', '', size=8)
        self.cell(64, 6, 'Найменування послуг', 1, 0, align='C')
        self.cell(25, 6, 'Одиниця виміру', 1, 0, align='C')
        self.cell(25, 6, 'Обсяг, кількість', 1, 0, align='C')
        self.multi_cell(25, 3, 'Вартість без ПДВ (грн.)', 1, align='C')
        self.set_xy(150, 40)
        self.cell(25, 6, 'ПДВ (грн.)', 1, 0, align='C')
        self.multi_cell(25, 3, 'Вартість з ПДВ (грн.)', 1, align='C')


pdf = ACT_PDF('P', 'mm', 'A4')
pdf.add_font('Arial_Cyr', '', 'font/Arial_Cyr.ttf', uni=True)
pdf.add_font('Arial_Cyr_B', 'B', 'font/Arial_Cyr_B.ttf', uni=True)
pdf.add_page()
pdf.table()


pdf.output("АКТ.pdf")
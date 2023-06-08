from fpdf import FPDF
from datetime import datetime

class BILL_PDF(FPDF):
    def header(self):
        self.set_font('Arial_Cyr_B', 'B', size=8)
        self.cell(22, 10, 'Постачальник:', 0, 0, 'L')
        self.set_font('Arial_Cyr', '', size=8)
        self.cell(10, 10, 'Комунальне підприємство "Міськводоканал" Мукачівської міської ради пл.Духновича,2', 0, 1)
        self.set_font('Arial_Cyr_B', 'B', size=8)
        self.cell(32, 10, 'Реквізити на оплату:', 0, 0, 'L')
        self.set_font('Arial_Cyr', '', size=8)
        self.cell(10, 10, 'Одержувач: Комунальне підприємство "Міськводоканал" Мукачівської міської ради', 0, 1)
        self.cell(0, 0, 'Р/р: UA 333223130000026004000048281 в АТ"Укрексімбанк" МФО:322313', 0, 1)
        self.cell(0, 7, 'Код ЄДРПОУ: 41536514 ІПН: 415365107024', 0, 1)

    def footer(self):
        self.set_font('Arial_Cyr', '', size=8)
        self.cell(52, 10, 'Начальник ВРтаРзА', 0, 0)
        self.cell(10, 10, 'Надія САБОВ', 0, 1)
        self.cell(0, 0, 'Виконавець    _____________', 0, 1)
        self.cell(0, 10, 'МП.', 0, 1)
        self.cell(100, 10, '1 прим. рахунку отримав "_______" __________________ 2023 р. _______________________________', 0, 0)
        self.set_font('Arial_Cyr', '', size=6)
        self.cell(0, 20, '(ПІБ, посада, підпис)', 0, 1)

    def dashed_t(self, w, h, text=''):
        cur_line_width = self.line_width
        self.set_line_width(0.1)
        x = self.get_x()
        y = self.get_y()
        pdf.dashed_line(x, y, w + x, y, dash_length=0.7, space_length=2)
        pdf.dashed_line(x+w, y, x+w, y + h, dash_length=0.7, space_length=2)
        self.dashed_line(x, y + h, x + w, y + h, dash_length=0.7, space_length=2)
        self.dashed_line(x, y, x, y + h, dash_length=0.7, space_length=2)
        self.set_line_width(cur_line_width)
        self.multi_cell(w, h, 'Особовий рахунок', 0, 1)


    def table(self):
        #from main import insert_into_bot
        self.set_font('Arial_Cyr_B', 'B', size=10)
        #self.cell(0, 0, 'РАХУНОК 0№ ' + str(acc_id) +'/053/' + str(acc_id), 0, 1, align='C')
        self.cell(0, 0, 'РАХУНОК № 1/053/1 ', 0, 1, align='C')

        months = {
            1: 'cічень',
            2: 'лютий',
            3: 'березень',
            4: 'квітень',
            5: 'травень',
            6: 'червень',
            7: 'липень',
            8: 'серпень',
            9: 'вересень',
            10: 'жовтень',
            11: 'листопад',
            12: 'грудень'
        }

        today = datetime.today()
        current_month = today.month
        datem = months[current_month]
        current_year = today.year

        self.set_font('Arial_Cyr', '', size=8)
        self.cell(0, 10, 'за ' + str(datem) + " " + str(current_year) + ' р.', 0, 1, align="C")
        self.set_font('Arial_Cyr_B', 'B', size=8)
        self.cell(10, 4, 'Увага!', 0, 0)
        self.set_font('Arial_Cyr', '', size=8)
        self.cell(10, 4, 'Попереджаємо, що у разі несплати цього груп-рахунку у термін 10 днів з моменту його отримання, надання послуг буде припинено. ', 0, 1)
        month = today.strftime("%m")
        self.cell(0,4, 'Сальдо на 01.' + str(month) + '.2023: ', border = 1, ln = 1)
        self.set_font('Arial_Cyr', '', size=7)
        self.cell(35, 15, 'Найменування підключення', border=1, ln=0, align='C')
        self.multi_cell(15, 7.5, '№ лічильника', border=1, align='C' )
        self.set_xy(60,55)
        self.multi_cell(13, 5, 'Наступна держ. повірка', border=1, align='C')
        self.set_xy(73,55)
        self.multi_cell(20, 3.75, 'Попередні показання приладів обліку води', border=1, align='C')
        self.set_xy(93,55)
        self.multi_cell(20, 3.75, 'Останні показання приладів обліку води', border=1, align='C')
        self.set_xy(113, 55)
        self.cell(43.5, 5, 'Водопостачання', border=1, ln=0, align='C')
        self.cell(43.5, 5, 'Водовідведення', border=1, ln=1, align='C')
        self.set_xy(113, 60)
        self.multi_cell(12.5, 3.35, 'Обсяг спожитої води, м3', border=1, align='C')
        self.set_xy(125.5, 60)
        self.multi_cell(11, 5, 'Тариф грн/м3', border=1, align='C')
        self.set_xy(136.5, 60)
        self.multi_cell(20,10, 'Вартість, грн', border=1, align='C')
        self.set_xy(156.5, 60)
        self.multi_cell(12.5, 2.5, 'Обсяг скинутих стоків, м3', border=1, align="C")
        self.set_xy(169, 60)
        self.multi_cell(11, 5, 'Тариф грн/м3', border=1, align='C')
        self.set_xy(180, 60)
        self.multi_cell(20, 10, 'Вартість, грн', border=1, align='C')

        self.set_font('Arial_Cyr_B', 'B', size=8)
        self.cell(35, 4, "1", 1, 0, align='C')
        self.cell(15, 4, "2", 1, 0, align='C')
        self.cell(13, 4, "3", 1, 0, align='C')
        self.cell(20, 4, "4", 1, 0, align='C')
        self.cell(20, 4, "5", 1, 0, align='C')
        self.cell(12.5, 4, "6", 1, 0, align='C')
        self.cell(11, 4, "7", 1, 0, align='C')
        self.cell(20, 4, "8", 1, 0, align='C')
        self.cell(12.5, 4, "9", 1, 0, align='C')
        self.cell(11, 4, "10", 1, 0, align='C')
        self.cell(20, 4, "11", 1, 1, align='C')




pdf = BILL_PDF('P', 'mm', 'A4')
pdf.add_font('Arial_Cyr', '', 'font/Arial_Cyr.ttf', uni=True)
pdf.add_font('Arial_Cyr_B', 'B', 'font/Arial_Cyr_B.ttf', uni=True)
pdf.add_page()
pdf.table()

pdf.output('РАХУНОК.pdf')
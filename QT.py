import sys
import csv
from PIL import Image, ImageDraw
import xlrd
from math import sqrt
import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, \
    QLabel, QApplication, QMainWindow, QComboBox, QColorDialog, QCheckBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent  # библиотеки


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('textred.ui', self)
        self.label.hide()  # прячем всякую гадость из дизайнера
        self.color = (255, 0, 0)  # константы, флажки, ухх...
        self.fl, self.fl1 = True, True
        self.flWhBl = False
        self.inf = 10 ** 10
        self.dic = {
            0: ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8',
                '0.9', '0.10', '0.11', 'Лифт 0', 'Кладовая',
                '41 каб.', '42 каб.', '43 каб.', 'Лестница 0.3',
                'Лестница 0.4', 'Лестница 0.3.5', 'Эскалатор 0', 'Лестница 0.1',
                'Раздевалка для девочек', 'Раздевалка для мальчиков',
                'Раздевалка для начальной школы', 'Столовая(кухня)',
                'Столовая', 'Слоловая2', 'Щитовая'],
            1: ['Выход 1', 'Выход 2', '1.1', '1.2', '1.3', '1.4', '1.5',
                '1.6', '1.7', '1.8', '1.9', '1.10', 'Туалеты', 'Лестница 1.1',
                'Эскалатор 1', 'Лестница 1.3', 'Лестница 1.4', 'Мед. Кабинет',
                'Библиотека', '9 каб.', '8 каб.', '6 каб.', '5 каб.', 'Лифт 1',
                '3 каб.', 'Кухня', 'Кабинет директора', 'Приемная'],
            2: ['Лестница 2.1', 'Эскалатор 2', '2.1', '2.2', '2.3',
                '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '2.10', '2.11',
                'Лаборанская биологии',
                'Кабинет заместителя директора по УВР. Начальная школа',
                '12 каб.', 'Лифт 2', '14 каб.', '15 каб.', '16 каб.',
                '17 каб.', '18 каб.', '19 каб.',
                'Кабинет заместителя директора по УВР', 'Учительская',
                'Туалет для мальчиков', '12.2'],
            3: ['3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9',
                '3.10', '3.11', '21.2', '21 каб.', 'Лифт 3', '23 каб.',
                '24 каб.', '25 каб.', '26 каб.', '27 каб.', '28 каб.',
                '29 каб.', '30 каб.', 'Лаборанская физики', 'Лестница 3.1',
                'Эскалатор 3', 'Кабинет заместителя директора',
                'Лаборанская географии', 'Туалет для девочек'],
            4: ['4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', 'Актовый зал',
                'А.З. 1', 'А.З. 2', 'Спортивный зал', 'С.З.1', 'Лестница 4.1',
                'Эскалатор 4', 'С.З.2', 'С.З.3', '31 каб.', 'Лифт 4',
                '33 каб.', '34 каб.', 'Лаборанская химии',
                'Методический кабинет', 'Лаборанская',
                'Раздевалка для мальчиков (Физ-ра)',
                'Раздевалка для девочек (Физ-ра)', '31.2']}
        self.spisNameStairs = ['Лестница 0.1',
                               'Лестница 1.1',
                               'Лестница 2.1',
                               'Лестница 3.1',
                               'Лестница 4.1'
                               ]
        self.spisNumStairs = []
        self.spisNameEscal = ['Эскалатор 0',
                              'Эскалатор 1',
                              'Эскалатор 2',
                              'Эскалатор 3',
                              'Эскалатор 4',
                              ]
        self.spisNumEscal = []
        self.spisNameElev = ['Лифт 0',
                             'Лифт 1',
                             'Лифт 2',
                             'Лифт 3',
                             'Лифт 4',
                             ]
        self.spisNumElev = []
        self.mainScreen()

    def inputIn(self):  # считываем из различных файлов нужную информацию
        b = xlrd.open_workbook("data.xls")  # ЭКСЕЛЬ?!
        # Ладно, это просто таблица смежности)
        s = b.sheet_by_index(0)
        self.weight, self.w, self.name_num = [], [], {}
        self.num_name, k, self.coords = {}, 0, {}
        con = sqlite3.connect("data.db")  # воу-воу-воу, базы данных!
        cur = con.cursor()
        for i in cur.execute("""SELECT Name FROM SchoolCoords""").fetchall():
            self.name_num[str(i[0])] = k
            self.num_name[k] = i[0]
            k += 1
        result = cur.execute("""SELECT * FROM SchoolCoords""").fetchall()
        self.coords = {}
        for i in result:
            self.coords[self.name_num[i[0]]] = list(i[1:])
        con.close()
        for i in range(1, len(s.col_values(4))):
            strok = s.row_values(i)[5:]
            for j in range(len(strok)):
                if strok[j] == '':
                    strok[j] = self.inf
                elif strok[j] <= 0:
                    strok[j] = sqrt((self.coords[i - 1][0] - self.coords[j][0]
                                     ) ** 2 + (self.coords[i - 1][1] -
                                               self.coords[j][1]) ** 2)
            self.weight += [strok]
        for i in range(len(self.weight)):
            self.w += [[j for j in range(len(self.weight[0]))
                        if self.weight[i][j] != self.inf]]
        self.alls = [j for i in self.dic.values() for j in i if
                     j.isalpha() or 'каб' in j or 'Выход' in j or
                     'Кабинет' in j or 'Лаборанская' in j or
                     'Туалет' in j or 'зал' in j or 'Столовая' in j or
                     'Раздевалка' in j]
        self.alls = self.alls[::-1]
        self.where = 1
        self.dataIm = ['Подвал11.png', '1 этаж11.png', '2 этаж11.png',
                       '3 этаж11.png', '4 этаж11.png']
        self.dataImOrig = ['Подвал10.png', '1 этаж10.png', '2 этаж10.png',
                           '3 этаж10.png', '4 этаж10.png']
        self.dataImBlaWhi = ['ПодвалЧБ.png', '1 этажЧБ.png', '2 этажЧБ.png',
                             '3 этажЧБ.png', '4 этажЧБ.png']
        self.plansOfescape = ['ПодвалПланЭвакуации.png',
                              '1 этажПланЭвакуации.png',
                              '2 этажПланЭвакуации.png',
                              '3 этажПланЭвакуации.png',
                              '4 этажПланЭвакуации.png']
        self.plansOfescapeBlaWhi = ['ПодвалПланЭвакуацииЧБ.png',
                                    '1 этажПланЭвакуацииЧБ.png',
                                    '2 этажПланЭвакуацииЧБ.png',
                                    '3 этажПланЭвакуацииЧБ.png',
                                    '4 этажПланЭвакуацииЧБ.png']
        #     Наколдовали основных строк, словарей и констант

    def mainScreen(self):  # кнопочки :>
        self.inputIn()
        self.resize(950, 580)
        self.setWindowTitle('Проект')
        self.start = QComboBox(self)
        self.start.move(50, 0)
        self.start.resize(200, 50)
        self.start.addItems(self.alls)
        self.start.setCurrentIndex(self.start.findText('Выход 1'))
        self.start.installEventFilter(self)
        self.finish = QComboBox(self)
        self.finish.move(250, 0)
        self.finish.resize(200, 50)
        self.finish.addItems(self.alls)
        self.finish.setCurrentIndex(self.finish.findText('Выход 1'))
        self.finish.installEventFilter(self)
        self.higher = QPushButton('▲\n|', self)
        self.higher.move(0, 50)
        self.higher.resize(50, 50)
        self.higher.clicked.connect(self.lift)
        self.higher.installEventFilter(self)
        self.lower = QPushButton('|\n▼', self)
        self.lower.move(0, 100)
        self.lower.resize(50, 50)
        self.lower.clicked.connect(self.lift)
        self.lower.installEventFilter(self)
        self.escape = QPushButton('План эвакуации', self)
        self.escape.move(850, 0)
        self.escape.resize(100, 50)
        self.escape.clicked.connect(self.run)
        self.escape.installEventFilter(self)
        self.go = QPushButton('Проложить маршрут', self)
        self.go.move(450, 0)
        self.go.resize(200, 50)
        self.go.clicked.connect(self.do)
        self.go.installEventFilter(self)
        self.image = QLabel(self)
        self.image.move(50, 50)
        self.image.resize(900, 449)
        self.image.setPixmap(QPixmap(self.dataIm[self.where]))
        self.colLine = QPushButton('Изменить цвет\nлинии маршрута', self)
        self.colLine.move(0, 500)
        self.colLine.resize(110, 50)
        self.colLine.clicked.connect(self.getCol)
        self.colUp = QPushButton('Изменить цвет\nкнопки "Вверх"', self)
        self.colUp.move(110, 500)
        self.colUp.resize(110, 50)
        self.colUp.clicked.connect(self.getCol)
        self.colLower = QPushButton('Изменить цвет\nкнопки "Вниз"', self)
        self.colLower.move(220, 500)
        self.colLower.resize(110, 50)
        self.colLower.clicked.connect(self.getCol)
        self.colStart = QPushButton("Изменить цвет кнопки\n" +
                                    "выбора начальной точки\nмаршрута", self)
        self.colStart.move(330, 500)
        self.colStart.resize(160, 50)
        self.colStart.clicked.connect(self.getCol)
        self.colFinish = QPushButton("Изменить цвет кнопки\n" +
                                     "выбора конечной точки\nмаршрута", self)
        self.colFinish.move(490, 500)
        self.colFinish.resize(160, 50)
        self.colFinish.clicked.connect(self.getCol)
        self.colGo = QPushButton("Изменить цвет\nкнопки\n" +
                                 '"Проложить маршрут"', self)
        self.colGo.move(650, 500)
        self.colGo.resize(160, 50)
        self.colGo.clicked.connect(self.getCol)
        self.colEscape = QPushButton("Изменить цвет\n" +
                                     'кнопки\n"План эвакуации"', self)
        self.colEscape.move(810, 500)
        self.colEscape.resize(140, 50)
        self.colEscape.clicked.connect(self.getCol)
        self.info = QPushButton('i', self)
        self.info.resize(50, 50)
        self.info.move(0, 0)
        self.info.clicked.connect(self.infoAbout)
        self.blaWhi = QPushButton('Сделать план в\nчерно-белом\nформате', self)
        self.blaWhi.resize(100, 50)
        self.blaWhi.move(750, 0)
        self.blaWhi.clicked.connect(self.blackWhite)
        self.changeLv = QPushButton('Перейти на этаж\nточки начала', self)
        self.changeLv.resize(100, 50)
        self.changeLv.move(650, 0)
        self.changeLv.clicked.connect(self.level)
        self.stairs = QCheckBox('Построение маршрута с лестницами', self)
        self.stairs.move(40, 550)
        self.stairs.resize(316, 30)
        self.stairs.click()
        self.stairs.stateChanged.connect(self.withoutStairs)
        # self.stairs.setDisabled(True)
        self.escalators = QCheckBox('Построение маршрута с эскалаторами', self)
        self.escalators.move(356, 550)
        self.escalators.resize(316, 30)
        self.escalators.click()
        self.escalators.stateChanged.connect(self.withoutEscal)
        # self.escalators.setDisabled(True)
        self.elevators = QCheckBox('Построение маршрута с лифтами', self)
        self.elevators.move(672, 550)
        self.elevators.resize(316, 30)
        self.elevators.click()
        self.elevators.stateChanged.connect(self.widthoutElev)
        # self.elevators.setDisabled(True)
        self.go.click()

    def withoutStairs(self):
        if self.stairs.isChecked():
            self.spisNumStairs = []
        else:
            self.spisNumStairs = [self.name_num[i] for i in self.spisNameStairs]
        self.go.click()

    def withoutEscal(self):
        if self.escalators.isChecked():
            self.spisNameEscal = []
        else:
            self.spisNumEscal = [self.name_num[i] for i in self.spisNameEscal]
        self.go.click()

    def widthoutElev(self):
        if self.elevators.isChecked():
            self.spisNameElev = []
        else:
            self.spisNumElev = [self.name_num[i] for i in self.spisNameElev]
        self.go.click()

    def blackWhite(self):  # работа с переходом из цветного в чб
        if self.flWhBl:
            self.flWhBl = False
            self.colLine.show()
        else:
            self.colLine.hide()
            self.badColor = (0, 0, 0)
            self.flWhBl = True
        self.dataImOrig, self.dataImBlaWhi \
            = self.dataImBlaWhi[:], self.dataImOrig[:]
        self.color, self.badColor = self.badColor, self.color
        if self.fl:
            self.plansOfescape, self.plansOfescapeBlaWhi = \
                self.plansOfescapeBlaWhi[:], self.plansOfescape[:]
            self.go.click()
        else:
            self.colLine.hide()
            self.dataIm, self.plansOfescape = \
                self.plansOfescape[:], self.dataIm[:]
            self.plansOfescape, self.plansOfescapeBlaWhi = \
                self.plansOfescapeBlaWhi[:], self.plansOfescape[:]
            self.go.click()
            self.dataIm, self.plansOfescape = \
                self.plansOfescape[:], self.dataIm[:]
            self.image.setPixmap(QPixmap(self.dataIm[self.where]))

    def hideAll(self):  # прячем все)
        self.changeLv.hide()
        self.blaWhi.hide()
        self.start.hide()
        self.finish.hide()
        self.higher.hide()
        self.lower.hide()
        self.escape.hide()
        self.go.hide()
        self.colUp.hide()
        self.colLower.hide()
        self.colGo.hide()
        self.colEscape.hide()
        self.colStart.hide()
        self.colFinish.hide()
        self.colLine.hide()
        self.image.hide()
        self.info.hide()

    def showAll(self):  # показываем все
        self.changeLv.show()
        self.blaWhi.show()
        self.start.show()
        self.finish.show()
        self.higher.show()
        self.lower.show()
        self.escape.show()
        self.go.show()
        self.colUp.show()
        self.colLower.show()
        self.colGo.show()
        self.colEscape.show()
        self.colStart.show()
        self.colFinish.show()
        self.colLine.show()
        self.image.show()
        self.info.show()

    def infoAbout(self):  # работа с кнопкой информации
        if self.fl1:
            self.hideAll()
            self.info.show()
            self.label.show()
            self.escape.setDisabled(True)
            self.fl1 = False
        else:
            self.label.hide()
            self.escape.setDisabled(False)
            self.fl1 = True
            if self.fl:
                self.showAll()
            else:
                self.blaWhi.show()
                self.colEscape.show()
                self.colLower.show()
                self.colUp.show()
                self.higher.show()
                self.lower.show()
                self.image.show()
                self.escape.show()

    def getCol(self):  # работа с диалоговым окном для выбора цвета
        color = QColorDialog.getColor()
        if color.isValid():
            if self.sender().text() == self.colUp.text():
                self.higher.setStyleSheet(
                    "background-color: {}".format(color.name()))
            elif self.sender().text() == self.colLower.text():
                self.lower.setStyleSheet(
                    "background-color: {}".format(color.name()))
            elif self.sender().text() == self.colGo.text():
                self.go.setStyleSheet(
                    "background-color: {}".format(color.name()))
            elif self.sender().text() == self.colEscape.text():
                self.escape.setStyleSheet(
                    "background-color: {}".format(color.name()))
            elif self.sender().text() == self.colStart.text():
                self.start.setStyleSheet(
                    "background-color: {}".format(color.name()))
            elif self.sender().text() == self.colFinish.text():
                self.finish.setStyleSheet(
                    "background-color: {}".format(color.name()))
            elif self.sender().text() == self.colLine.text():
                self.color = color.name()
                self.go.click()

    def alg_Dijkstra(self):  # алгоритм дейкстры
        if self.numSt == self.numFin:
            self.path = [self.numFin]
        else:
            n = len(self.weight)
            prev = [None] * n
            dist = [self.inf] * n
            dist[self.numSt] = 0
            used = [False] * n
            min_dist = 0
            min_vertex = self.numSt
            while min_dist < self.inf:
                min_dist = self.inf
                i = min_vertex
                used[i] = True
                for j in range(n):
                    if ((i not in self.spisNumStairs and j not in self.spisNumStairs) and
                        (i not in self.spisNumEscal and j not in self.spisNumEscal) and
                        (i not in self.spisNumElev and j not in self.spisNumElev)) and \
                            dist[i] + self.weight[i][j] < dist[j]:
                        dist[j] = dist[i] + self.weight[i][j]
                        prev[j] = i
                for j in range(n):
                    if not used[j] and dist[j] < min_dist:
                        min_dist = dist[j]
                        min_vertex = j
            self.path = []
            while self.numFin is not None:
                self.path.append(self.numFin)
                self.numFin = prev[self.numFin]
            self.path = self.path[::-1]

    def drawWay(self, lv):  # работа с изображением, рисовка линии маршрута
        im = Image.open(self.dataImOrig[lv])
        drawer = ImageDraw.Draw(im)
        z = 5
        for i in range(len(self.mass)):
            x, y = self.coords[self.mass[i]]
            drawer.ellipse(((int(x - z), int(y - z)),
                            (int(x + z), int(y + z))),
                           self.color)
            if i != len(self.mass) - 1:
                x1, y1 = self.coords[self.mass[i + 1]]
                drawer.line((x, y, x1, y1), fill=self.color, width=5)
        for i in range(-1, 1):
            x, y = self.coords[self.mass[i]]
            z += 5
            drawer.ellipse(((int(x - z), int(y - z)),
                            (int(x + z), int(y + z))),
                           self.color)
            z -= 2
            drawer.ellipse(((int(x - z), int(y - z)),
                            (int(x + z), int(y + z))),
                           (255, 255, 255))
            z -= 3
            drawer.ellipse(((int(x - z), int(y - z)),
                            (int(x + z), int(y + z))),
                           self.color)
        im.save(self.dataIm[lv], "PNG")

    def do(self):  # объединение всех функций для построения пути
        self.numSt, self.numFin = 0, 0
        self.numSt = self.name_num[self.start.currentText()]
        self.numFin = self.name_num[self.finish.currentText()]
        self.alg_Dijkstra()
        notUsed = []
        for j in self.dic.keys():
            self.mass = []
            for i in self.path:
                if self.num_name[i] in self.dic[j]:
                    self.mass += [i]
            if self.mass:
                self.drawWay(j)
            else:
                notUsed += [j]
        for i in notUsed:
            im = Image.open(self.dataImOrig[i])
            im.save(self.dataIm[i], "PNG")
        self.image.setPixmap(QPixmap(self.dataIm[self.where]))

    def level(self):  # поиск уровня точки наяала и перенос на данный уровень
        for j in self.dic.keys():
            if self.num_name[self.numSt] in self.dic[j]:
                self.where = j
                self.lift()
                break

    def keyPressEvent(self, event):  # горячие клавиши
        if event.key() == Qt.Key_W:
            self.higher.click()
        elif event.key() == Qt.Key_S:
            self.lower.click()
        elif event.key() == Qt.Key_H:
            self.escape.click()
        elif event.key() == Qt.Key_G:
            self.go.click()
        elif event.key() == Qt.Key_I:
            self.info.click()
        elif event.key() == Qt.Key_B:
            self.blaWhi.click()

    def eventFilter(self, obj, event):  # не дает фокусироваться на
        # комбобоксах, чтобы все горячие клавиши работали
        if event.type() == QEvent.FocusIn:
            if obj == self.start:
                self.higher.setFocus()
            elif obj == self.finish:
                self.lower.setFocus()
        return super(MyWidget, self).eventFilter(obj, event)

    def lift(self):
        if self.sender().text() == self.higher.text():
            self.where += 1
        elif self.sender().text() == self.lower.text():
            self.where -= 1
        if self.where == 4:
            self.higher.setDisabled(True)
        elif self.where == 0:
            self.lower.setDisabled(True)
        else:
            self.higher.setDisabled(False)
            self.lower.setDisabled(False)
        self.image.setPixmap(QPixmap(self.dataIm[self.where]))

    def run(self):  # работа с режимом плана эвакуации
        if self.fl:
            self.hideAll()
            self.colUp.show()
            self.blaWhi.show()
            self.colLower.show()
            self.colEscape.show()
            self.info.show()
            self.higher.show()
            self.lower.show()
            self.image.show()
            self.escape.show()
            self.fl = False
        else:
            self.showAll()
            self.fl = True
        self.dataIm, self.plansOfescape = \
            self.plansOfescape[:], self.dataIm[:]
        self.image.setPixmap(QPixmap(self.dataIm[self.where]))


def except_hook(cls, exception, traceback):  # луч света в этом
    # темном царстве pyqt, где только избранные знают где ошибка в коде
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

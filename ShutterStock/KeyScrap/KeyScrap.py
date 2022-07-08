
# Python3
#  Author: TpuPyku
#    Site github: https://github.com/TpuPyku
#    Site portfolio: https://tpupyku.myportfolio.com
# ----------------------------------------------
# Name: exiftool
# Author: Phil Harvey
# Version: 12.0.7.0
# Home-page: https://exiftool.org/
# License: GPLv1

from PyQt5 import QtCore #, QtWidgets, QtGui
from PyQt5.QtCore import QThread #, pyqtSignal, pyqtSlot, QBasicTimer, QObject, QSize
from PyQt5.QtGui import QIcon, QFont #, QClipboard
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLineEdit, QApplication,
                                QPushButton, QToolTip, QListWidget, QLabel,
                                QProgressBar, QFileDialog, QGridLayout)  #, QMessageBox, QHBoxLayout, QComboBox, QVBoxLayout, QSpacerItem, QSizePolicy)

import requests #, json, urllib
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

import os, sys, re, datetime #, threading
#from inspect import getsourcefile # для анализа path в exiftool
#from os.path import abspath

import base64
from icon import img

from exiftool import ExifTool, fsencode


class Worker(QThread):
    # передачач сообщений в MainWindow
    progressChanged = QtCore.pyqtSignal(int)
    messageSend = QtCore.pyqtSignal(str)
    colorSend = QtCore.pyqtSignal(str)
    buttonSend = QtCore.pyqtSignal()
    dataSend = QtCore.pyqtSignal(list)
    #finish_signal = QtCore.pyqtSignal() # в скобки добавить переменные для возврата в UI

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        # передаваемые значения из UI
        self.urlSend = None

        # отслеживание для завершения потока
        self.flagFinished = False
        self.count = 0

        # список сообщений в главное окно
        self.color = ['background-color : palette(self)', 
                    'background-color : pink', 
                    'background-color : yellow', 
                    'background-color : green']
        
    @QtCore.pyqtSlot()
    def parsing(self):
        # проверка на ошибку
        try:
            p = re.compile(r'\b\d\d\d\d\d+')
            #img_id = self.urlSend.split(sep='-')
            img_id = str(re.findall(p, self.urlSend)[0])

            url = 'https://shutterstock.com/studioapi/images/{}?include=contributor'.format(img_id)
            print(url)

            req = requests.Session()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            r = req.get(url, headers=headers).json()
            
            self.messageSend.emit('Начинаю скребсти')
            self.colorSend.emit(self.color[0])
            self.progressChanged.emit(10)

        except Exception as e: 
            print('Ошибка в УРЛ или нет интернета', e)
            self.messageSend.emit('Ты мне даёшь какую-то дичь! Дай нормальную ссылку...')
            self.colorSend.emit(self.color[1])
            self.progressChanged.emit(0)
            self.buttonSend.emit()
            self.flagFinished = True
            return
        
        '''
        biblio =    {'data': {'id': '1914601450', 
                            'type': 'images', 
                            'attributes': {'alt': 'Business Development illustrations. Mega set. Collection of scenes with men and women taking part in business activities. Trendy vector style', 
                                            'title': 'Business Development illustrations. Mega set. Collection of scenes with men and women taking part in business activities. Trendy vector style', 
                                            'image_type': 'vector', 
                                            'description': 'Business Development illustrations. Mega set. Collection of scenes with men and women taking part in business activities. Trendy vector style', 
                                            'description_language_map': {'en': 'Business Development illustrations. Mega set. Collection of scenes with men and women taking part in business activities. Trendy vector style'}, 
                                            'aspect': 3.6236, 
                                            'sizes': {'vector_eps': {'format': 'eps', 
                                                                    'dpi': None, 
                                                                    'name': 'vector_eps', 
                                                                    'width': None, 
                                                                    'height': None, 
                                                                    'display_name': 'Vector', 
                                                                    'size_in_bytes': None, 
                                                                    'human_readable_size': None, 
                                                                    'width_in': None, 
                                                                    'height_in': None, 
                                                                    'width_cm': None, 
                                                                    'height_cm': None}, 
                                                        'huge_jpg': {'format': 'jpg', 
                                                                    'dpi': 300, 
                                                                    'name': 'huge_jpg', 
                                                                    'width': 4265, 
                                                                    'height': 1177, 
                                                                    'display_name': 'Huge', 
                                                                    'size_in_bytes': 1954422, 
                                                                    'human_readable_size': '1.9 MB', 
                                                                    'width_in': '14.2"',
                                                                    'height_in': '3.9"', 
                                                                    'width_cm': '36.1 cm', 
                                                                    'height_cm': '10.0 cm'}}, 
                                            'keywords': ['illustration', 'develop', 'people', 'business', 'job', 'set', 'style', 'web', 'application', 'bundle', 
                                                        'businessman', 'character', 'coding', 'collection', 'color', 'communication', 'company', 'computer', 'concept', 'connection', 
                                                        'content', 'design', 'designer', 'developer', 'development', 'digital', 'discussion', 'flat', 'graphic', 'infographic', 
                                                        'internet', 'isolated', 'modern', 'organization', 'outline', 'person', 'professional', 'programming', 'project', 'scene', 
                                                        'site', 'situation', 'software', 'speak', 'technology', 'vector', 'work'], 
                                            'has_property_release': False, 
                                            'has_model_release': False, 
                                            'is_editorial': False, 
                                            'releases': [], 
                                            'src': 'https://image.shutterstock.com/image-vector/business-development-illustrations-mega-set-260nw-1914601450.jpg', 
                                            'displays': {'260nw': {'src': 'https://image.shutterstock.com/image-vector/business-development-illustrations-mega-set-260nw-1914601450.jpg', 
                                                                'width': 942.13, 
                                                                'height': 260}, 
                                                        '600w': {'src': 'https://image.shutterstock.com/image-vector/business-development-illustrations-mega-set-600w-1914601450.jpg', 
                                                                'width': 600, 
                                                                'height': 165.58}, 
                                                        '1500w': {'src': 'https://image.shutterstock.com/z/stock-vector-business-development-illustrations-mega-set-collection-of-scenes-with-men-and-women-taking-part-1914601450.jpg', 
                                                                'width': 1500, 
                                                                'height': 413.95}}, 
                                            'status': 'approved', 
                                            'link': '/image-vector/business-development-illustrations-mega-set-collection-1914601450', 
                                            'width': 943, 
                                            'height': 260, 
                                            'channels': ['shutterstock']}, 
                            'relationships': {'contributor': {'data': {'id': '4100305', 'type': 'contributors'}}}}, 
                    'included': [{'id': '4100305', 
                                'type': 'contributors', 
                                'attributes': {'public_information': {'accounts_id': 153582955, 
                                                                    'contributor_id': 4100305, 
                                                                    'bio': 'Contact us via email - stonepicstudio[at]gmail[dot]com', 
                                                                    'location': 'ua', 
                                                                    'website': 'http://shutterstock.com/g/StonePictures', 
                                                                    'contributor_type_list': ['illustrator'], 
                                                                    'equipment_list': ['Wacom-Smacom'], 
                                                                    'style_list': ['cartooning', 'digital', 'line_art'], 
                                                                    'subject_matter_list': ['abstract', 'backgrounds', 'nature', 'signs', 'vectors'], 
                                                                    'storage_key': '/contributors/4100305/avatars/thumb.jpg', 
                                                                    'cdn_thumb_path': '/contributors/4100305/avatars/thumb.jpg', 
                                                                    'display_name': 'StonePictures', 
                                                                    'vanity_url_username': 'StonePictures', 
                                                                    'portfolio_url_suffix': 'StonePictures', 
                                                                    'portfolio_url': 'https://www.shutterstock.com/g/StonePictures', 
                                                                    'instagram_username': 'ston_epic', 
                                                                    'has_public_sets': True}}}]}
        '''
        try:
            # Берём картинку
            img_src = r['data']["attributes"]["displays"]["600w"]["src"]
            self.progressChanged.emit(20)
            # тип картинки
            img_type = r["data"]["attributes"]["image_type"]

            # берём описание из картинки           
            img_alt = r["data"]["attributes"]["alt"]
            self.progressChanged.emit(30)

            # берём автора
            img_author = r['included'][0]["attributes"]['public_information']['portfolio_url_suffix']
            self.progressChanged.emit(40)

            author_url = r['included'][0]["attributes"]['public_information']['portfolio_url']
            self.progressChanged.emit(50)

            # берём url картинки
            img_url = 'https://shutterstock.com/en' + r['data']["attributes"]["link"]
            self.progressChanged.emit(60)
            
            # берём ключи
            key_tag = r['data']["attributes"]["keywords"]
            self.progressChanged.emit(70)
        except Exception as e:
            print('Ошибка разбора данных', e)
            self.messageSend.emit('Ты мне даёшь какую-то дичь! Такой картинки нет в живых')
            self.colorSend.emit(self.color[1])
            self.progressChanged.emit(0)
            self.buttonSend.emit()
            self.flagFinished = True
            return
        try:
            author_ico = 'https://ak.picdn.net' + r['included'][0]["attributes"]['public_information']['cdn_thumb_path']
        except Exception as e:
            print('Ошибка, у автора нет аватарки', e)
            author_ico = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/271/man-artist_1f468-200d-1f3a8.png'

        soldIndex = ''
        i = len(key_tag)-1
        while i > 0:
            i = i-1
            if key_tag[i] < key_tag[i-1]:
                soldIndex = i
                break

        soldWords = []
        notSoldWords = []
        i = 0
        #print('soldIndex =', soldIndex)
        while i < len(key_tag)-1:
            i = i+1
            #print('i =',i)
            if soldIndex and i <= soldIndex:
                #print('soldWords add')
                soldWords = key_tag[0:i]
            else:
                notSoldWords = key_tag[soldIndex:len(key_tag)]
                #print('notSoldWords add')

        #print(len(key_tag), len(soldWords), len(notSoldWords))
        #print(key_tag)
        #print(len(soldWords), soldWords)
        #print(len(notSoldWords), notSoldWords)
        self.progressChanged.emit(80)

        # Получаем дату загрузки
        try:
            if int(img_id) >= 223291078 :
                url = 'http://m-rank.net/?search=' + str(img_id)
                print(url)
                r = req.get(url, headers=headers)
                soup = BeautifulSoup(r.content, "lxml")

                self.progressChanged.emit(90)
                #print(soup)
                pattern = r'\d\d\d\d\.\d\d\.\d\d'
                #pattern2 = r'<br>"from portfolio"<a href="\/\?search=4100305">(.*?)<\/a>'
                date = re.findall(pattern, str(soup))
                #print(date)
                if date == []:
                    date_day = datetime.date.today().strftime("%Y.%m.%d")
                else:
                    date_day = date[0]
                print(date_day)
            else:
                date_day = 'старше 2014.10.14'
        except Exception as e: 
            print('m-rank parsing kaput', e)
            self.messageSend.emit('Узнать дату загрузки не удалось :(')
            self.colorSend.emit(self.color[1])
            self.progressChanged.emit(90)
            date_day = '🕒'

        # передать данные в основной поток. в скобки записать все переменные
        dataScrap = [img_url, key_tag, img_src, img_alt, img_author, date_day, img_id, soldIndex, soldWords, notSoldWords, author_url, img_type, author_ico]
        #print(self.dataScrap)
        self.dataSend.emit(dataScrap)
        self.buttonSend.emit()
        
        # прогресс бар
        self.messageSend.emit('Соскрёб всё что мог')
        self.colorSend.emit(self.color[3])
        self.progressChanged.emit(100)
        self.flagFinished = True
    
    def run(self):
        self.parsing()        
        
    def stop(self):
        self.flagFinished = False
        self.wait()


class MainWindow(QMainWindow):
    #messageSend = QtCore.pyqtSignal(str)
    #colorSend = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KeyScrap 2.1.210323")
        self.setMinimumSize(800, 600)

        tmp = open("temp.ico","wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.setWindowIcon(QIcon('temp.ico'))
        os.remove("temp.ico")

        QToolTip.setFont(QFont('SansSerif', 10))
        self.urlInput = None
        self.scrape_directory = None
        # список сообщений в главное окно
        self.threadWorker = Worker()
        self.threadWorker.dataSend.connect(self.stop_scrap) # передать данные
        self.threadWorker.messageSend.connect(self.statusBar().showMessage)
        self.threadWorker.colorSend.connect(self.statusBar().setStyleSheet)
        
        self.message = ['Директория выбрана', 
                    'Некорректная ссылка!', 
                    'Должна быть введена директория сохранения файла', 
                    'Картинка сохранена в ', 
                    'Ошибка сохранения: ',
                    'Введите адрес картинки и нажмите Start']
        self.color = ['background-color : palette(self)', 
                'background-color : pink', 
                'background-color : yellow', 
                'background-color : green']


        self.statusBar().setStyleSheet(self.color[0])
        self.statusBar().showMessage(self.message[5])

        self.initUI()
        self.show()
    
    def initUI(self): # главное окно
        clipboard = QApplication.clipboard()
        
        def inBufer(item):
            print(item.text())
            clipboard.setText(item.text())

        def outBufer():
            print(clipboard.text())
            self.urlEntry.setText('')
            self.urlEntry.setText(clipboard.text())

        root = QWidget()
        root.setMinimumSize(800, 600)
        self.setCentralWidget(root)

        # лейбл, текстовое поле ввода запросов
        urlLabel = QLabel("URL or ID: ", self)
        urlLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.urlEntry = QLineEdit(self)
        self.urlEntry.setToolTip("Введи ссылку на картинку или её ID")
        self.urlEntry.setText('')
        
        self.urlEntry.returnPressed.connect(outBufer)

        #кнопка стоп
        self.stopButton = QPushButton("Stop", self)
        self.stopButton.setToolTip('Остановить')
        self.stopButton.clicked.connect(self.sendStop)

        #кнопка старт
        self.startButton = QPushButton("Start", self)
        self.startButton.setToolTip('Запустить')
        self.startButton.clicked.connect(self.sendStart)
        
        # создаем список выдачи
        self.Listbox = QListWidget(self)
        self.Listbox.setAutoFillBackground(True)
        self.Listbox.setToolTip('Здесь выводится найденая информация')
        self.Listbox.setEnabled(False)
        self.Listbox.itemClicked.connect(inBufer)
        

        # лейбл, текстовое поле ввода директории
        dirLabel = QLabel("DIR:", self)
        dirLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.dirEntry = QLineEdit(self)
        self.dirEntry.setToolTip('Выбери папку для сохранения')
        
        #кнопка сохранить
        saveButton = QPushButton("Save", self)
        saveButton.setToolTip('Сохранить')
        saveButton.clicked.connect(self.saveDialog)

        # прогресс бар скачивания
        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        self.progressBar.setEnabled(False)

        # выравнивание в окне
        grid = QGridLayout(root)
        
        grid.setSpacing(10)
        grid.setContentsMargins(30, 30, 30, 50)

        grid.addWidget(urlLabel,         0, 0, 1, 1)
        grid.addWidget(self.urlEntry,    0, 1, 1, 2)
        grid.addWidget(self.stopButton,  0, 3, 1, 1)
        grid.addWidget(self.startButton, 0, 3, 1, 1)

        grid.addWidget(self.Listbox,     1, 0, 3, 4)
        grid.addWidget(self.progressBar, 5, 0, 1, 4)

        grid.addWidget(dirLabel,         6, 0, 1, 1)
        grid.addWidget(self.dirEntry,    6, 1, 1, 2)
        grid.addWidget(saveButton,       6, 3, 1, 1)

        # размеры сетки
        grid.setColumnStretch(1, 0)
        grid.setColumnMinimumWidth(0, 60)
        grid.setColumnMinimumWidth(1, 600)
        grid.setColumnMinimumWidth(2, 60)
        grid.setRowMinimumHeight(5, 10)
    
    def saveDialog(self):
        if self.scrape_directory == None or '':
            self.scrape_directory = QFileDialog.getExistingDirectory(self, 'Выберете Папку для сохранения')
        try:
            while True:
                a = os.path.exists(self.scrape_directory)
                if a == False:
                    self.statusBar().setStyleSheet(self.color[1])
                    self.statusBar().showMessage(self.message[2])
                    break
                else:
                    self.dirEntry.setText(self.scrape_directory)
                    # скачивание картинки
                    img_name = str(self.soldIndex) + '-' + os.path.basename(self.img_src)
                    urlretrieve(self.img_src, os.path.join(self.scrape_directory, img_name))

                    # сохранение инфы в exif
                    etPath = 'ExifTool/exiftool.exe'

                    imgPath = self.scrape_directory + '/' + img_name
                    author = self.img_author
                    keywords = self.printSoldWords
                    comment = ''
                    title = 'Продающих {}, автор {}, ID {}, Загружено {}'.format(self.soldIndex, self.img_author, self.img_id, self.date_day)
                    description = self.img_alt
                    with ExifTool(etPath) as et:
                        params = map(fsencode, ['-Title=%s' % title,
                                                '-Headline=%s' % title,
                                                '-Object Name=%s' % title,
                                                '-Description=%s' % description,
                                                '-Image Description=%s' % description,
                                                '-Caption-Abstract=%s' % description,
                                                '-Author=%s' % author,
                                                '-Creator=%s' % author,
                                                '-Subject=%s' % keywords,
                                                '-Keywords=%s' % keywords,
                                                '-XPAuthor=%s' % author,
                                                '-XPKeywords=%s' % keywords,
                                                '-XPSubject=%s' % description,
                                                '-XPTitle=%s' % title,
                                                '-LastKeywordXMP=%s' % keywords,
                                                '-XPComment=%s' % comment,
                                                '%s' % imgPath])
                        et.execute(*params)

                    delFile = imgPath + '_original'
                    os.remove(delFile)
                    self.statusBar().setStyleSheet(self.color[3])
                    self.statusBar().showMessage(self.message[3] + self.scrape_directory)
                    break
        except Exception as e:
            print(e)
            self.statusBar().setStyleSheet(self.color[1])
            self.statusBar().showMessage('Ошибка сохранения: ' + str(e))
            return

    def stop_scrap(self, dataScrap):
        self.img_url = dataScrap[0]
        self.key_tag = dataScrap[1]
        self.img_src = dataScrap[2]
        self.img_alt = dataScrap[3]
        self.img_author = dataScrap[4]
        self.date_day = dataScrap[5]
        self.img_id = dataScrap[6]
        self.soldIndex = dataScrap[7]
        self.soldWords = dataScrap[8]
        self.notSoldWords = dataScrap[9]
        self.author_url = dataScrap[10]
        self.printSoldWords = ", ".join(self.soldWords)
        self.printSoldWords = self.printSoldWords.replace('"', '')
        self.printNotSoldWords = ", ".join(self.notSoldWords)
        self.printNotSoldWords = self.printNotSoldWords.replace('"', '')
        
        # печатаем
        self.Listbox.insertItem(0,'')
        self.Listbox.insertItem(0,'----------------------------------------')
        self.Listbox.insertItem(0,self.printNotSoldWords)
        self.Listbox.insertItem(0,'Не продающие({}):'.format(len(self.key_tag)-int(self.soldIndex)))
        self.Listbox.insertItem(0,self.printSoldWords)
        text = 'Всего {} ключей. '.format(str(len(self.key_tag))) + '{} из них продающие:'.format(self.soldIndex)
        self.Listbox.insertItem(0,text)
        self.Listbox.insertItem(0,self.img_alt)
        dopInfo = 'Автор: {}, ID: {}, Загружено: {}'.format(self.img_author, self.img_id, self.date_day)
        self.Listbox.insertItem(0,dopInfo)
        self.Listbox.insertItem(0,self.img_url)
        
        self.progressBar.setEnabled(False)

    def sendStart(self): # начало работы в Worker
        print('start')
        self.urlInput = self.urlEntry.text()
        self.Listbox.setEnabled(True)
        self.progressBar.setEnabled(True) # показать прогрессбар
        self.progressBar.setValue(0)
        self.startButton.hide() # смена кнопки старт на стоп
        if not self.threadWorker.isRunning():
            # приём значения прогрессбара
            self.threadWorker.progressChanged.connect(self.progressBar.setValue, QtCore.Qt.QueuedConnection)

            # приём сообщений
            self.threadWorker.buttonSend.connect(self.startButton.show, QtCore.Qt.QueuedConnection) # показать кнопку старт
            
            # передача переменных в доп поток
            self.threadWorker.urlSend = self.urlInput

            self.threadWorker.start()
        
    def sendStop(self): # остановить работу
        print('stop')
        self.progressBar.setValue(0)
        self.startButton.show()
        self.progressBar.setEnabled(False)
        self.threadWorker.flagFinished = True
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
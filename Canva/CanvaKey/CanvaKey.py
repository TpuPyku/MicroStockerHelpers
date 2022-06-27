# Python 3.8
#  Name: CanvaKey
#  Summary: Transfer of metadata from jpg to png files for uploading to Canva.com
#  Author: TpuPyku
#    Site github: https://github.com/TpuPyku
#    Site portfolio: https://tpupyku.myportfolio.com
# --------------------------------------------------
# Name: pyexiv2
# Version: 2.7.1
# Summary: Read/Write metadata(including EXIF, IPTC, XMP), comment and ICC Profile embedded in digital images.
# Home-page: https://github.com/LeoHsiao1/pyexiv2
# Author: LeoHsiao
# Author-email: leohsiao@foxmail.com
# License: GPLv3
# ---------------------------------------------------
# Name: exif2
# Version: 0.27.5-2019
# Home-page: https://exiv2.org/
# License: GPLv2

# UI tkinter
from tkinter import filedialog, Tk, messagebox
from tkinter.constants import SUNKEN, W, E, SW, BOTH, NORMAL, DISABLED
from tkinter.ttk import Progressbar, Frame, Label, Button, Style

# system
import os, threading, subprocess, platform, re, locale

# icon app
import base64
from icon import img

# import pyexiv2
try:
    import pyexiv2
except:
    print('Install pyexiv2...')
    subprocess.check_call('pip3 install pyexiv2', shell=True)
    if platform.system() == 'Darwin':
        print('Install gettext...')
        subprocess.check_call('brew install gettext', shell=True)
    import pyexiv2

class App(Frame):
    def __init__(self):
        super().__init__()
        # detect OS and apply path Exiv2
        def find_on_path(tool): # Find the first occurrence of a exiv2 on the path
            paths = os.environ['PATH'].split(os.pathsep)
            for path in paths:
                path = os.path.join(path, tool)
                if os.path.exists(path):
                    return path

        os_select = platform.system()
        if os_select == 'Windows':
            self.Exiv2Path = 'exiv2/Windows/exiv2.exe'
            type_file = [('Executable file', 'exiv2.exe')]
        elif os_select == 'Linux':
            self.Exiv2Path = 'exiv2/Linux/exiv2'
            type_file = [('App file', 'exiv2')]
        elif os_select == 'Darwin':
            self.Exiv2Path = 'exiv2/MacOS/exiv2'
            type_file = [('App file', '*exiv2')]
        else:
            self.Exiv2Path = 'exiv2'
            type_file = [('App file', '*')]

        if os.path.exists(self.Exiv2Path) == False:
            self.Exiv2Path = find_on_path('exiv2')
        if self.Exiv2Path == None:
            message = 'Please set the correct location or install exiv2 first.'
            messagebox.showwarning('Exiv2 is missing!', message)
            self.Exiv2Path = filedialog.askopenfilename(title='Set the exiv2 app', initialdir='/', filetypes=type_file)
            if self.Exiv2Path == '':
                messagebox.showerror('Canceled exiv2 selection', 'You canceled the exiv2 selection. \
                \nThe program will quit! \
                \nFirst install exiv2 or restart this program and select the correct exiv2. \
                \nDownload exiv2 https://exiv2.org/')
                exit()
        #print(self.Exiv2Path)

        # values
        self.jpg_directory = None
        self.png_directory = None

        self.initUI()

    def initUI(self): # main window ui
        self.style = Style()
        self.style.theme_use('clam')
        self.style.configure('blue.Horizontal.TProgressbar', foreground='blue', background='blue')
        self.pack(fill=BOTH, expand=True)
 
        self.columnconfigure(1, weight=1)
        self.columnconfigure(1, pad=7)
        self.rowconfigure(3, weight=1)

        # JPG widgets
        jpgDirLabel = Label(self, text='JPG:', width=5)
        self.jpgDirEntry = Label(self, text='Choise folder with .JPG', background='white', relief=SUNKEN, anchor=W, width=200)
        jpgDirButton = Button(self, text='Folder jpg..', width=10, command=self.jpgDialog)

        # PNG widgets
        pngDirLabel = Label(self, text='PNG:', width=5)
        self.pngDirEntry = Label(self, text='Choise folder with .PNG', background='white', relief=SUNKEN, anchor=W, width=200)
        pngDirButton = Button(self, text='Folder png..', width=10, command=self.pngDialog)

        # progress bar widget
        self.progressBar = Progressbar(self, style='blue.Horizontal.TProgressbar', length=300, mode='determinate')
        self.progressBar['value'] = 0
        self.pbLabel = Label(self, text='')

        # stop button
        self.stopButton = Button(self, text='Stop', width=10, command=self.sendStop)
        self.stopButton.grid_remove()
        # start button
        self.startButton = Button(self, text='Start', width=10, command=self.sendStart)
        # statusbar widget
        self.statusbar = Label(self, text='Choise folders and press Start', relief=SUNKEN, anchor=W, width=350)

        # grid in window
        jpgDirLabel.grid(     row=0, column=0, padx=5, pady=5, sticky=E)
        self.jpgDirEntry.grid(row=0, column=1, padx=5, pady=5)
        jpgDirButton.grid(    row=0, column=2, padx=5, pady=5)

        pngDirLabel.grid(     row=1, column=0, padx=5, pady=5, sticky=E)
        self.pngDirEntry.grid(row=1, column=1, padx=5, pady=5)
        pngDirButton.grid(    row=1, column=2, padx=5, pady=5)
        
        self.pbLabel.grid(    row=2, column=0, padx=5, pady=5)
        self.progressBar.grid(row=2, column=1, padx=5, pady=5)
        self.stopButton.grid( row=2, column=2, padx=5, pady=5)
        self.startButton.grid(row=2, column=2, padx=5, pady=5)

        self.statusbar.grid(row=3, column=0, columnspan=3, sticky=SW)

    def jpgDialog(self):
        self.jpg_directory = filedialog.askdirectory()
        a = chr(0x20)
        self.jpg_directory = re.sub(' ', a, self.jpg_directory)
        self.jpgDirEntry.config(text=self.jpg_directory)

    def pngDialog(self):
        self.png_directory = filedialog.askdirectory()
        a = chr(0x20)
        self.png_directory = re.sub(' ', a, self.png_directory)
        self.pngDirEntry.config(text=self.png_directory)

    def sendStart(self):
        self.statusbar.config(text='', background='')
        try:
            a = os.path.exists(self.jpg_directory)
            b = os.path.exists(self.png_directory)
        except:
            a = False
            b = False
            
        if a == False or b == False:
            self.statusbar.config(text='Select 2 folders, for JPG and PNG files!', background='pink')
            return

        self.progressBar['value']=0
        self.pbLabel.config(text='0%')
        self.startButton.grid_remove() # replacement start and stop buttons
        self.stopButton.grid()
        
        threadWorker = threading.Thread(target=self.Worker)
        #print(threading.main_thread().name)
        #print(threadWorker.name)
        threadWorker.start()

    def Worker(self):
        self.flagFinished = False
        try:
            os_encoding = locale.getpreferredencoding() # get OS encoding for path
            print('- OS encoding:', os_encoding)
            self.statusbar.config(text='Start working...', background='')

            # jpg files list in folder
            jpgList = []
            for file in os.listdir(self.jpg_directory):
                if file.endswith('.jpg'):
                    jpgList.append(file)
            print('JPG files in folder:\n', jpgList)

            # png files list in folder
            pngList = []
            for file in os.listdir(self.png_directory):
                if file.endswith('.png'):
                    pngList.append(file)
            print('PNG files in folder:\n', pngList)

            progressOne = int(100 / len(jpgList))
            progress = 0
            i = 0
            a = 0
            png = True
            for file in jpgList:
                if self.flagFinished == True:
                    self.statusbar.config(text='Stop working', background='yellow')
                    return
                
                jpgFile = file
                pngFile = jpgFile[0:(len(jpgFile) - 3)] + 'png'
                print('---------------------------------')
                print(f'Transfer metadata {file} to {pngFile}')
                self.statusbar.config(text=f'Metadata {jpgFile} transfer to {pngFile}', background='')
                print('---------------------------------')

                jpgPath = os.path.join(self.jpg_directory, jpgFile)
#               Modify exif informations
                try:
                    meta_jpg = pyexiv2.Image(jpgPath, encoding=os_encoding)
                    jpgTitle = ''
                    jpgKeywords = []
                    jpgDescription = ''
                    '''print('IPTC READ:\n', meta_jpg.read_iptc())
                    print('ICC READ:\n', meta_jpg.read_icc())
                    print('RAW READ:\n', meta_jpg.read_raw_xmp())
                    print('XMP READ:\n', meta_jpg.read_xmp())
                    print('EXIF READ:\n', meta_jpg.read_exif())'''
                    # Read Title
                    try:
                        jpgTitle = meta_jpg.read_xmp()['Xmp.dc.title']['lang="x-default"']
                        acept = 'xmp'
                    except:
                        acept = 'None'
                        #print('Title bad XMP data')
                    if jpgTitle == None or jpgTitle == '':
                        jpgTitle = meta_jpg.read_iptc()['Iptc.Application2.Headline']
                        acept = 'iptc'
                    if jpgTitle == None or jpgTitle == '':
                        #print('Title bad IPTC data')
                        jpgTitle = meta_jpg.read_exif().get('Exif.Image.XPTitle')
                        jpgTitle = re.sub('\\x00', '', jpgTitle)
                        acept = 'exif'
                    if jpgTitle == None or jpgTitle == '':
                        #print('Title bad EXIF data')
                        acept = 'None'
                    print(f'Acept title: {acept}')
                    
                    # Read Keywords
                    try:
                        jpgKeywords = meta_jpg.read_xmp().get('Xmp.dc.subject')
                        acept = 'xmp'
                    except:
                        acept = 'None'
                        #print('Keywords bad XMP data')
                    if jpgKeywords == None or jpgKeywords == '':
                        jpgKeywords = meta_jpg.read_iptc().get('Iptc.Application2.Keywords')
                        acept = 'iptc'
                    if jpgKeywords == None or jpgKeywords == '':
                        #print('Keywords bad IPTC data')
                        jpgKeywords = meta_jpg.read_exif().get('Exif.Image.XPKeywords')
                        jpgKeywords = re.sub('\\x00', '', jpgKeywords)
                        jpgKeywords = jpgKeywords.split(';')
                        acept = 'exif'
                    if jpgKeywords == None or jpgKeywords == '':
                        #print('Keywords bad EXIF data')
                        acept = 'None'
                    print(f'Acept keywords: {acept}')
                    
                    
                    # Read Description
                    try:
                        jpgDescription = meta_jpg.read_xmp()['Xmp.dc.description']['lang="x-default"']
                        acept = 'xmp'
                    except:
                        acept = 'None'
                        #print('Description bad XMP data')
                    if jpgDescription == None or jpgDescription == '':
                        jpgDescription = meta_jpg.read_iptc()['Iptc.Application2.Caption']
                        acept = 'iptc'
                    if jpgDescription == None or jpgDescription == '':
                        #print('Description bad IPTC data')
                        jpgDescription = meta_jpg.read_exif('Exif.Image.XPSubject')
                        jpgDescription = re.sub('\\x00', '', jpgDescription)
                        acept = 'exif'
                    if jpgDescription == None or jpgDescription == '':
                        #print('Description bad EXIF data')
                        acept = 'None'
                    print(f'Acept description: {acept}')
                    
                    #print('JPG XMP:\n', meta_jpg.read_xmp().keys(), '\nJPG IPTC:\n', meta_jpg.read_iptc().keys())
                    print('---JPG META---',
                        '\n- JPG Title:\n', jpgTitle,
                        '\n- JPG Keywords:\n', jpgKeywords,
                        '\n- JPG Descrip:\n', jpgDescription)
                except Exception as ex:
                    print(f'- Error read JPG:{jpgFile}\n', ex)
                    continue

#               transfer png
                try: 
                    pngList.index(pngFile)
                    pngPath = os.path.join(self.png_directory, pngFile)
                    try:
                        meta_png = pyexiv2.Image(pngPath, encoding=os_encoding)
                        #print('initiation png meta is OK')
                    except:
                        # command delete all meta. after Bridge exiv2 xpm toolkit get error 201
                        print(f'- PNG MetaData in {pngFile} file not standart. Meta cleaning...')
                        self.statusbar.config(text=f'PNG MetaData in {pngFile} file not standart. Meta cleaning...', background='yellow')
                        subprocess.check_call(f'{self.Exiv2Path} -d x "{pngPath}"', shell=False)
                        meta_png = pyexiv2.Image(pngPath, encoding='utf-8')

                    '''print('---PNG OLD META---',
                        '\nPNG XMP Title:\n', pngTitle,
                        '\nPNG XMP Keys:\n', pngKeywords,
                        '\nPNG XMP Descr:\n', pngDescription)'''
                    
#                   command Write tags
                    pngKeyTitle = {'Xmp.dc.title':jpgTitle}
                    meta_png.modify_xmp(pngKeyTitle)
                    pngKeyKeywords = {'Xmp.dc.subject':jpgKeywords}
                    meta_png.modify_xmp(pngKeyKeywords)
                    pngKeyDescription = {'Xmp.dc.description':jpgDescription}
                    meta_png.modify_xmp(pngKeyDescription)

                    # command Print tags
                    pngTitle = meta_png.read_xmp()['Xmp.dc.title']
                    pngKeywords = meta_png.read_xmp()['Xmp.dc.subject']
                    pngDescription = meta_png.read_xmp()['Xmp.dc.description']
                    print('---PNG NEW META---',
                        '\n- PNG XMP Title:\n', pngTitle,
                        '\n- PNG XMP Keys:\n', pngKeywords,
                        '\n- PNG XMP Descr:\n', pngDescription)

                    meta_png.close()
                    meta_jpg.close()
                except Exception as ex:
                    print('- Error png:', ex)
                    png = False

                # progressbar
                progress += progressOne
                self.progressBar['value']=progress
                self.pbLabel.config(text=f'{progress}%', state=NORMAL)

                if len(jpgList) < i:
                    return
                i+=1

                if png == False:
                    continue
                a+=1
                print('- Transfer completed')

            self.statusbar.config(text=f'Finish. {a} files out of {len(pngList)} processed', background='green')
            self.progressBar['value']=100
            self.pbLabel.config(text='100%')
            self.stopButton.grid_remove()
            self.startButton.grid()
            self.flagFinished = True
            print(f'- Finish. {a} files out of {len(pngList)} processed')
        except Exception as e:
            print('- Error transfer exif:', e)
            self.statusbar.config(text=f'Error transfer exif: {e}', background='pink')
            self.flagFinished = True
            return

    def sendStop(self): # Stop treading
        print('- Stop')
        self.progressBar['value']=0
        self.pbLabel.config(text='', state=DISABLED)
        self.stopButton.grid_remove()
        self.startButton.grid()
        self.flagFinished = True

    def stop_convert(self): # to future
        print('- Stop')

def MainWindow():
    root = Tk()
    root.title('CanvaKey 0.3.211123')
    root.geometry('350x150')

    tmp = open('temp.ico','wb+')
    tmp.write(base64.b64decode(img))
    tmp.close()
    root.iconbitmap('temp.ico')
    os.remove('temp.ico')

    app = App()
    root.mainloop()

if __name__ == '__main__':
    MainWindow()
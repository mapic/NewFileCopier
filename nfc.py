import sys
import copier
import getopt
import os
import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
import pickle


def printhelp():
    print('New file copier')
    print('Usage:')
    print('nfc -b -c -s <源路径> -d <目标路径> [-p <数据文件名>]')
    print('-b --build 建立源路径数据')
    print('-c --copy 从源路径，复制修改了的文件，到目标路径')
    print('-s --srcdir 源文件夹路径')
    print('-d --dstdir 目标文件夹路径')
    print('-p --profile 建立或读取源路径数据时，数据文件名，默认文件名 db')
    print('-h 帮助')
    print('例子：')
    print('nfc -b -s srcpath')
    print('nfc -b -s srcpath -p dbname')
    print('nfc -c -s srcpath -d dstpath')
    print('nfc -c -s srcpath -d dstpath -p dbname')


def settext(textgui, text):
    textgui.configure(state='normal')
    textgui.delete('1.0', 'end')
    textgui.insert('end', text)
    textgui.configure(state='disabled')


def gettext(textgui):
    return textgui.get('1.0', 'end').strip()


def showmsg(msg):
    tkmb.showinfo('消息', msg)


def rungui():
    root = tk.Tk()

    setting = {
        'dbname': 'db',
        'srcdir': '',
        'dstdir': ''
    }

    settingfilepath = 'nsfSettingFile'

    if os.path.exists(settingfilepath):
        with open(settingfilepath, 'rb') as sf:
            setting = pickle.load(sf)

    frame = tk.Frame(root)
    frame.pack()

    srcbtn = tk.Button(frame, text='源目录')
    srcbtn.grid(column=0, row=0)

    srctext = tk.Text(frame, width=80, height=1)
    srctext.configure(state='disabled')
    settext(srctext, setting['srcdir'])
    srctext.grid(column=1, row=0)

    dstbtn = tk.Button(frame, text='目标目录')
    dstbtn.grid(column=0, row=1)

    dsttext = tk.Text(frame, width=80, height=1)
    dsttext.configure(state='disabled')
    settext(dsttext, setting['dstdir'])
    dsttext.grid(column=1, row=1)

    dbnbtn = tk.Button(frame, text='数据文件')
    dbnbtn.grid(column=0, row=2)

    dblbt = tk.Text(frame, width=80, height=1)
    dblbt.configure(state='disabled')
    settext(dblbt, setting['dbname'])
    dblbt.grid(column=1, row=2, sticky='w')

    scanbtn = tk.Button(frame, text='生成源目录数据文件')
    scanbtn.grid(column=0, row=3, pady=20)
    cpybtn = tk.Button(frame, text='复制新文件到目标目录')
    cpybtn.grid(column=1, row=3, sticky='w')

    def sk():
        d = tkfd.askdirectory()
        if d == '':
            return
        settext(srctext, d)
        setting['srcdir'] = d

    def dk():
        d = tkfd.askdirectory()
        if d == '':
            return
        settext(dsttext, d)
        setting['dstdir'] = d

    def setdbn():
        d = tkfd.asksaveasfilename()
        if d == '':
            return
        settext(dblbt, d)
        setting['dbname'] = d

    def checksrcdir():
        if not os.path.isdir(setting['srcdir']):
            tkmb.showinfo(title='消息', message='请设置正确的 源目录')
            return False
        return True

    def checkdbn():
        if setting['dbname'] == '':
            tkmb.showinfo(title='消息', message='请设置 数据文件')
            return False
        return True

    def checkdstdir():
        if not os.path.isdir(setting['dstdir']):
            tkmb.showinfo(title='消息', message='请设置正确的 目标目录')
            return False
        return True

    def startscan():
        if not (checksrcdir() and checkdbn()):
            return
        copier.scan(setting['srcdir'], setting['dbname'])
        showmsg('数据建立完成！')

    def startcopy():
        if not (checksrcdir() and checkdstdir() and checkdbn()):
            return
        if setting['srcdir'] == setting['dstdir']:
            tkmb.showinfo('消息', '源目录 和 目标目录 不能一样')
            return
        if not os.path.exists(setting['dbname']):
            tkmb.showinfo('消息', '数据文件不存在，请先生成 源目录 数据')
            return
        copier.startcopy(setting['srcdir'], setting['dstdir'], setting['dbname'])
        showmsg('文件复制完成！')

    srcbtn['command'] = sk
    dstbtn['command'] = dk
    dbnbtn['command'] = setdbn
    scanbtn['command'] = startscan
    cpybtn['command'] = startcopy

    root.title("新文件复制工具 - by 小试刀剑")
    root.mainloop()
    with open(settingfilepath, 'wb') as sf:
        pickle.dump(setting, sf)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        rungui()
        sys.exit(0)

    try:
        opts, args = getopt.getopt(args[1:], 'hbcs:d:p:', ['build', 'copy', 'srcdir==', 'dstdir==', 'profile=='])
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)

    srcdir = ''
    dstdir = ''
    datafilepath = 'db'
    isbuild = False
    iscopy = False

    for opt, value in opts:
        if opt == '-h':
            printhelp()
            sys.exit(0)
        if opt in ('-b', '--build'):
            isbuild = True
        if opt in ('-c', '--copy'):
            iscopy = True
        if opt in ('-s', '--srcdir'):
            srcdir = value
        if opt in ('-d', '--dstdir'):
            dstdir = value
        if opt in ('-p', '--profile'):
            datafilepath = value

    if isbuild and (srcdir == ''):
        print('请设置 源路径')
        sys.exit(0)
    if iscopy:
        if srcdir == '' or dstdir == '':
            print('请设置 源路径 和 目标路径')
            sys.exit(0)
        if not os.path.exists(datafilepath):
            print('请先建立源路径的数据')
            sys.exit(0)

    if isbuild:
        copier.scan(srcdir, datafilepath)
    elif iscopy:
        copier.startcopy(srcdir, dstdir, datafilepath)
    else:
        printhelp()
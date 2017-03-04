# coding:utf-8

"""
只可用于Windows平台
"""

import json
import requests
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import win32com.client
import webbrowser


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def __del__(self):
        print('del tianyanche')

    def createWidgets(self):
        self.contentDest = tk.StringVar()
        self.contentDest.set('\uf649')
        self.entryDest = tk.Entry(self, width=40)
        self.entryDest["textvariable"] = self.contentDest
        self.entryDest.grid(row=0)
        self.entryDest.focus()
        self.entryDest.bind('<Return>', lambda event: self.start())

        self.buttonStart = tk.Button(self, text='ヽ(ˋ▽ˊ)ノ ', width=25)
        self.buttonStart['command'] = self.start
        self.buttonStart['fg'] = 'black'
        self.buttonStart.grid(row=1)

        self.text = ScrolledText(self, font=('Courier New', 13), fg='green', bg='black', width=30)
        self.text.grid(row=2, columnspan=1)

    def start(self):
        self.running = True
        self.td = threading.Thread(target=self.startThread)
        self.td.setDaemon(True)
        self.td.start()

    def get_info(self, t):
        url = "http://www.tuling123.com/openapi/api"
        data = {
            "key": "13e4499c33c27055a3c7ee2904b8",
            "info": t,
            "userid": "masong"
        }
        content = requests.post(url, data=data).content
        result = json.loads(content)
        return result["text"]

    def startThread(self):
        try:
            spk = win32com.client.Dispatch("SAPI.SpVoice")
            t = self.contentDest.get()
            self.text.delete(0.0, "end")
            self.text.insert("end", u"正在为您检索:【%s】的应答\n" % t)
            t = self.get_info(t)
            if not t:
                t = "不好意思，服务出问题了"
            self.text.delete(0.0, "end")
            self.text.insert("end", u"检索结果如下：\n")
            self.text.insert("end", t)
            spk.Speak(t)
        except Exception as e:
            pass
            self.text.delete(0.0, "end")
            self.text.insert("end", "请先安装TTS模块(用以文字转语音)")
            webbrowser.open("https://www.baidu.com/s?wd=Windows怎么安装TTS模块")


root = tk.Tk()
root.withdraw()
app = Application(master=root)
root.title("懒人搜索")
try:
    root.iconbitmap("logo.ico")
except:
    pass
screen_width = root.winfo_screenwidth()
root.resizable(False, False)
root.update_idletasks()
root.deiconify()
screen_height = root.winfo_screenheight() - 100
root.geometry('%sx%s+%s+%s' % (
    root.winfo_width() + 10, root.winfo_height() + 10, (screen_width - root.winfo_width()) / 2,
    (screen_height - root.winfo_height()) / 2))
root.deiconify()
app.mainloop()

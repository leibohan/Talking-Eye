from tkinter import *
import tkinter.filedialog
import requests
import os
from PIL import Image
from PIL import ImageTk
import paramiko


class uploadDemo:
    def __init__(self):
        window = Tk()
        self.ready = False
        window.title('上传图片')
        window.minsize(640, 555)
        frame0 = Frame(window)
        frame0.pack()
        lblInfo = Label(frame0, text='请选择您想要提问的图片')
        lblInfo.grid(row=1, column=1)
        btn = Button(frame0, text='选择图片', command=self.xz)
        btn.grid(row=1, column=2)
        btnUpload = Button(frame0, text='确认上传',
                           command=self.upload).grid(row=1, column=3)
        frame1 = Frame(window)
        frame1.pack()
        self.lb = Label(frame1)
        self.lb.grid(row=1, column=1)
        self.canvas = tkinter.Canvas(bg="white", width=640, height=480)
        self.canvas.place(x=0, y=50)
        self.lblUp = Label(frame1)
        self.lblUp.grid(row=2, column=1)
        window.mainloop()

    def xz(self):
        self.filename = tkinter.filedialog.askopenfilename(title='请选择您想上传的图片')
        if self.filename == '':
            self.ready = False
            self.lb.config(text="您没有选择图片")
            self.canvas.delete('all')
        elif self.filename[-4:] == ".png" or self.filename[-4:] == ".jpg" or self.filename[-4:] == "jpeg" or self.filename[-4:] == ".bmp" or self.filename[-4:] == ".gif":
            self.ready = True
            photo = Image.open(self.filename)
            img = ImageTk.PhotoImage(photo)  # 用PIL模块的PhotoImage打开
            self.canvas.create_image(320, 240, image=img)
            self.lb.config(text="您选择的图片是：" + self.filename)
            load = Image.open(self.filename)
            render = ImageTK.PhotoImage(load)
            img.image = render
        else:
            self.ready = False
            self.lb.config(text='不是图片文件或者不支持的类型')
            self.canvas.delete('all')

    def upload(self):
        print('check')
        if self.ready:
            self.lb.config(text='已上传')
            do_upload(self.filename)
        else:
            self.lb.config(text='当前无可上传文件')


def do_upload(filename):
    ssh = paramiko.SSHClient()
    # 这行代码的作用是允许连接不在know_hosts文件中的主机。
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("221.122.128.54", 31011, "meirtz", {password})
    stdin, stdout, stderr = ssh.exec_command('ls')
    print(stdout.readlines())
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    file_name = filename.split('/')[-1]
    print(filename)
    print(file_name)
    sftp.put(filename, "/home/meirtz/hackathon/" + file_name)
    # shell = "scp -P 31011 " + "/Users/apple/Downloads/upload.py" + \
    #         " {user}@221.122.128.54:/home/meirtz/hackathon/"
    print('finish')


uploadDemo()

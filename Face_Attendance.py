import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time



def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)



def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)



def contact():
    mess._show(title='連絡先', message="メール : 'nishahamed2018@gmail.com' ")

#------------------------------------------------------------------------------#

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='必要なファイルがありません', message='haarcascade_frontalface_default.xmlファイルが見つかりませんでした')
        window.destroy()

#------------------------------------------------------------------------------#

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\pass.txt")
    if exists1:
        tf = open("TrainingImageLabel\pass.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('パスワードが見つかりませんでした', '新しいパスワードの入力', show='*')
        if new_pas == None:
            mess._show(title='パスワードを入力してください', message='パスワードが設定されていませんからもう一度入力してください')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='パスワードが登録されました', message='新しいパスワードが登録されました!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='エラー', message='新しいパスワードを確認して下さい')
            return
    else:
        mess._show(title='パスワードが間違っています', message='もう一度確認して入力してください')
        return
    mess._show(title='パスワードが変更されました', message='パスワードが変更されました!!')
    master.destroy()

#------------------------------------------------------------------------------#

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("パスワード変更")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='前のパスワード',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='新パスワードを入力', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='新パスワードの確認', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="キャンセル", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="保存", command=save_pass, fg="black", bg="#363636", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#------------------------------------------------------------------------------#

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('前のパスワードが見つかりませんでした', '新パスワードを入力してください', show='*')
        if new_pas == None:
            mess._show(title='パスワードが入力されていないです', message='パスワードが設定されていないです！！')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='パスワードが設定されました', message='新パスワードが設定されました!!')
            return
    password = tsd.askstring('パスワード', 'パスワード入力', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='パスワード間違っています', message='入力されたパスワードが間違っています')

#------------------------------------------------------------------------------#

def clear():
    txt.delete(0, 'end')
    res = "1)顔データを取る  >>>>  2)Profileを保存する"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)顔データを取る  >>>>  2)Profileを保存する"
    message1.configure(text=res)

#------------------------------------------------------------------------------#

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # sample numberの増加
                sampleNum = sampleNum + 1
                # TrainingImageフォルダにイメージデータを保存する
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('イメージデータを取っています', img)
            # 100 milisecondsまで待つ
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # サンプル数が100を超える場合はbreakする
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "このIDのイメージデータを取りました : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "名前を入力してください"
            message.configure(text=res)

#------------------------------------------------------------------------------#

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='登録何もされていません', message='新規登録のほう一人を登録してください!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profileが保存されました"
    message1.configure(text=res)
    message.configure(text='今までの登録総数  : ' + str(ID[0]))

#------------------------------------------------------------------------------#

def getImagesAndLabels(path):
    # フォルダ内のすべてのファイルのパスを取得する
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # 空のface listの作成
    faces = []
    # 空のID listの作成
    Ids = []
    # すべての画像パスをloopしてIDと画像を読み込む
    for imagePath in imagePaths:
        # 読み込んだ画像をgray scaleにする
        pilImage = Image.open(imagePath).convert('L')
        # PIL image into numpy arrayの変換
        imageNp = np.array(pilImage, 'uint8')
        # 画像からIDを取る
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # Training画像から顔を抽出する
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

#------------------------------------------------------------------------------#

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='データが見つかりませんでした', message='データをresetする為profileを保存するボタンを押してください!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='詳細がありません', message='顔認識データが見つかりませんでした、確認してください!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

#　時間、日付の設定
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'1月',
      '02':'2月',
      '03':'3月',
      '04':'4月',
      '05':'5月',
      '06':'6月',
      '07':'7月',
      '08':'8月',
      '09':'9月',
      '10':'10月',
      '11':'11月',
      '12':'12月'
      }

#　ユーザーインタフェース GUI

window = tk.Tk()
window.geometry("1280x650")
window.resizable(True,False)
window.title("出席システム")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#D6CFC7")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#D6CFC7")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="顔認識出席システム" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       　　新規登録　　                        ", fg="white",bg="#363636" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       登録されている場合                      ", fg="white",bg="#363636" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="IDを入力してください",width=20  ,height=1  ,fg="black"  ,bg="#D6CFC7" ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="名前を入力してください",width=20  ,fg="black"  ,bg="#D6CFC7" ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)顔データを取る  >>>>  2)Profileを保存する" ,bg="#D6CFC7" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#D6CFC7" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="出席",width=20  ,fg="black"  ,bg="#D6CFC7"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

lbl3 = tk.Label(frame1, text="nishahamed2018@gmail.com",width=20  ,fg="black"  ,bg="#D6CFC7"  ,height=1 ,font=('times', 9, ' bold '))
lbl3.place(x=170, y=500)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='今までの登録総数  : '+str(res))

#　メニュー

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='パスワード変更', command = change_pass)
filemenu.add_command(label='問い合わせ', command = contact)
filemenu.add_command(label='閉じる',command = window.destroy)
menubar.add_cascade(label='ヘルプ',font=('times', 29, ' bold '),menu=filemenu)

#　TreeView出席テーブル設定

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='名前')
tv.heading('date',text ='日付')
tv.heading('time',text ='時間')

#　スクロールバー設定

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

# Button

clearButton = tk.Button(frame2, text="クリア", command=clear  ,fg="black"  ,bg="grey"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="クリア", command=clear2  ,fg="black"  ,bg="grey"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)    
takeImg = tk.Button(frame2, text="顔データを取る", command=TakeImages  ,fg="black"  ,bg="grey"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Profileを保存する", command=psw ,fg="black"  ,bg="grey"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="出席を取る", command=TrackImages  ,fg="black"  ,bg="grey"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="閉じる", command=window.destroy  ,fg="black"  ,bg="grey"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)



window.configure(menu=menubar)
window.mainloop()

#--------------------------------------------------------------------------------------------------#

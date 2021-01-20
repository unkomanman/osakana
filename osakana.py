import time
import pandas as pd
import tkinter as tk
import datetime
import pytz

kiroku = pd.DataFrame(columns=['Area', 'time'])


class Application(tk.Frame):
    def __init__(self,master):
        global kiroku

        super().__init__(master)
        self.pack()

        master.geometry("500x400")
        master.title("おさかな")
        master.config(bg="black")

        self.startTime=time.time()
        self.stopTime=0.0
        self.elapsedTime=0.0
        self.playTime=False

        self.canvas = tk.Canvas(master,width=300,height=80,bg="skyblue")
        self.canvas.place(x=3,y=10)

        tk.Button(master,text="記録終了",command=self.resetButtonClick,width=10).place(x=10, y=110)
        tk.Button(master,text="スタート",command=self.startButtonClick,width=10).place(x=110, y=110)
        tk.Button(master,text="ストップ",command=self.stopButtonClick,width=10).place(x=210, y=110)
        tk.Button(master,text="A",command= lambda : self.check("A", zikan=self.elapsedTime),width=10).place(x=10, y=210)
        tk.Button(master,text="B",command= lambda : self.check("B", zikan=self.elapsedTime),width=10).place(x=110, y=210)
        tk.Button(master,text="C",command= lambda : self.check("C", zikan=self.elapsedTime),width=10).place(x=10, y=310)
        tk.Button(master,text="D",command= lambda : self.check("D", zikan=self.elapsedTime),width=10).place(x=110, y=310)
        tk.Button(master,text="やり直す",command=self.undo,width=10).place(x=10, y=160)

        self.message= tk.StringVar()
        self.message.set("記録")
        tk.Message(master,textvariable=self.message,width=300,).place(x=330,y=10)

        master.after(50,self.update)
    
    def check(self, area, zikan):
        global kiroku
      
        kiroku = kiroku.append({'Area': area,'time': zikan}, ignore_index=True)
    
        self.message.set( kiroku )
    
    def undo(self):
        global kiroku
        kiroku.drop([len(kiroku)- 1 ], inplace=True)
        self.message.set( kiroku )


    def startButtonClick(self):
        if not self.playTime:
            self.startTime=time.time()-self.elapsedTime
            self.playTime=True

    def stopButtonClick(self):
        if self.playTime:
            self.stopTime=time.time()-self.startTime
            self.playTime=False

    def resetButtonClick(self):
        global kiroku
        self.startTime=time.time()
        self.stopTime=0.0
        self.elapsedTime=0.0
        self.playTime=False
        dtnow = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        hiduke = dtnow.strftime('%Y年%m月%d日%H%M%S')
        filepath = f'osakanadata/{hiduke}.csv'
        kiroku.to_csv( filepath )

    def update(self):
        self.canvas.delete("Time")
        if self.playTime:
            self.elapsedTime=time.time()-self.startTime
            self.canvas.create_text(280,40,text=round(self.elapsedTime,1),font=("Helvetica",40,"bold"),fill="black",tag="Time",anchor="e")
        else:
            self.canvas.create_text(280,40,text=round(self.stopTime,1),font=("Helvetica",40,"bold"),fill="black",tag="Time",anchor="e")

        self.master.after(50,self.update)

    
    


def main():
    win = tk.Tk()
    #win.resizable(width=False, height=False) #ウィンドウを固定サイズに
    app = Application(master=win)
    app.mainloop()

if __name__ == "__main__":
    main()

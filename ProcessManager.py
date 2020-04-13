# Importing Modules

from tkinter import *
import psutil
import subprocess
import platform
import MySQLdb
import pymsgbox
from datetime import *
import multiprocessing

# Database table layout  (pid,name,username,status,time)
# password : pro123

class ProcessMan():
    def __init__(self,root,next_frame,curr_frame = None):
        self.root = root
        
        ScreenSizeX = root.winfo_screenwidth()  # Get screen width [pixels]
        ScreenSizeY = root.winfo_screenheight() # Get screen height [pixels]
        ScreenRatio = 0.8                              # Set the screen ratio for width and height
        FrameSizeX  = int(ScreenSizeX * ScreenRatio)
        FrameSizeY  = int(ScreenSizeY * ScreenRatio)
        FramePosX   = (ScreenSizeX - FrameSizeX)/2 # Find left and up border of window
        FramePosY   = (ScreenSizeY - FrameSizeY)/2
        root.geometry("%dx%d+%d+%d"%(FrameSizeX,FrameSizeY,FramePosX,FramePosY-20))
        
        self.next_frame = next_frame
        self.frame = curr_frame
        self.switch_frame()
    
    def switch_frame(self):
        new_frame = self.next_frame(self.root)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame

class LoginPage(ProcessMan):
    def __init__(self,root):
        self.f = Frame(root,height = 691, width = 1228)
        self.f.pack()
        self.v = StringVar()
        self.L1  = Label(self.f,text="WELCOME TO PROCESS MANAGER \n\n Login to continue...", font = ("",-30,"")).place(x = 350 , y = 150)
        self.L2 = Label(self.f,text = "Enter Admin Password : ",font = ("",-20,"")).place(x = 400, y = 300)
        self.pwd = Entry(self.f,show = '*',width = 30,textvariable = self.v).place( x= 620,y = 307)
               
        self.loginbtn = Button(self.f,text = "Login",font = ("",-15,""),command = self.check ,width = 15).place(x = 525 , y = 350)
        self.CloseAppbtn = Button(self.f,text = "Exit",font = ("",-15,""),command = lambda: root.destroy() ,width = 15).place(x = 525,y = 390)
    def check(self):
        conn = MySQLdb.connect(host = 'localhost',user = 'root' ,password = 'root123' , database = 'process_manager')
        cursor = conn.cursor()
        try:
            cursor.execute("select * from password")
            row = cursor.fetchone()
            pawd = row[0]
            cursor.close()
            conn.close()
        except:
            print("Retrieval Error")
        
        if pawd == self.v.get(): 
            super(LoginPage,self).__init__(root,MainPage,self.f)
        else:
            root.withdraw()
            pymsgbox.alert(text = "Wrong Password !",title = "Error", button = "OK")
            root.deiconify()
            
class MainPage(ProcessMan):
    def __init__(self,root):
        self.f = Frame(root,height = 691, width = 1228)
        self.f.pack()
        
        self.logoutbtn = Button(self.f,text = "Logout",font = ("",-15,""),command = lambda: super(MainPage,self).__init__(root,LoginPage,self.f)).place(x = 1100 , y = 20)
        self.L = Label(self.f,text = "Select process category..... ",font = ("",-35,"")).place(x = 100,y = 100)
        self.L1 = Label(self.f,text = "Running processes",font =("",-20,"")).place(x = 100 , y = 200)
        self.L2 = Label(self.f,text = "Top 15 memory consuming processes",font =("",-20,"")).place(x = 100 , y = 275)
        self.L3 = Label(self.f,text = "Top 15 CPU time consuming processes",font =("",-20,"")).place(x = 100 , y = 350)
        self.L4 = Label(self.f,text = "All processes",font =("",-20,"")).place(x = 100 , y = 425)
        
        self.B1 = Button(self.f,text = ("View"),font =("",-17,""),command = lambda : super(MainPage,self).__init__(root,RunningPro,self.f)).place(x = 500 , y = 200)
        self.B2 = Button(self.f,text = ("View"),font =("",-17,""),command = lambda : super(MainPage,self).__init__(root,TopMem,self.f)).place(x = 500 , y = 275)
        self.B3 = Button(self.f,text = ("View"),font =("",-17,""),command = lambda : super(MainPage,self).__init__(root,TopCPU,self.f)).place(x = 500 , y = 350)
        self.B4 = Button(self.f,text = ("View"),font =("",-17,""),command = lambda : super(MainPage,self).__init__(root,AllPro,self.f)).place(x = 500 , y = 425)
        
        self.C = Canvas(self.f,height = 400,width = 3,bg = "black").place(x = 600 , y  = 100)
        m = psutil.virtual_memory().total
        m = m/(1024**3)
        self.RL = Label(self.f,text = "System information..... ",font = ("",-35,"")).place(x = 700,y = 100)
        self.RL1 = Label(self.f,text = "Operating System : %s" % platform.system(),font =("",-20,"")).place(x = 700 , y = 200)
        self.RL1 = Label(self.f,text = "Processor : %s" % platform.processor()[:-25],font =("",-20,"")).place(x = 700 , y = 275)
        Label(self.f,text = "Total memory : %.2f GB" % m ,font =("",-20,"")).place(x = 700 , y = 350)
        Label(self.f,text = "Number of CPU's : %d " % multiprocessing.cpu_count(),font =("",-20,"")).place(x = 700 , y = 425)
        
        Label(self.f,text = "Application Activity : ",font =("",-25,"")).place(x = 100,y = 600)
        Button(self.f,text = ("Activity"),font =("",-17,""),command = lambda : super(MainPage,self).__init__(root,Activity,self.f)).place(x = 350 , y = 600)
        
class RunningPro(ProcessMan):
    def __init__(self,root):
        self.root = root
        self.f = Frame(self.root,height = 691, width = 1228)
        self.f.pack()
        Label(self.f,text = "Current running processes....",font = ("",-35,"")).place(x= 10,y = 10)
        self.rows=0
        self.counter = 0
        self.generate_list()
    
        self.table = Frame(self.f,height = 500, width = 1228)
        
        e1 = Label(self.table,width = 25,text = "Process ID",font = ("",-15,"bold")).grid(row = 0,column = 0)
        e2 = Label(self.table,width = 25,text = "Process Name",font = ("",-15,"bold")).grid(row = 0,column = 1)
        e3 = Label(self.table,width = 25,text = "Memory Usage (MB)",font = ("",-15,"bold")).grid(row = 0,column = 2)
        e4 = Label(self.table,width = 25,text = "User",font = ("",-15,"bold")).grid(row = 0,column = 3)
        e5 = Label(self.table,width = 25,text = "Process Status",font = ("",-15,"bold")).grid(row = 0,column = 4)
        
        for i in range(5):
            self.C = Canvas(self.table,height = 1,width = 200,bg = "black").grid(row = 1,column = i)
           
        for i in range(self.rows):
            if i < 25:
                for j in range(5):
                    self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                    self.e.grid(row = i+2,column = j)
                    self.counter = i+1
                            
        self.table.place(x = 0 , y = 70)
        
        Canvas(self.f,height = 1,width = 1228,bg = "black").place(x = 0,y = 640)
           
        Button(self.f,text = "Back",font=("",-15,""),command=lambda : super(RunningPro,self).__init__(self.root,MainPage,self.f)).place(x=1100,y=20)
        Button(self.f,text = "Refresh",font=("",-15,""),command=lambda : super(RunningPro,self).__init__(self.root,RunningPro,self.f)).place(x = 10 ,y = 650)
        Button(self.f,text = "Next -->",font=("",-15,""),command = self.page2).place(x=120,y=650)
        
        Label(self.f,text = "Enter process ID to kill : ",font=("",-15,"bold")).place(x = 600,y = 650)
        self.str1 = StringVar()
        self.pidEntry = Entry(self.f,width = 15,textvariable = self.str1).place(x = 785,y = 653)
        Button(self.f,text = "Kill",font = ("",-15,""),command=self.kill).place(x = 890,y = 648)
        
    def cal(self,n):
        value_bytes = n * 8471822991.36
        value_mb = value_bytes/(1024.00**3)
        return "%-.2f" %value_mb
    
    def generate_list(self):
        self.pro_list = []
        for p in psutil.process_iter(attrs=['pid','name', 'username','status','memory_percent']):
            q = psutil.Process(p.pid)
            if p.info['username'] == '<USERNAME>' and p.info['status'] == psutil.STATUS_RUNNING:
                self.pro_list.append((p.pid, p.info['name'],self.cal(p.info['memory_percent']),p.info['username'],p.info['status']))
                self.rows+=1
    
    def page2(self):
        for i in range(25,self.rows):
            if i < 50:
                for j in range(5):
                        self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                        self.e.grid(row = (i+2)-25,column = j)
        Button(self.f,text = "Next -->",font=("",-15,""),command = self.page3).place(x=120,y=650)
        
    def page3(self):
        for i in range(50,self.rows):
            if i < 75:
                for j in range(5):
                    self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                    self.e.grid(row = (i+2)-50,column = j)
    
    def kill(self):
        self.root.withdraw()
        ans = pymsgbox.confirm(text = "Kill Process",title ="Confirm Action",buttons = ["OK","CANCEL"])
        if(ans != "OK"):
            return
        pid = int(self.str1.get())
        q = psutil.Process(pid)
        d_t = str(datetime.today())
        #in_values = (q.pid,q.name(),q.username(),q.status(),str(datetime.today()))
        try:
            conn = MySQLdb.connect(host = 'localhost',user = 'root' ,password = 'root123' , database = 'process_manager')
            cursor = conn.cursor()
            cursor.execute("insert into process(pid,name,username,status,time) values(%s,%s,%s,%s,%s)",(int(q.pid),q.name(),q.username(),q.status(),d_t[:-7]))
            conn.commit()
        except:
            conn.rollback()
            print("Error in updating database!")
        cursor.close()
        conn.close()
        
        try:
            s = "taskkill /pid '%d' /t /f"
            sc = subprocess.Popen(["powershell",s % pid], stdout=subprocess.PIPE)
            print(sc.communicate)
        except:
            print(" Taskkill Error")
        finally:
            self.root.deiconify()

class TopMem(ProcessMan):
    def __init__(self,root):
        self.root = root
        self.f = Frame(self.root,height = 691, width = 1228)
        self.f.pack()
        Label(self.f,text = "Top 15 memory consuming processes....",font = ("",-35,"")).place(x= 10,y = 10)
        
        self.generate_list()
    
        self.table = Frame(self.f,height = 500, width = 1228)
        
        e1 = Label(self.table,width = 25,text = "Process ID",font = ("",-15,"bold")).grid(row = 0,column = 0)
        e2 = Label(self.table,width = 25,text = "Process Name",font = ("",-15,"bold")).grid(row = 0,column = 1)
        e3 = Label(self.table,width = 25,text = "Memory Usage (MB)",font = ("",-15,"bold")).grid(row = 0,column = 2)
        e4 = Label(self.table,width = 25,text = "User",font = ("",-15,"bold")).grid(row = 0,column = 3)
        e5 = Label(self.table,width = 25,text = "Process Status",font = ("",-15,"bold")).grid(row = 0,column = 4)
        
        for i in range(5):
            self.C = Canvas(self.table,height = 1,width = 200,bg = "black").grid(row = 1,column = i)
           
        for i in range(15):
            if i < 25:
                for j in range(5):
                    self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                    self.e.grid(row = i+2,column = j)
                            
        self.table.place(x = 0 , y = 70)
        
        Canvas(self.f,height = 1,width = 1228,bg = "black").place(x = 0,y = 640)
           
        Button(self.f,text = "Back",font=("",-15,""),command=lambda : super(TopMem,self).__init__(self.root,MainPage,self.f)).place(x=1100,y=20)
        Button(self.f,text = "Refresh",font=("",-15,""),command=lambda : super(TopMem,self).__init__(self.root,TopMem,self.f)).place(x = 10 ,y = 650)
        
        Label(self.f,text = "Enter process ID to kill : ",font=("",-15,"bold")).place(x = 600,y = 650)
        self.str1 = StringVar()
        self.pidEntry = Entry(self.f,width = 15,textvariable = self.str1).place(x = 790,y = 650)
        Button(self.f,text = "Kill",font = ("",-15,""),command=self.kill).place(x = 890,y = 650)
        
    def cal(self,n):
        value_bytes = n * 8471822991.36
        value_mb = value_bytes/(1024.00**3)
        return "%-.2f" %value_mb
    
    def generate_list(self):
        l = []
        for p in psutil.process_iter(attrs=['pid','name', 'username','status','memory_percent']):
            l.append((p.pid, p.info['name'],self.cal(p.info['memory_percent']),p.info['username'],p.info['status']))
        s_list = sorted(l,key = lambda k: k[2],reverse = True)
        self.pro_list =  s_list[:15]
        
    def kill(self):
        self.root.withdraw()
        ans = pymsgbox.confirm(text = "Kill Process",title ="Confirm Action",buttons = ["OK","CANCEL"])
        if(ans != "OK"):
            return
        pid = int(self.str1.get())
        q = psutil.Process(pid)
        d_t = str(datetime.today())
        try:
            conn = MySQLdb.connect(host = 'localhost',user = 'root' ,password = 'root123' , database = 'process_manager')
            cursor = conn.cursor()
            cursor.execute("insert into process(pid,name,username,status,time) values(%s,%s,%s,%s,%s)",(int(q.pid),q.name(),q.username(),q.status(),d_t[:-7]))
            conn.commit()
        except:
            conn.rollback()
            print("Error in updating database!")
        cursor.close()
        conn.close()
        
        try:
            s = "taskkill /pid '%d' /t /f"
            sc = subprocess.Popen(["powershell",s % pid], stdout=subprocess.PIPE)
            print(sc.communicate)
        except:
            print("Error")
        finally:
            self.root.deiconify()

class TopCPU(ProcessMan):
    def __init__(self,root):
        self.root = root
        self.f = Frame(self.root,height = 691, width = 1228)
        self.f.pack()
        Label(self.f,text = "Top 15 CPU time consuming processes....",font = ("",-35,"")).place(x= 10,y = 10)
        self.rows=0
        self.generate_list()
    
        self.table = Frame(self.f,height = 500, width = 1228)
        
        e1 = Label(self.table,width = 25,text = "Process ID",font = ("",-15,"bold")).grid(row = 0,column = 0)
        e2 = Label(self.table,width = 25,text = "Process Name",font = ("",-15,"bold")).grid(row = 0,column = 1)
        e3 = Label(self.table,width = 25,text = "CPU Time (sec)",font = ("",-15,"bold")).grid(row = 0,column = 2)
        e4 = Label(self.table,width = 25,text = "User",font = ("",-15,"bold")).grid(row = 0,column = 3)
        e5 = Label(self.table,width = 25,text = "Process Status",font = ("",-15,"bold")).grid(row = 0,column = 4)
        
        for i in range(5):
            self.C = Canvas(self.table,height = 1,width = 200,bg = "black").grid(row = 1,column = i)
           
        for i in range(15):
            if i < 25:
                for j in range(5):
                    self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                    self.e.grid(row = i+2,column = j)
                            
        self.table.place(x = 0 , y = 70)
        
        Canvas(self.f,height = 1,width = 1228,bg = "black").place(x = 0,y = 640)
           
        Button(self.f,text = "Back",font=("",-15,""),command=lambda : super(TopCPU,self).__init__(self.root,MainPage,self.f)).place(x=1100,y=20)
        Button(self.f,text = "Refresh",font=("",-15,""),command=lambda : super(TopCPU,self).__init__(self.root,TopCPU,self.f)).place(x = 10 ,y = 650)
        
        Label(self.f,text = "Enter process ID to kill : ",font=("",-15,"bold")).place(x = 600,y = 650)
        self.str1 = StringVar()
        self.pidEntry = Entry(self.f,width = 15,textvariable = self.str1).place(x = 790,y = 650)
        Button(self.f,text = "Kill",font = ("",-15,""),command=self.kill).place(x = 890,y = 650)
        
    def cal(self,n):
        value_bytes = n * 8471822991.36
        value_mb = value_bytes/(1024.00**3)
        return "%-.2f" %value_mb
    
    def generate_list(self):
        l = []
        for p in psutil.process_iter(attrs=['pid','name', 'username','status','cpu_times']):
            l.append((p.pid, p.info['name'],sum(p.info['cpu_times'][:2]),p.info['username'],p.info['status']))
        s_list = sorted(l,key = lambda k: k[2],reverse = True)
        self.pro_list =  s_list[:15]
        
    def kill(self):
        self.root.withdraw()
        ans = pymsgbox.confirm(text = "Kill Process",title ="Confirm Action",buttons = ["OK","CANCEL"])
        if(ans != "OK"):
            return
        pid = int(self.str1.get())
        q = psutil.Process(pid)
        d_t = str(datetime.today())
        try:
            conn = MySQLdb.connect(host = 'localhost',user = 'root' ,password = 'root123' , database = 'process_manager')
            cursor = conn.cursor()
            cursor.execute("insert into process(pid,name,username,status,time) values(%s,%s,%s,%s,%s)",(int(q.pid),q.name(),q.username(),q.status(),d_t[:-7]))
            conn.commit()
        except:
            conn.rollback()
            print("Error in updating database!")
        cursor.close()
        conn.close()
        
        try:
            s = "taskkill /pid '%d' /t /f"
            sc = subprocess.Popen(["powershell",s % pid], stdout=subprocess.PIPE)
            print(sc.communicate)
        except:
            print("Error")
        finally:
            self.root.deiconify()
        
class AllPro(ProcessMan):
    def __init__(self,root):
        self.root = root
        self.f = Frame(self.root,height = 691, width = 1228)
        self.f.pack()
        Label(self.f,text = "All processes....",font = ("",-35,"")).place(x= 10,y = 10)
        self.rows=0
        self.generate_list()
    
        self.table = Frame(self.f,height = 500, width = 1228)
        
        e1 = Label(self.table,width = 25,text = "Process ID",font = ("",-15,"bold")).grid(row = 0,column = 0)
        e2 = Label(self.table,width = 25,text = "Process Name",font = ("",-15,"bold")).grid(row = 0,column = 1)
        e3 = Label(self.table,width = 25,text = "Memory Usage (MB)",font = ("",-15,"bold")).grid(row = 0,column = 2)
        e4 = Label(self.table,width = 25,text = "User",font = ("",-15,"bold")).grid(row = 0,column = 3)
        e5 = Label(self.table,width = 25,text = "Process Status",font = ("",-15,"bold")).grid(row = 0,column = 4)
        
        for i in range(5):
            self.C = Canvas(self.table,height = 1,width = 200,bg = "black").grid(row = 1,column = i)
           
        for i in range(self.rows):
            if i < 25:
                for j in range(5):
                    self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                    self.e.grid(row = i+2,column = j)
                            
        self.table.place(x = 0 , y = 70)
        
        Canvas(self.f,height = 1,width = 1228,bg = "black").place(x = 0,y = 640)
           
        Button(self.f,text = "Back",font=("",-15,""),command=lambda : super(AllPro,self).__init__(self.root,MainPage,self.f)).place(x=1100,y=20)
        Button(self.f,text = "Refresh",font=("",-15,""),command=lambda : super(AllPro,self).__init__(self.root,AllPro,self.f)).place(x = 10 ,y = 650)
        Button(self.f,text = "Next -->",font=("",-15,""),command = self.page2).place(x=120,y=650)
        
        Label(self.f,text = "Enter process ID to kill : ",font=("",-15,"bold")).place(x = 600,y = 650)
        self.str1 = StringVar()
        self.pidEntry = Entry(self.f,width = 15,textvariable = self.str1).place(x = 790,y = 650)
        Button(self.f,text = "Kill",font = ("",-15,""),command=self.kill).place(x = 890,y = 650)
        
    def cal(self,n):
        value_bytes = n * 8471822991.36
        value_mb = value_bytes/(1024.00**3)
        return "%-.2f" %value_mb
    
    def generate_list(self):
        self.pro_list = []
        for p in psutil.process_iter(attrs=['pid','name', 'username','status','memory_percent']):
            self.pro_list.append((p.pid, p.info['name'],self.cal(p.info['memory_percent']),p.info['username'],p.info['status']))
            self.rows+=1
    
    def page2(self):
        for i in range(25,self.rows):
            if i < 50:
                for j in range(5):
                        self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                        self.e.grid(row = (i+2)-25,column = j)
        Button(self.f,text = "Next -->",font=("",-15,""),command = self.page3).place(x=120,y=650)
        
    def page3(self):
        for i in range(50,self.rows):
            if i < 75:
                for j in range(5):
                    self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                    self.e.grid(row = (i+2)-50,column = j)
        Button(self.f,text = "Next -->",font=("",-15,""),command = self.page4).place(x=120,y=650)
    
    def page4(self):
        for i in range(75,self.rows):
            if i < 100:
                for j in range(5):
                    self.e = Label(self.table,text = self.pro_list[i][j],width = 25)
                    self.e.grid(row = (i+2)-75,column = j)
    
    
    def kill(self):
        self.root.withdraw()
        ans = pymsgbox.confirm(text = "Kill Process",title ="Confirm Action",buttons = ["OK","CANCEL"])
        if(ans != "OK"):
            return
        pid = int(self.str1.get())
        q = psutil.Process(pid)
        d_t = str(datetime.today())
        try:
            conn = MySQLdb.connect(host = 'localhost',user = 'root' ,password = 'root123' , database = 'process_manager')
            cursor = conn.cursor()
            cursor.execute("insert into process(pid,name,username,status,time) values(%s,%s,%s,%s,%s)",(int(q.pid),q.name(),q.username(),q.status(),d_t[:-7]))
            conn.commit()
        except:
            conn.rollback()
            print("Error in updating database!")
        cursor.close()
        conn.close()
        
        try:
            s = "taskkill /pid '%d' /t /f"
            sc = subprocess.Popen(["powershell",s % pid], stdout=subprocess.PIPE)
            print(sc.communicate)
        except:
            print(" Taskkill Error")
        finally:
            self.root.deiconify()
            
class Activity(ProcessMan):
    def __init__(self,root):
        self.root = root
        self.f = Frame(self.root,height = 691, width = 1228)
        self.f.pack()
        Label(self.f,text = "List of processes killed....",font = ("",-35,"")).place(x= 10,y = 10)
        
        self.data = []
        self.generate_list()
        self.rows=len(self.data)
        self.table = Frame(self.f,height = 500, width = 1228)
        
        e1 = Label(self.table,width = 25,text = "Process ID",font = ("",-15,"bold")).grid(row = 0,column = 0)
        e2 = Label(self.table,width = 25,text = "Process Name",font = ("",-15,"bold")).grid(row = 0,column = 1)
        e3 = Label(self.table,width = 25,text = "User",font = ("",-15,"bold")).grid(row = 0,column = 2)
        e4 = Label(self.table,width = 25,text = "Process Status",font = ("",-15,"bold")).grid(row = 0,column = 3)
        e5 = Label(self.table,width = 25,text = "Date & Time",font = ("",-15,"bold")).grid(row = 0,column = 4)
        
        for i in range(5):
            self.C = Canvas(self.table,height = 1,width = 200,bg = "black").grid(row = 1,column = i)
           
        for i in range(self.rows):
            if i < 25:
                for j in range(5):
                    self.e = Label(self.table,text = self.data[i][j],width = 25)
                    self.e.grid(row = i+2,column = j)
                    self.counter = i+1
                            
        self.table.place(x = 0 , y = 70)
        
        Canvas(self.f,height = 1,width = 1228,bg = "black").place(x = 0,y = 640)
           
        Button(self.f,text = "Back",font=("",-15,""),command=lambda : super(Activity,self).__init__(self.root,MainPage,self.f)).place(x=1100,y=20)
        Button(self.f,text = "Refresh",font=("",-15,""),command=lambda : super(Activity,self).__init__(self.root,Activity,self.f)).place(x = 10 ,y = 650)
        
    
    def generate_list(self):
        conn = MySQLdb.connect(host = 'localhost',user = 'root' ,password = 'root123' , database = 'process_manager')
        cursor = conn.cursor()
        try:
            cursor.execute("select * from process")
            self.data = cursor.fetchall()
        except:
            print("Retrieval Error !")
        
        cursor.close()
        conn.close()

if __name__ == "__main__":
    root = Tk()
    root.title("Process Manager")
    root.iconbitmap(default = 'Bar-chart.ico')
    app = ProcessMan(root,LoginPage)
    root.mainloop()

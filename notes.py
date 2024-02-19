import pandas as pd
import os
from datetime import datetime
from tkinter import messagebox


class Notes:
    # Пандас
    df = pd.DataFrame(data = [[0,"First Note(Automated)","This Book was created at that moment",datetime.now()]], columns = ["id","title","body","datetime"])
    filepath = ""
    def __init__(self,filepath : str):
        self.filepath = filepath
        if os.path.exists(filepath):
            try:
                data = pd.read_csv(filepath,index_col=0)
                if len(data.columns) == len(self.df.columns) and (data.columns == self.df.columns).all():
                    self.df = data
                    messagebox.showinfo("InfoBOx","Data  loaded")
                    print("Data been loaded")
                else:
                    # Проверка на соответствие колонок
                    mb =messagebox.askyesno('Warning',"File will be rewritten")
                    if mb:
                        with open(filepath,"w") as f:
                            self.df.to_csv(filepath)
                    else: exit()
            except pd.errors.EmptyDataError:
                print("File is empty")
                with open(filepath,"w") as f:
                    self.df.to_csv(filepath)
                    messagebox.showinfo("InfoBOx","Empty File")
        else:
            with open(filepath,"w") as f:
                self.df.to_csv(filepath)
                messagebox.showinfo("InfoBOx","File has been created")
            
        self.df.id = self.df.id.astype(int)
        self.df.title = self.df.title.astype(str)
        self.df.body = self.df.body.astype(str)
        self.df.datetime = pd.to_datetime(self.df.datetime)
        self.df.sort_values('datetime',ascending=False,inplace = True)
        self.df.reset_index(drop= True,inplace=True)
    
    
    def save(self):
        with open(self.filepath,"w") as f:
            self.df.to_csv(self.filepath)
            messagebox.showinfo("InfoBOx","File saved")
            print("File saved")
        
    def add(self,title:str,msg:str):
        self.df.reset_index(inplace=True, drop=True)
        # Добавление записи с уникальным id
        self.df.loc[len(self.df.index)] = [self.df.sort_values("id").iloc[len(self.df.index)-1,0]+1, title,msg,datetime.now()]
        messagebox.showinfo("InfoBOx","Note added")
        print("Note added")
        
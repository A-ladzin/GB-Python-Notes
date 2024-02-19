from tkinter import *
from tkinter import messagebox
from functools import partial

class NotesWindow(Toplevel):
    # Окно заметок сорт бай дата
    def __init__(self, notes,master = None):
        super().__init__(master = master)
        self.mindate = self.master.mindate
        self.maxdate = self.master.maxdate
    
        self.title("My Notes")
        self.geometry("400x300")
        self.resizable(False,False)
        self.notes = notes
        self.master = master
        self.canvas = Canvas(self)
        self.scrollbar = Scrollbar(self,orient='vertical',command=self.canvas.yview)
        self.canvas.config(scrollregion=self.bbox("all"))
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
                        "<Configure>",
                        lambda e: self.canvas.configure(
                            scrollregion=self.canvas.bbox("all")
                        )
                    )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        nrow = 1
        
        def format_text(body,idx = None, length = 30):
            if idx == None:
                new_lines_idx = [i for i in range(len(body)) if body.startswith("\n", i)]
            else:
                new_lines_idx = [i for i in range(idx) if body.startswith("\n", i)]
            new_lines_idx.insert(0,0)
            for i in range(len(new_lines_idx)-1,0,-1):
                if (i == 0): 
                    break
                if new_lines_idx[i]-new_lines_idx[i-1] > length:
                    new_new_line_idx = new_lines_idx[i]-min(length,(new_lines_idx[i]-new_lines_idx[i-1] - length))
                    body = body[:new_new_line_idx]+"\n"+body[new_new_line_idx:]
                    return format_text(body,new_new_line_idx+3)
            return body
        
        for i in notes.df.index:
            # проверка календаря
            if self.mindate is not None and self.maxdate is not None:
                if notes.df.loc[i,"datetime"].date() < self.mindate or notes.df.loc[i,"datetime"].date() > self.maxdate:
                    continue
            body = notes.df.loc[i,"body"]+"\n"
            body = format_text(body, length = 50)
            title = notes.df.loc[i,"title"]+"\n"
            title = format_text(title)
            
            Label(self.scrollable_frame,text="-"*10).grid(row=nrow-1,column =0)
            edit_action = partial(self.edit_note,i)
            edit_button = Button(self.scrollable_frame,text='Edit',command = edit_action,)
            edit_button.grid(row=nrow,column = 0)
            
            delete_action = partial(self.delete_note,i)
            delete_button = Button(self.scrollable_frame,text='Delete',command = delete_action,)
            delete_button.grid(row=nrow+1,column = 0)
        
            Label(self.scrollable_frame,text=title+"  -  "*(2)).grid(row = nrow+1,column = 1)
            Label(self.scrollable_frame,text=body).grid(row=nrow+2,column = 1)
            Label(self.scrollable_frame,text=f"{notes.df.loc[i,"datetime"].strftime('%Y-%m-%d %X')}").grid(row=nrow,column = 2)
            Label(self.scrollable_frame,text=f"  -----   ").grid(row=nrow+3,column = 1)
            nrow+=5
            
        self.canvas.grid(row=0,column=0,sticky="nw")
        self.scrollbar.grid(row=0,column=1,sticky="nse")
        
    def edit_note(self,note_idx: int):
        EditFrame(self.notes,self.master,note_idx)
        self.destroy()
        
    def delete_note(self,note_idx: int):
        def confirm_delete(confirm:bool):
            if confirm:
                self.notes.df.drop(note_idx,axis = 0,inplace = True)
                self.notes.df.reset_index(inplace = True,drop = True)
                NotesWindow(self.notes,self.master)
                self.destroy()
            
        mb = messagebox.askyesno("Warning","Are you sure?")
        confirm_delete(mb)
        
        
# Окошко редактирования заметки      
class EditFrame(Toplevel):
    def __init__(self,notes,master=None, idx = None):
        super().__init__(master = master)
        self.notes = notes
        self.idx = idx
        self.note = notes.df.loc[idx]
        self.inputTitle = Text(self,height = 1,width=20)
        self.inputTitle.insert("1.0",self.note["title"].strip())
        self.inputMessage = Text(self, 
                        height = 5, 
                        width = 20) 
        self.inputMessage.insert("1.0",self.note["body"].strip())
        Label(self,text = self.notes.df.loc[idx,'datetime']).grid(row = 0, column = 1)
        self.inputTitle.grid(row=1,column=1)
        self.inputMessage.grid(row=2,column=1)
        save = partial(self.exit, True)
        cancel = partial(self.exit, False)
        self.save_button = Button(self, text = "Save", command = save)
        self.cancel_button = Button(self,text = "Cancel", command = cancel)
        self.save_button.grid(row = 3, column = 0)
        self.cancel_button.grid(row = 3, column = 2)
        
        
    def exit(self, save: bool):
        if save:
            self.notes.df.loc[self.idx,'title'] = self.inputTitle.get("1.0","end")
            self.notes.df.loc[self.idx,'body']= self.inputMessage.get("1.0","end")
        NotesWindow(self.notes,self.master)
        self.destroy()
        
                                            
        

        
        
        
        
            
        
        
        
    
from tkinter import *
from notes import Notes
from window import NotesWindow
from calendarillus import Calendarillus
from tkinter import filedialog, messagebox







class NotesApp(Toplevel):
    def __init__(self,master):
        master.withdraw()
        super().__init__(master = master)
        self.nn = Notes(filedialog.askopenfile("r",title = "Choose a file ",filetypes= (("CSV Files","*.csv"),)).name)
        self.mindate = None
        self.maxdate = None
        
        self.title("Notes App") 
        self.geometry('400x200')         
        # TextBox Creation 
        self.inputTitle = Text(self,height = 1,width=20)
        self.inputMessage = Text(self, 
                        height = 5, 
                        width = 20) 
        
        self.inputTitle.grid(row=0,column=1)
        self.inputMessage.grid(row=1,column=1)
        # Buttons Creation 
        self.addButton = Button(self, 
                                text = "Add Note",  
                                command = self.add_note) 
        self.addButton.grid(row = 2, column=0)

        self.readButton = Button(self,
                                text = "Read Notes")

        self.readButton.bind("<Button>", 
                lambda e: NotesWindow(self.nn,self))

        self.readButton.grid(row =2 , column = 2)


        self.saveButton = Button(self,text = "Save", command = self.nn.save)
        self.saveButton.grid(row=0,column=2)

        self.openButton = Button(self,text = "Open",command = self.open_notes)
        self.openButton.grid(row = 1, column = 2)


        self.calendarButton = Button(self, text = "Calendar", command= self.open_calendar)
        self.calendarButton.grid(row = 2, column = 1)
        
        self.titleLabel = Label(self, text = "Title") 
        self.titleLabel.grid(row=0,column=0) 

        self.textLabel = Label(self, text = "Message") 
        self.textLabel.grid(row=1,column=0) 
        self.mainloop()


  

  


    # Button commands
    def add_note(self):
        self.nn.add(self.inputTitle.get("1.0","end"),
                                            self.inputMessage.get("1.0","end"))
        
    def open_calendar(self):
        cal = Calendarillus(self,2024,2,19,selectmode = 'day')
        cal.pack()
        
    def confirm_save(self,confirm:bool):
        if confirm:
            self.nn.save()
        self.nn = Notes(filedialog.askopenfile("r",title = "Choose a file ",filetypes= (("CSV Files","*.csv"),)).name)
        

    def open_notes(self):
        self.mindate = None
        self.maxdate = None
        mb = messagebox.askyesno("Alert","Save_changes?")
        self.confirm_save(mb)


    
    
if __name__ == '__main__':
    root = Tk()
    NotesApp(root)
    


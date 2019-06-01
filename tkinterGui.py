import tkinter as tk
from tkinter import filedialog
from tkinter import font

from PIL import ImageTk, Image

import hta

class MainGui:
    def __init__(self, master):
        self.master = master
        self.workingFolder = None
        self.mainFile = None
        master.title("HTA")
        
        tempImg = Image.open("Gradient.png")
        tempImg = tempImg.resize((600, 638))

        self.gradient = ImageTk.PhotoImage(tempImg)
        self.bgImage = tk.Label(master, image=self.gradient)
        self.bgImage.place(x=0, y=0, relwidth=1, relheight=1)

        self.img = ImageTk.PhotoImage(Image.open("HTA Logo.png"))
        self.ImgWidget = tk.Label(master, image=self.img)
        self.ImgWidget.place(x=9, y=9, relwidth=1, relheight=1, width=-18, height=-311)

        self.inputFrame = tk.Frame(master)
        self.inputFrame.place(x=50, y=347, relwidth=1, relheight=1, width=-100, height=-360)

        self.SDASFrame = tk.Frame(self.inputFrame)
        self.sdasPrompt = tk.Label(self.SDASFrame, text="SDAS (m)")
        self.sdasPrompt.pack(side=tk.LEFT)
        self.sdasField = tk.Entry(self.SDASFrame, font=default_font)
        self.sdasField.pack()
        self.SDASFrame.pack(pady=10)

        self.WorkingFolderButton = tk.Button(self.inputFrame, text="Browse for working folder", command=self.chooseWorkingFolder)
        self.WorkingFolderButton.pack()

        self.displayWorkingFolder = tk.Label(self.inputFrame, text="")
        self.displayWorkingFolder.pack()

        self.MainFileButton = tk.Button(self.inputFrame, text="Select main file", command=self.chooseMainFile)
        self.MainFileButton.pack()

        self.displayMainFile = tk.Label(self.inputFrame, text="")
        self.displayMainFile.pack()

        self.RunButton = tk.Button(self.inputFrame, text="Run computation", command=self.run)
        self.RunButton.pack()

        self.runResult = tk.Label(self.inputFrame, text="")
        self.runResult.pack()

    def chooseWorkingFolder(self):
        temp = filedialog.askdirectory(initialdir="C:\\")
        if temp is not None and temp != "":
            self.workingFolder = temp
            self.displayWorkingFolder["text"] = "You chose: " + self.workingFolder

        self.runResult["text"] = ""

    def chooseMainFile(self):
        if self.workingFolder is None:
            self.runResult["text"] = "Please select a working folder first."
        else:
            temp = filedialog.askopenfile(initialdir=self.workingFolder, filetypes=[("DATAPLOT files", "*.exp")])
            if temp is not None and temp != "":
                self.mainFile = temp.name
                self.displayMainFile["text"] = "You chose: " + self.mainFile

    def run(self):
        if self.workingFolder is None:
            self.runResult["text"] = "Please choose a folder containing files for chemistries."
            return
        if self.mainFile is None:
            self.runResult["text"] = "Please choose a main file."
            return
        try:
            sdas = float(self.sdasField.get())
        except ValueError:
            self.runResult["text"] = "Please enter the secondary dendrite arm spacing (SDAS)."
            return

        mainFile = self.mainFile[self.mainFile.rfind("/") + 1:]

        try:
            lines, solidus = hta.runMain(self.workingFolder, mainFile, sdas)
        except OSError as e:
            self.runResult["text"] = "Error creating directory.  Perhaps the directory is protected?"
            raise
            return

        self.runResult["text"] = "Outputs have been created.\nThere were {} lines and the solidus was {}.".format(lines, solidus)

root = tk.Tk()
root.geometry("600x638")
root.resizable(0, 0)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=13)

def runGui():

    gui = MainGui(root)
    root.mainloop()


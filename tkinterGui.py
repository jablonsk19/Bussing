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

        self.img = ImageTk.PhotoImage(Image.open("HTA Logo.png"))
        self.ImgWidget = tk.Label(master, image=self.img)
        self.ImgWidget.pack()

        self.spacer_1 = tk.Label(master, text="")
        self.spacer_1.pack()

        self.SDASFrame = tk.Frame(master)
        self.sdasPrompt = tk.Label(self.SDASFrame, text="SDAS (m)")
        self.sdasPrompt.pack(side=tk.LEFT)
        self.sdasField = tk.Entry(self.SDASFrame, font=default_font)
        self.sdasField.pack()
        self.SDASFrame.pack()

        self.spacer_2 = tk.Label(master, text="")
        self.spacer_2.pack()

        self.WorkingFolderButton = tk.Button(master, text="Browse for working folder", command=self.chooseWorkingFolder)
        self.WorkingFolderButton.pack()

        self.displayWorkingFolder = tk.Label(master, text="")
        self.displayWorkingFolder.pack()

        self.MainFileButton = tk.Button(master, text="Select main file", command=self.chooseMainFile)
        self.MainFileButton.pack()

        self.displayMainFile = tk.Label(master, text="")
        self.displayMainFile.pack()

        self.RunButton = tk.Button(master, text="Run computation", command=self.run)
        self.RunButton.pack()

        self.runResult = tk.Label(master, text="")
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
            temp = filedialog.askopenfile(initialdir=self.workingFolder)
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
default_font.configure(size=12)

def runGui():

    gui = MainGui(root)
    root.mainloop()


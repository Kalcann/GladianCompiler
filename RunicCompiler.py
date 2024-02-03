import sys
from tkinter import *
from tkinter import font
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd

content = []
fileSelector = None

class Rune():
    def __init__(self, stringValue):
        self.__values = []
        for i in stringValue:
            if i=='0':
                self.__values.append(False)
            else:
                self.__values.append(True)
    def getGridValue(self, index):
        return self.__values[index]
    def getGridValues(self):
        return self.__values

def openFile():
    global fileSelector
    global content
    try:
        file = open("compiled.dat")
        for line in file:
            stringValue, name = line.rstrip('\n').split(',')
            content.append([Rune(stringValue), name])
        for i in content:
            contentList.insert(END, i[1])
        contentList.insert(END, "--Add New--")
    except IOError:
        fileSelector = Toplevel(root)
        fileSelector.geometry("250x125")
        fileSelector.protocol("WM_DELETE_WINDOW", myExit)
        label = Label(fileSelector, text="compiled.dat not found", font=listFont, padx=20, pady=10)
        label.pack()
        newFile = Button(fileSelector, text="Create new file?", font=listFont, command=createnewFile, pady=10)
        newFile.pack()
        fileSelector.grab_set()
     
       
def myExit():
    sys.exit()
        
def createnewFile():
    global fileSelector
    open("compiled.dat", 'x')
    contentList.insert(END, "--Add New--")
    fileSelector.destroy()
    root.focus()
    
currentSelected = -1

def moveUp():
    global currentSelected
    global contentList
    global content
    if currentSelected > 0:
        contentList.delete(currentSelected)
        contentList.insert(currentSelected-1, content[currentSelected][1])
        content[currentSelected], content[currentSelected-1] = content[currentSelected-1], content[currentSelected]
        currentSelected -= 1
        contentList.select_set(currentSelected)
        


def moveDown():
    global currentSelected
    global contentList
    global content
    if currentSelected < len(content)-1 and currentSelected > -1:
        contentList.delete(currentSelected)
        contentList.insert(currentSelected+1, content[currentSelected][1])
        content[currentSelected], content[currentSelected+1] = content[currentSelected+1], content[currentSelected]
        currentSelected += 1
        contentList.select_set(currentSelected)
        
def search():
    global searchItemButtonStates
    global searchLabel
    global buttons
    searchItemButtonStates = [False for i in range(25)]
    searchItemWin = Toplevel(root)
    searchItemWin.title("Search")
    searchItemWin.geometry("400x200")
    searchItemWin.grab_set()
    buttonFrame = Frame(searchItemWin)
    buttons = [Button(buttonFrame, image=buttonOff, command=lambda l=i: searchLatticeButton(l)) for i in range(25)]
    for y in range(5):
        for x in range(5):
            buttons[y*5 +x].grid(column=x, row=y)
        
    buttonFrame.pack(side=LEFT, padx=15, pady=5)
    searchLabel = Label(searchItemWin, font=listFont, width=15, text='')
    searchLabel.pack(anchor='center', pady=70)
    
def delete():
    global currentSelected
    global contentList
    global content
    global selectionLabel
    global DisplayGrid
    if(currentSelected != -1):
        contentList.delete(currentSelected)
        content.pop(currentSelected)
        currentSelected = -1
        selectionLabel.config(text='')
        for button in DisplayGrid:
            button.config(image=gridEmpty)
        
        
        

#main window set up
root = Tk()
root.title("Runic Compiler")
root.geometry("600x400")

contentFrame = Frame(root)
#contentFrame

contentBar = Scrollbar(contentFrame, orient=VERTICAL)
contentBar.pack(fill=Y, side = RIGHT)

listFont = font.Font(family="Helvetica", size="16")
contentList = Listbox(contentFrame, width = 25, yscrollcommand=contentBar.set, font=listFont)
contentList.pack(fill=BOTH, expand=YES)
contentBar.config(command=contentList.yview)

contentFrame.pack(fill=Y, side=RIGHT)


buttonOn = PhotoImage(file="toggleOn.png")
buttonOff = PhotoImage(file="toggleOff.png")
gridEmpty = PhotoImage(file="GridEmpty.png")
gridPresent = PhotoImage(file="GridPresent.png")

#display
displayFrame = Frame(root)

selectionLabel = Label(text = "", font = listFont)
selectionLabel.pack(anchor='n', pady = 10)
ImageFrame = Frame(displayFrame)

DisplayGrid = [Label(ImageFrame,image=gridEmpty) for i in range(25)]
for y in range(5):
    for x in range(5):
        DisplayGrid[y*5 + x].grid(column=x, row=y, padx=0, pady=0)

ImageFrame.pack(padx=5)

buttonGrid = Frame(displayFrame)
moveFrame = Frame(buttonGrid)

upButton = Button(moveFrame, text="Move Up", command=moveUp)
downButton = Button(moveFrame, text="Move Down", command=moveDown)
upButton.pack(anchor='n')
downButton.pack(anchor='s')

moveFrame.grid(row=0, column=2, padx=5)
searchButton = Button(buttonGrid, text="Search", command=search, font=listFont)
searchButton.grid(row=0, column=1, padx=5)
deleteButton = Button(buttonGrid, text="delete", command=delete, font=listFont)
deleteButton.grid(row=0, column=0, padx=5)

buttonGrid.pack(pady=10)
displayFrame.pack(side=RIGHT, fill=BOTH)



def latticeButton(index):
    global buttons
    newItemButtonStates[index] = not newItemButtonStates[index]
    if newItemButtonStates[index]:
        buttons[index].config(image=buttonOn)
    else:
        buttons[index].config(image=buttonOff)
        
def searchLatticeButton(index):
    global searchItemButtonStates
    global searchLabel
    global content
    global buttons
    searchItemButtonStates[index] = not searchItemButtonStates[index]
    if searchItemButtonStates[index]:
        buttons[index].config(image=buttonOn)
    else:
        buttons[index].config(image=buttonOff)
    for cont in content:
        if cont[0].getGridValues() == searchItemButtonStates:
            searchLabel.config(text=cont[1])
            return
        searchLabel.config(text='')
        
def confirmNewItem():
    global content
    global newItemWin
    global newItemEntry
    global newItemButtonStates
    newItemWin.grab_release()
    buttonsEmpty = True
    for i in newItemButtonStates:
        if i == True:
            buttonsEmpty = False
            
    nameUsed = False
    for i in content:
        if i[1].lower() == newItemEntry.get().lower():
            nameUsed = True
    if newItemEntry.get() == '' or buttonsEmpty:
        showinfo(title="Error", message="invalid entry")
        newItemWin.focus()
        newItemWin.grab_set()
    elif newItemEntry.get() == "--Add New--":
        showinfo("Nice Try Asshole")
        newItemWin.focus()
        newItemWin.grab_set()
    elif nameUsed:
        showinfo("Name Already in Use")
        newItemWin.focus()
        newItemWin.grab_set()
    else:
        string= ''
        for i in range(25):
            if newItemButtonStates[i]:
                string += '1'
            else:
                string += '0'
        content.append([Rune(string), newItemEntry.get()])
        contentList.insert(len(content)-1, content[-1][1])

                

        newItemWin.destroy()
        root.focus()
        

def onSelectItem(event):
    global newItemButtonStates
    global newItemWin
    global buttons
    global newItemEntry
    global content
    global DisplayGrid
    global selectionLabel
    global currentSelected
    if contentList.curselection != None:
        if contentList.get(contentList.curselection()) == "--Add New--": #create a new window if addnewitem is pressed
        
            newItemButtonStates = [False for i in range(25)]
            newItemWin = Toplevel(root)
            newItemWin.title("Add Item")
            newItemWin.geometry("400x200")
            newItemWin.grab_set()
            buttonFrame = Frame(newItemWin)
            buttons = [Button(buttonFrame, image=buttonOff, command=lambda l=i: latticeButton(l)) for i in range(25)]
            for y in range(5):
                for x in range(5):
                    buttons[y*5 +x].grid(column=x, row=y)
        
            buttonFrame.pack(side=LEFT, padx=15, pady=5)
            newItemEntry = Entry(newItemWin, font=listFont, width=15, justify=CENTER)
            newItemEntry.pack(pady=50)
            confirm = Button(newItemWin, text="confirm", command=confirmNewItem)
            confirm.pack()
        else:
            index = contentList.index(contentList.curselection())
            selectionLabel.config(text=content[index][1])
            for i in range(25):
                if(content[index][0].getGridValue(i)):
                    DisplayGrid[i].config(image=gridPresent)
                else:
                    DisplayGrid[i].config(image=gridEmpty)
            currentSelected = index
            
def saveAndExit():
    global content
    file = open("compiled.dat", 'w')
    for cont in content:
        string = ''
        for val in cont[0].getGridValues():
            if val:
                string += '1'
            else:
                string += '0'
        file.write(f"{string},{cont[1]}\n")
    sys.exit()
            
        

contentList.bind('<<ListboxSelect>>', onSelectItem)

newItemWin = None


searchItemButtonStates = [False for i in range(25)]
searchLabel = NONE

buttons = []
newItemEntry = None
newItemButtonStates = [False for i in range(25)]

root.protocol("WM_DELETE_WINDOW", saveAndExit)

root.after(500, openFile)
root.mainloop()

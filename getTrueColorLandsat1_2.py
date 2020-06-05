import cv2 as cv
import sys, os
#import tkinter as tk
#from tkinter import filedialog
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from landsatCore import getTrueColorLandsat, colorCorrect, convertToFinal

# GUI: LANDSAT TRUE COLOR IMAGE CONVERTER
# V1.0 June 1 2020
# CREATED BY DEREK PICKELL

def run(folder):
    """
    Functionality: executes main processing sequence using core landsat library
    """
    try:
        button2.setText("processing...")
        print("merging images...")
        print(folder)
        mergedImage = getTrueColorLandsat(folder)
        print("color correcting...")
        B, G, R = cv.split(mergedImage)
        Bnew = colorCorrect(B)
        Gnew = colorCorrect(G)
        Rnew = colorCorrect(R)
        colorCorrected = cv.merge((Bnew, Gnew, Rnew))
        print("saving image...")
        convertToFinal(colorCorrected, folder)
        print("processing complete")
        button2.setText("processing complete...")
        
    except:
        print("failure to launch")
        #text2.set("failure to launch...")

def restart():
    """
    Functionality: Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

folder = [None]
def fileDialog():
    folderPath = QFileDialog.getExistingDirectory(window, "open dir")
    if folderPath:
        folder[0] = folderPath
        button1.setText(folderPath)

    # text2.set("Press to Start")
    # if getattr(sys, 'frozen', False): # check if running bundle or normal python
    #     application_path = os.path.dirname(sys.argv[0])
    # else: # normal python
    #     application_path = os.path.dirname(os.path.abspath(__file__))
    # folderPath = filedialog.askdirectory(initialdir =  str(application_path), title = "Select Folder")
    # if folderPath:
    #     text.set(folderPath)
    #     folder[0] = folderPath

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Landsat 8 Image Processing")

label1 = QLabel()
label1.setText("Created by Derek Pickell\nClick to search for folder that contains \
proper images.\n Required: Landsat 8 Bands 4, 3, 2, 8 and metadata.txt. \nOutput is a pansharpened RGB \
true color image \nstored in the original folder.")
label1.setAlignment(Qt.AlignCenter)


button1 = QPushButton("Search for Landsat image folder")
button1.clicked.connect(lambda: fileDialog())

button2 = QPushButton("Press to Start")
button2.clicked.connect(lambda: run(folder))

label2 = QLabel()
label2.setText("Depending on datasize, processing can take several minutes \nwith the spinning wheel of death.")
label2.setAlignment(Qt.AlignCenter)

button3 = QPushButton("Reset")
button3.clicked.connect(lambda: restart())

label3 = QLabel()
label3.setText("V.6.2020. Distribute with credit to www.derekpickell.com")
label3.setAlignment(Qt.AlignCenter)

vbox = QVBoxLayout()
vbox.addWidget(label1)
vbox.addStretch()
vbox.addWidget(button1)
vbox.addStretch()
vbox.addWidget(button2)
vbox.addStretch()
vbox.addWidget(label2)
vbox.addStretch()
vbox.addWidget(button3)
vbox.addStretch()
vbox.addWidget(label3)

# l1.setOpenExternalLinks(True)
# l4.linkActivated.connect(clicked)
# l2.linkHovered.connect(hovered)
# l1.setTextInteractionFlags(Qt.TextSelectableByMouse)
window.setLayout(vbox)
   
window.show()
sys.exit(app.exec_())

# window = tk.Tk()
# window.title("Landsat Image Processing")
# window.geometry("500x500")
# #window.resizable(0, 0)
# greeting = tk.Label(text="Created by Derek Pickell\nClick to search for folder that contains \
# proper images.\n Required: Bands 4, 3, 2, 8 and metadata.txt. \nOutput is a pansharpened RGB \
# true color image \nstored in the original folder.")
# greeting.grid(column = 0, row = 1, padx = 5, pady = 5)

# text = tk.StringVar()
# button1 = tk.Button(textvar = text, command =  lambda: fileDialog(), bg = "blue")
# text.set("Search for Landsat image folder")
# button1.grid(column = 0, row = 2, padx = 20, pady = 20)

# text2 = tk.StringVar()
# button2 = tk.Button(textvar = text2, command = lambda: run(folder))
# text2.set("Press to start")
# button2.grid(column = 0, row = 3, padx = 20, pady = 20)

# text3 = tk.StringVar()
# label = tk.Label(textvar =text3)
# text3.set("Depending on datasize, processing can take several minutes \nwith spinning wheel of death. \nGo do something else in meantime.")
# label.grid(column = 0, row = 4, padx = 20, pady = 20)

# button3 = tk.Button(text = "Restart", command = lambda: restart())
# button3.grid(column = 0, row = 5, padx = 20, pady = 20)

# label = tk.Label(text = "Created 2020. Distribute as you please, with credit to www.derekpickell.com")
# label.grid(column = 0, row = 6, pady = 20)

# window.grid_columnconfigure(0,weight=1)
# window.grid_rowconfigure(1,weight=1)
# window.grid_rowconfigure(2,weight=1)
# window.grid_rowconfigure(3,weight=1)
# window.grid_rowconfigure(4,weight=1)
# window.grid_rowconfigure(5,weight=1)
# window.grid_rowconfigure(6,weight=1)

# window.mainloop() 
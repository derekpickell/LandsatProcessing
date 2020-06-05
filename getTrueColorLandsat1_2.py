# RUN PARAMETERS: Python 3.6.8 python.org (no brew/conda, etc)
# APP FREEZE: pyinstaller 3.6
import cv2 as cv #opencv-contrib-python 3.4.9.33
import sys, os 
from PyQt5.Qt import * #PyQt5 5.13.0
from landsatCore import getTrueColorLandsat, colorCorrect, convertToFinal

# GUI: LANDSAT 8 TRUE COLOR IMAGE CONVERTER
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
        button2.setText("failure to launch...")

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

window.setLayout(vbox)
window.show()
sys.exit(app.exec_())

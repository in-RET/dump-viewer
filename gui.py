import os
import uuid
import sys

from oemof import solph
from plot import plot

try:
    from PySide6.QtWidgets import QPushButton, QWidget, QApplication, QVBoxLayout, QFileDialog, QProgressBar, QTabWidget, QHBoxLayout, QLabel
    from PySide6.QtGui import QPixmap
    from PySide6.QtCore import QUrl, QFileInfo, QObject
    from PySide6.QtWebEngineWidgets import QWebEngineView
    PYQT = True
except ModuleNotFoundError:
    PYQT = False
    print("Please install PySide6 to start the application with a graphical user interface.")


if PYQT:
    class MainWindow(QWidget):
        filepath = None

        def __init__(self, parent: QApplication):
            super().__init__()
            self.button_plot = None
            self.progressbar = None
            self.parent = parent
            self.initUI()

        def initUI(self):
            hbox_input = QHBoxLayout()
            hbox_output = QHBoxLayout()
            vbox = QVBoxLayout()

            ### Input GUI
            button_load_data = QPushButton("Select dumpfile", self)
            button_load_data.clicked.connect(self.GetFolderName)
            button_load_data.setObjectName("load")
            hbox_input.addWidget(button_load_data)

            hbox_input.addStretch()

            self.button_plot = QPushButton("Show diagrams", self)
            self.button_plot.clicked.connect(self.ShowDiagrams)
            self.button_plot.setObjectName("go")
            self.button_plot.setEnabled(False)
            hbox_input.addWidget(self.button_plot)

            qbtn = QPushButton('Quit', self)
            qbtn.clicked.connect(QApplication.instance().quit)

            hbox_input.addWidget(qbtn)

            ### Output GUI
            self.tabs = QTabWidget()

            hbox_output.addWidget(self.tabs)

            vbox.addLayout(hbox_input)
            vbox.addLayout(hbox_output)

            self.setLayout(vbox)

            self.setGeometry(300, 300, 750, 550)
            self.setWindowTitle('Tool: Dumpfile viewer')
            self.show()

        def ShowDiagrams(self):
            es = solph.EnergySystem()
            es.restore(dpath=os.path.dirname(self.filepath), filename=os.path.basename(self.filepath))

            figures = plot(es)

            imagepath = os.path.join(os.getcwd(), "images")

            if not os.path.exists(imagepath):
                os.mkdir(imagepath)

            for fig in figures:
                name = str(uuid.uuid4().hex)
                fig.write_image("images/" + name + ".png")
                self.AddPlotTab(name)

        def GetFolderName(self):
            filedialog = QFileDialog
            self.filepath = filedialog.getOpenFileName(self, 'Open File', filter=str("Dumpfiles (*.dump)"))[0]

            if os.path.exists(self.filepath) and os.path.isfile(self.filepath):
                self.button_plot.setEnabled(True)

        def AddPlotTab(self, name):
            file = "images/" + name + ".png"

            filename = os.path.basename(file)
            if str.find(filename, ".png") > 0:
                #print("png")
                tab = QWidget()

                image = QPixmap(file)
                label = QLabel()
                label.setPixmap(image)

                vbox = QVBoxLayout()
                vbox.addWidget(label)
                tab.setLayout(vbox)

                self.tabs.addTab(tab, filename)
            else:
                print("Nicht Identifiziert")
     
        def on_downloadRequested(self, download: QObject):
            old_path = download.url().path()  # download.path()
            suffix = "png"
            path, _ = QFileDialog.getSaveFileName(
                self, "Save File", old_path, "*." + suffix
            )
            if path:
                download.setDownloadDirectory(os.path.dirname(path))
                download.setDownloadFileName(os.path.basename(path))
                download.accept()


    def StartGui():
        app = QApplication(sys.argv)
        window = MainWindow(parent=app)
        window.show()

        sys.exit(app.exec())
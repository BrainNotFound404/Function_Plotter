import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSizePolicy, QLineEdit, QLabel, QMessageBox
from matplotlib.pyplot import show
import pyqtgraph as pg
import numpy as np
import functie

tolerance = 1e-8


class MyPlotWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        xl, xr = self.viewRange()[0]
        yd, yu = self.viewRange()[1]
        x = np.linspace(2 * xl - xr, 2 * xr - xl, 800)
        y1 = np.zeros_like(x)
        for i, val in enumerate(x):
            y1[i] = functie.vale(functie.operands[-1], val)
            if y1[i] * y1[i - 1] < -(yu - yd) ** 2:
                y1[i] = None
                y1[i - 1] = None

        self.clear()

        self.addLine(x=0, pen=pg.mkPen('k'))  # Oy
        self.addLine(y=0, pen=pg.mkPen('k'))  # Ox
        self.plot(x, y1, pen='r')

        if self.showing_derivate:
            y2 = np.zeros_like(x)
            for i, val in enumerate(x):
                y2[i] = (functie.vale(functie.operands[-1], val + tolerance) - functie.vale(functie.operands[-1], val)) / tolerance
                if y2[i] * y2[i - 1] < -(yu - yd) ** 2:
                    y2[i] = None
                    y2[i - 1] = None
            self.plot(x, y1, pen='r')
            self.plot(x, y2, pen='b')
        else:
            self.plot(x, y1, pen='r')


    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Grapher")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.plot_widget = MyPlotWidget()
        self.button_widget, self.text_box = self.createButtonsWidget()
        self.plot_widget.setBackground(background = None)
        self.plot_widget.showing_derivate = False
        layout.addWidget(self.button_widget)
        layout.addWidget(self.plot_widget)


    #Butoanele pt graf
    def createButtonsWidget(self):
        # Creez un widget pentru interfata butoanelor
        buttons_widget = QWidget()

        buttons_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        buttons_widget.setFixedHeight(80)  # Seteaza o inaltime fixa pentru butoane

        # Create layout for the buttons widget
        buttons_layout = QVBoxLayout(buttons_widget)

        # Prima linie de butoane
        first_line_layout = QHBoxLayout()
        label1 = QLabel("Introduceti functia: ")
        text_box = QLineEdit()
        text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  
        button_read_function = QPushButton('Citeste functia')
        button_read_function.setFixedSize(120, 30)    
        button_draw_function = QPushButton('Reseteaza originea')
        button_draw_function.setFixedSize(150, 30)
        button_center_camera = QPushButton('Centreaza Camera')
        button_center_camera.setFixedSize(150, 30)

        #Functiile butoanelor de pe prima linie
        button_draw_function.clicked.connect(self.plot_function)
        button_center_camera.clicked.connect(self.center_camera)
        button_read_function.clicked.connect(self.receive_input)

        first_line_layout.addWidget(label1)
        first_line_layout.addWidget(text_box)
        first_line_layout.addWidget(button_read_function)
        first_line_layout.addStretch()
        first_line_layout.addWidget(button_draw_function)
        first_line_layout.addWidget(button_center_camera)
        buttons_layout.addLayout(first_line_layout)
        
        # A doua linie de butoane
        label2 = QLabel("Functia curenta: ")
        self.label3 = QLabel('')
        second_line_layout = QHBoxLayout()
        self.button_show_derivate = QPushButton('Afiseaza derivata')
        self.button_show_derivate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 
        #Functia butonului de pe a doua linie
        self.button_show_derivate.clicked.connect(self.on_off_derivate)

        #Adaug spatiu intre butoane
        second_line_layout.addStretch()
        second_line_layout.addWidget(label2)
        second_line_layout.addWidget(self.label3)
        second_line_layout.addWidget(self.button_show_derivate)
        buttons_layout.addLayout(second_line_layout)

        #Setez raportul "intinderii" butoanelor pentru a creste direct proportional cu maximizarea/minimizarea ecranului 
        buttons_layout.setStretchFactor(first_line_layout, 1)
        buttons_layout.setStretchFactor(second_line_layout, 1)

        return buttons_widget, text_box
    
    def on_off_derivate(self):
        if self.button_show_derivate.text() == 'Afiseaza derivata':
            self.button_show_derivate.setText("Nu mai afisa derivata")
            self.plot_widget.showing_derivate = True
            xl, xr = self.plot_widget.viewRange()[0]
            yd, yu = self.plot_widget.viewRange()[1]
            x = np.linspace(2 * xl - xr, 2 * xr - xl, 800)
            y = np.zeros_like(x)
            for i, val in enumerate(x):
                y[i] = (functie.vale(functie.operands[-1], val + tolerance) - functie.vale(functie.operands[-1], val)) / tolerance
                if y[i] * y[i - 1] < - (yu - yd) ** 2:
                    y[i] = None
                    y[i - 1] = None
            
            self.plot_widget.plot(x, y, pen='b')
        else:
            self.button_show_derivate.setText('Afiseaza derivata')
            self.plot_widget.showing_derivate = False
            xl, xr = self.plot_widget.viewRange()[0]
            yd, yu = self.plot_widget.viewRange()[1]
            x = np.linspace(2 * xl - xr, 2 * xr - xl, 800)
            y = np.zeros_like(x)
            for i, val in enumerate(x):
                y[i] = functie.vale(functie.operands[-1], val)
                if y[i] * y[i - 1] < -(yu - yd) ** 2:
                    y[i] = None
                    y[i - 1] = None

            self.plot_widget.clear()

            self.plot_widget.addLine(x=0, pen=pg.mkPen('k'))  # Oy
            self.plot_widget.addLine(y=0, pen=pg.mkPen('k'))  # Ox

            self.plot_widget.plot(x, y, pen='r')

    def receive_input(self):
        functia = self.text_box.text()
        functie.translate_function(functia)
        self.text_box.clear()
        self.label3.setText(functia)
        self.plot_function()


    def center_camera(self):
        xl, xr = self.plot_widget.viewRange()[0]
        yd, yu = self.plot_widget.viewRange()[1]
        mij = functie.vale(functie.operands[-1], (xr + xl) / 2)

        x = np.linspace(2 * xl - xr, 2 * xr - xl, 800)
        y = np.zeros_like(x)
        new_yu = mij + (yu - yd) / 2
        new_yd = mij - (yu - yd) / 2
        for i, val in enumerate(x):
            y[i] = functie.vale(functie.operands[-1], val)
            if y[i] * y[i - 1] < -(yu - yd) ** 2:
                    y[i] = None
                    y[i - 1] = None

        self.plot_widget.clear()

        self.plot_widget.addLine(x=0, pen=pg.mkPen('k'))  # Oy
        self.plot_widget.addLine(y=0, pen=pg.mkPen('k'))  # Ox

        self.plot_widget.plot(x, y, pen='r')

        self.plot_widget.setYRange(new_yd, new_yu)

    def plot_function(self):
        x = np.linspace(-20, 20, 800)
        y = np.zeros_like(x)
        
        for i, val in enumerate(x):
            y[i] = functie.vale(functie.operands[-1], val)
            if y[i] > 10 or y[i] < -10:
                y[i] = None

        self.plot_widget.showGrid(x = True, y = True, alpha = 0.4)

        self.plot_widget.clear()
        
        self.plot_widget.addLine(x=0, pen=pg.mkPen('k'))  # Oy
        self.plot_widget.addLine(y=0, pen=pg.mkPen('k'))  # Ox

        self.plot_widget.plot(x, y, pen='r')

        self.plot_widget.setXRange(-7, 7)
        self.plot_widget.setYRange(-5, 5)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
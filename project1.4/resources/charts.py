import sys
import os
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import JSPYLib
# Load the UI file
app = QtWidgets.QApplication(sys.argv)
loader = QUiLoader()
mainwindow = loader.load("D:/programming/Python/Exercices/project1.3/mainWindow.ui", None)

mydbfile = JSPYLib.DATABASE()

def barchart(widgetName,X_axes=[],Y_axes=[],color=['blue']):
    # Find the empty QWidget by its object name in Qt Designer
    chart_widget = mainwindow.findChild(QWidget, widgetName)

    # Ensure chartWidget has a proper layout
    if not chart_widget.layout():
        chart_widget.setLayout(QVBoxLayout())  # Set a vertical layout if none exists

    # Create Matplotlib Canvas
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvas(fig)
    chart_widget.layout().addWidget(canvas)  # Embed canvas inside chartWidget

    # Plot Bar Chart
    ax = fig.add_subplot(111)
    ax.bar(X_axes,Y_axes,color)










# Show the main window
mainwindow.show()
sys.exit(app.exec())
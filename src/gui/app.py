import sys
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QLineEdit, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ero-2025")
        self.setMinimumSize(800, 600)

        # Create the label for the text input
        self.area_label = QLabel("Custom area")
        # Create the text input
        self.area_input = QLineEdit()
        self.area_input.setPlaceholderText("Enter area name")

        # Create the buttons
        self.outremont_button = QPushButton("Outremont")
        self.verdun_button = QPushButton("Verdun")
        self.saint_leonard_button = QPushButton("Saint-Léonard")
        self.rdp_button = QPushButton(
            "Rivière-des-prairies-pointe-aux-trembles")
        self.plateau_button = QPushButton("Le Plateau-Mont-Royal")

        self.start_button = QPushButton("Start")
        self.quit_button = QPushButton("Quit")

        # Connect button signals to their respective slots
        self.outremont_button.clicked.connect(
            lambda: self.set_area("Outremont, Montreal, QC, Canada"))
        self.verdun_button.clicked.connect(
            lambda: self.set_area("Verdun, Montreal, QC, Canada"))
        self.saint_leonard_button.clicked.connect(
            lambda: self.set_area("Saint-Léonard, Montreal, QC, Canada"))
        self.rdp_button.clicked.connect(lambda: self.set_area(
            "Rivière-des-prairies-pointe-aux-trembles, Montreal, QC, Canada"))
        self.plateau_button.clicked.connect(lambda: self.set_area(
            "Le Plateau-Mont-Royal, Montreal, QC, Canada"))

        self.start_button.clicked.connect(self.start)
        self.quit_button.clicked.connect(self.quit)

        # Create the layout for the side menu
        side_menu_layout = QVBoxLayout()
        side_menu_layout.addWidget(self.area_label)
        side_menu_layout.addWidget(self.area_input)
        side_menu_layout.addWidget(self.outremont_button)
        side_menu_layout.addWidget(self.verdun_button)
        side_menu_layout.addWidget(self.saint_leonard_button)
        side_menu_layout.addWidget(self.rdp_button)
        side_menu_layout.addWidget(self.plateau_button)
        side_menu_layout.addStretch()
        side_menu_layout.addWidget(self.start_button)
        side_menu_layout.addWidget(self.quit_button)

        # Create the left side menu widget
        side_menu_widget = QWidget()
        side_menu_widget.setMaximumWidth(250)
        side_menu_widget.setStyleSheet("background-color: #444444;")

        # Set the layout for the side menu widget
        side_menu_widget.setLayout(side_menu_layout)

        # Create the network display area widget
        self.network_display = QWidget()
        self.network_display.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create the main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(side_menu_widget)
        main_layout.addWidget(self.network_display)

        # Set the main layout for the main window
        self.setLayout(main_layout)

        # Store the last area name for subsequent clicks on the "Start" button
        self.last_area = ""

    def quit(self):
        # Close the application when the Quit button is clicked
        QApplication.quit()

    def start(self):
        # Retrieve the area name from the text input
        area = self.area_input.text()

        # Check if the area has changed since the last click on the "Start" button
        if area != self.last_area:
            # Retrieve the street layout using osmnx
            network = ox.graph_from_place(area, network_type='drive')

            # Store the current area as the last area
            self.last_area = area

            # Clear the existing layout of the network display area
            layout = self.network_display.layout()
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)

            # Create a new Figure and Canvas
            fig = plt.figure()
            canvas = FigureCanvas(fig)

            # Plot the network on the Figure
            ax = fig.add_subplot(111)
            ox.plot_graph(network, node_color='black', ax=ax, show=False)

            # Set the layout for the network display area
            layout = QVBoxLayout(self.network_display)
            layout.addWidget(canvas)
            self.network_display.setLayout(layout)

    def set_area(self, area):
        self.area_input.setText(area)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

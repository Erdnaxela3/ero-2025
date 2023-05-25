import sys
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, \
        QWidget, QHBoxLayout, QLineEdit, QLabel, QFrame, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

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

        self.recon_button = QPushButton("Drone Recon")
        self.plow_button = QPushButton("Plow Area")
        self.quit_button = QPushButton("Quit")

        # Connect button to set the area input
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

        self.recon_button.clicked.connect(self.start)
        self.plow_button.clicked.connect(self.start)
        self.quit_button.clicked.connect(self.quit)

        # Create the layout for the side menu
        side_menu_layout = QVBoxLayout()
        side_menu_layout.addWidget(self.area_label)
        side_menu_layout.addWidget(self.area_input)

        # Add separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        side_menu_layout.addWidget(line)

        side_menu_layout.addWidget(self.outremont_button)
        side_menu_layout.addWidget(self.verdun_button)
        side_menu_layout.addWidget(self.saint_leonard_button)
        side_menu_layout.addWidget(self.rdp_button)
        side_menu_layout.addWidget(self.plateau_button)
        side_menu_layout.addStretch()
        side_menu_layout.addWidget(self.recon_button)
        side_menu_layout.addWidget(self.plow_button)
        side_menu_layout.addWidget(self.quit_button)

        # Create the left side menu widget
        side_menu_widget = QWidget()
        side_menu_widget.setMaximumWidth(250)
        side_menu_widget.setStyleSheet("background-color: #444444;")

        # Set the layout for the side menu widget
        side_menu_widget.setLayout(side_menu_layout)

        # Create the network display area widget
        self.figure = plt.figure()
        self.network_display = FigureCanvas(self.figure)

        # Create the text area widget
        self.text_area = QTextEdit()
        self.text_area.setMaximumWidth(350)
        self.text_area.setReadOnly(True)

        # Create the main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(side_menu_widget)
        main_layout.addWidget(self.network_display)
        main_layout.addWidget(self.text_area)

        # Set the main layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Store the last area name for subsequent clicks on the "Start" button
        self.last_area = ""

    def quit(self):
        # Close the application when the Quit button is clicked
        QApplication.quit()

    def start(self):
        input_area = self.area_input.text()

        if self.last_area == input_area:
            return

        self.last_area = input_area

        try:
            network = ox.graph_from_place(input_area, network_type='drive')
            stats = ox.stats.basic_stats(network)
            stats_str = ""
            for key, value in stats.items():
                stats_str += f"{key}: {value}\n"
        except ox.errors.PlaceNotFound:
            self.area_input.clear()
            self.area_input.setPlaceholderText(
                "Invalid area: Please enter a valid area name")
            return

        self.text_area.setPlainText(stats_str)
        self.update_plot_data(network)

    def update_plot_data(self, network):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ox.plot_graph(network, ax=ax, node_color='black',
                      node_size=3, show=False)

        self.network_display.draw()

    def clear_plot_data(self):
        self.figure.clear()
        self.network_display.draw()
        self.text_area.clear()

    def set_area(self, area):
        self.area_input.setText(area)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

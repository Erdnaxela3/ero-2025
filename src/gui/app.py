import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import osmnx as ox
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, \
    QWidget, QHBoxLayout, QLineEdit, QLabel, QFrame, QTextEdit
from PyQt5.QtGui import QIntValidator
import sys

from colorizing import edge_index_path2color, edge_path2edge_index
from cost import ClassicDroneCost, VehicleT1Cost, VehicleT2Cost
from report import DroneReport, PlowReport
from graph_manip import eulerian_path
import pickle

matplotlib.use('Agg')  # to avoid pop ups

OSMNX_NETWORK_TYPE = 'drive'
OSMNX_NODE_SIZE = 1
OSMNX_NODE_COLOR = 'black'
QT_MINSIZE_WIDTH = 800
QT_MINSIZE_HEIGHT = 600
TEXT_AREA_WIDTH = 350
SIDE_MENU_WIDTH = 250
BIGGER_BUTTON_SCALE_FACTOR = 2
ANIMATION_DURATION = 5
SECOND_IN_MS = 1000


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.animation_on = False
        self.network = None
        self.edge_colors = None

        self.setWindowTitle("ero-2025")
        self.setMinimumSize(QT_MINSIZE_WIDTH, QT_MINSIZE_HEIGHT)

        # Create the buttons
        self.drone_recon_label = QLabel("Load Montréal")
        self.montreal_button = QPushButton("Montréal")
        BIGGER_BUTTON_HEIGHT = self.montreal_button.sizeHint().height() * \
            BIGGER_BUTTON_SCALE_FACTOR

        self.plow_area_label = QLabel("Load Subject Plow Area")
        self.outremont_button = QPushButton("Outremont")
        self.verdun_button = QPushButton("Verdun")
        self.saint_leonard_button = QPushButton("Saint-Léonard")
        self.rdp_button = QPushButton(
            "Rivière-des-prairies-pointe-aux-trembles")
        self.plateau_button = QPushButton("Le Plateau-Mont-Royal")

        self.area_label = QLabel("Load Custom area")
        self.area_input = QLineEdit()
        self.area_input.setPlaceholderText("Enter area name")
        self.load_custom_button = QPushButton("Load Custom")

        self.number_of_vehicle_label = QLabel("Vehicle number for plowing")
        self.number_of_vehicle_input = QLineEdit()
        self.number_of_vehicle_input.setValidator(QIntValidator())
        self.number_of_vehicle_input.setPlaceholderText("Enter vehicle number")
        self.number_of_vehicle_input.setText("1")

        self.vehicle_cost = VehicleT1Cost()
        self.vehicle_t1_button = QPushButton("Vehicle T1")
        self.vehicle_t2_button = QPushButton("Vehicle T2")

        self.recon_button = QPushButton("Drone Recon")
        self.recon_button.setFixedHeight(BIGGER_BUTTON_HEIGHT)
        self.plow_button = QPushButton("Plow Area")
        self.plow_button.setFixedHeight(BIGGER_BUTTON_HEIGHT)
        self.quit_button = QPushButton("Quit")
        self.quit_button.setFixedHeight(BIGGER_BUTTON_HEIGHT)

        # Connect button to set the area input
        self.montreal_button.clicked.connect(
            lambda: self.load_area("Montreal, QC, Canada"))
        self.outremont_button.clicked.connect(
            lambda: self.load_area("Outremont, Montreal, QC, Canada"))
        self.verdun_button.clicked.connect(
            lambda: self.load_area("Verdun, Montreal, QC, Canada"))
        self.saint_leonard_button.clicked.connect(
            lambda: self.load_area("Saint-Léonard, Montreal, QC, Canada"))
        self.rdp_button.clicked.connect(
            lambda: self.load_area(
                "Rivière-des-prairies-pointe-aux-trembles, Montreal, QC, Canada"))
        self.plateau_button.clicked.connect(
            lambda: self.load_area("Le Plateau-Mont-Royal, Montreal, QC, Canada"))

        self.load_custom_button.clicked.connect(self.load_area)
        self.vehicle_t1_button.clicked.connect(self.setT1)
        self.vehicle_t2_button.clicked.connect(self.setT2)
        self.recon_button.clicked.connect(self.drone_recon)
        self.plow_button.clicked.connect(self.plow_area)
        self.quit_button.clicked.connect(self.quit)

        side_menu_layout = QVBoxLayout()

        side_menu_layout.addWidget(self.drone_recon_label)
        side_menu_layout.addWidget(self.montreal_button)

        # Add separator line
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        side_menu_layout.addWidget(line1)

        side_menu_layout.addWidget(self.plow_area_label)
        side_menu_layout.addWidget(self.outremont_button)
        side_menu_layout.addWidget(self.verdun_button)
        side_menu_layout.addWidget(self.saint_leonard_button)
        side_menu_layout.addWidget(self.rdp_button)
        side_menu_layout.addWidget(self.plateau_button)

        # Add separator line
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        side_menu_layout.addWidget(line2)

        side_menu_layout.addWidget(self.area_label)
        side_menu_layout.addWidget(self.area_input)
        side_menu_layout.addWidget(self.load_custom_button)

        # Add separator line
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setFrameShadow(QFrame.Sunken)
        side_menu_layout.addWidget(line3)

        side_menu_layout.addWidget(self.number_of_vehicle_label)
        side_menu_layout.addWidget(self.number_of_vehicle_input)
        side_menu_layout.addWidget(self.number_of_vehicle_input)

        number_of_vehicle_layout = QHBoxLayout()
        number_of_vehicle_layout.addWidget(self.vehicle_t1_button)
        number_of_vehicle_layout.addWidget(self.vehicle_t2_button)
        side_menu_layout.addLayout(number_of_vehicle_layout)

        side_menu_layout.addStretch()

        side_menu_layout.addWidget(self.recon_button)
        side_menu_layout.addWidget(self.plow_button)

        side_menu_layout.addWidget(self.quit_button)

        # Create the left side menu widget
        side_menu_widget = QWidget()
        side_menu_widget.setMaximumWidth(SIDE_MENU_WIDTH)
        side_menu_widget.setStyleSheet("background-color: #444444;")

        # Set the layout for the side menu widget
        side_menu_widget.setLayout(side_menu_layout)

        # Create the network display area widget
        self.figure = plt.figure()
        self.network_display = FigureCanvas(self.figure)

        # Create the text area widget
        self.text_area = QTextEdit()
        self.text_area.setMaximumWidth(TEXT_AREA_WIDTH)
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

        # Store the last area name for subsequent clicks on the "Load Custom" button
        self.last_area = ""

    def quit(self):
        # Close the application when the Quit button is clicked
        QApplication.quit()

    def load_area(self, area_arg=None):
        if self.animation_on:
            self.text_area.setPlainText(
                "Animation in process can't load another graph")
            return

        if area_arg:
            self.set_area(area_arg)

        input_area = self.area_input.text()

        if self.last_area == input_area:
            return

        self.last_area = input_area

        try:
            network = ox.graph_from_place(
                input_area, network_type=OSMNX_NETWORK_TYPE)
            try:
                self.network = network.to_undirected()
            except Exception:
                self.network = network

            self.stats = ox.stats.basic_stats(self.network)
            stats_str = ""
            for key, value in self.stats.items():
                stats_str += f"{key}: {value}\n"
        except Exception:
            self.area_input.clear()
            self.area_input.setPlaceholderText(
                "Invalid area: Please enter a valid area name")
            return

        self.text_area.setPlainText(stats_str)
        self.update_plot_data(self.network)

    def update_plot_data(self, network):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ox.plot_graph(network, ax=ax, node_color=OSMNX_NODE_COLOR,
                      node_size=OSMNX_NODE_SIZE, show=False)
        self.network_display.draw()

    def drone_recon(self):
        if not self.network:
            return self.text_area.setPlainText("PLEASE LOAD A GRAPH")

        costs = ClassicDroneCost()
        report = DroneReport(costs)

        self.animation_on = True

        self.eulerized, path = eulerian_path(self.network)
        pickle.dump(path, open(
            f"{self.area_input.text().split()[0]}-drone.p", "wb"))
        pickle.dump(path, open(
            f"{self.area_input.text().split()[0]}-eulerized.p", "wb"))

        report.create_report(self.eulerized, path)
        report.save("drone_report.json")
        self.animate_path(path)

        stats = {
            "street_length_total": "{0:.2f}km".format(self.stats["street_length_total"] / 1000),
            "Total distance traveled": "{0:.2f}km".format(report['total_distance']),
            "Fixed droned cost": "{0:.2f}km".format(report['cumul_fix_cost']),
            "Cumul km distance cost": "{0:.2f}$".format(report['cumul_flight_cost']),
            "Total flight cost": "{0:.2f}$".format(report.report['total_cost'])
        }

        stats_str = ""
        for key, value in stats.items():
            stats_str += f"{key}: {value}\n"
        self.text_area.setPlainText(stats_str)

    def plow_area(self):
        if not self.network:
            return self.text_area.setPlainText("PLEASE LOAD A GRAPH")

        n = max(1, int(self.number_of_vehicle_input.text()))
        report = PlowReport(self.vehicle_cost)

        self.eulerized, path = eulerian_path(self.network)
        pickle.dump(path, open(
            f"{self.area_input.text().split(',')[0]}-drone.p", "wb"))
        pickle.dump(path, open(
            f"{self.area_input.text().split(',')[0]}-eulerized.p", "wb"))

        report.create_report(self.eulerized, path, n)
        report.save("plow_report.json")
        self.animate_path(path, n)

        stats = {
            "Number of vehicles": f"{n}",
            "street_length_total": "{0:.2f}km".format(self.stats["street_length_total"] / 1000),
            "Total distance traveled": "{0:.2f}km".format(report['total_distance']),
            "Vehicle cumul hours": "{0:.2f}h".format(report['cumul_hours']),
            "Vehicle cumul non-overtime hours": "{0:.2f}h".format(report['cumul_not_overtime_h']),
            "Vehicle cumul overtime hours": "{0:.2f}h".format(report['cumul_overtime_h']),
            "Vehicle fixed cumul cost": "{0:.2f}$".format(report['cumul_fixed_cost']),
            "Vehicle km cumul cost": "{0:.2f}$".format(report['cumul_km_cost']),
            "Vehicle cumul non-overtime cost": "{0:.2f}$".format(report['cumul_not_overtime_cost']),
            "Vehicle cumul overtime cost": "{0:.2f}$".format(report['cumul_overtime_cost']),
            "Operation Total Cost": "{0:.2f}$".format(report['total_cost']),
            "Operation Duration": "{0:.2f}h".format(report['operation_duration'])
        }
        stats_str = ""
        for key, value in stats.items():
            stats_str += f"{key}: {value}\n"
        self.text_area.setPlainText(stats_str)

    def set_area(self, area):
        self.area_input.setText(area)

    def setT1(self):
        self.vehicle_cost = VehicleT1Cost()

    def setT2(self):
        self.vehicle_cost = VehicleT2Cost()

    def animate_path(self, path, n=1):
        n_edges = len(path)
        self.edge_colors = np.zeros((len(self.eulerized.edges), 3))
        interval_ms = int(ANIMATION_DURATION * SECOND_IN_MS / n_edges / n)
        n_frames = int(n_edges / n)
        path = edge_path2edge_index(self.eulerized, path)

        def update(frame):
            self.edge_colors = edge_index_path2color(
                path, self.edge_colors, frame, n)
            ax = self.figure.add_subplot(111)
            ox.plot_graph(self.eulerized, ax=ax, edge_color=self.edge_colors,
                          node_color=OSMNX_NODE_COLOR,
                          node_size=OSMNX_NODE_SIZE)
            self.network_display.draw()

            # Stop the animation after all frames are captured
            if frame == n_edges - 1:
                anim.event_source.stop()

        # Create the animation
        anim = FuncAnimation(
            self.figure, update, frames=n_frames+1, interval=interval_ms, repeat=False)

        # Start the animation
        anim._start()
        plt.show()

        self.animation_on = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

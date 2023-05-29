import sys
import osmnx as ox
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, \
    QWidget, QHBoxLayout, QLineEdit, QLabel, QFrame, QTextEdit
from PyQt5.QtGui import QIntValidator
import numpy as np

matplotlib.use('Agg')  # to avoid pop ups

OSMNX_NETWORK_TYPE = 'drive'
OSMNX_NODE_SIZE = 1
OSMNX_NODE_COLOR = 'black'
QT_MINSIZE_WIDTH = 800
QT_MINSIZE_HEIGHT = 600
BIGGER_BUTTON_SCALE_FACTOR = 2
ANIMATION_DURATION = 5
EDGE_VISIT_COLOR = np.array([0.11, 0.5, 0.13])
SECOND_IN_MS = 1000


def node_path2color(G, node_path, edge_dict, edge_colors=None, already_done=0, n=1):
    """
    Args
    G : networkx.graph
    node_path: list
    Returns list of int : edge colors
    """
    u = node_path[already_done]
    v = node_path[already_done+1]
    edge_index = edge_dict[(u, v)]
    edge_colors[edge_index] = EDGE_VISIT_COLOR  # Set edge color to red

    return edge_colors


def dict_edge_index(G):
    edge_l = list(G.edges())
    res = dict()
    for u, v in G.edges():
        edge_index = edge_l.index((u, v))
        res[(u, v)] = edge_index
        res[(v, u)] = edge_index
    return res


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

            stats = ox.stats.basic_stats(self.network)
            stats_str = ""
            for key, value in stats.items():
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
        self.animation_on = True

        path = nx.approximation.traveling_salesman_problem(self.network)
        print(path)
        self.animate_path(path)

        stats = {
            "Distance parcourue": "TODO",
            "Cout": "TODO$"
        }
        stats_str = ""
        for key, value in stats.items():
            stats_str += f"{key}: {value}\n"
        self.text_area.setPlainText(stats_str)

    def plow_area(self):
        n = int(self.number_of_vehicle_input.text())

        path = nx.approximation.traveling_salesman_problem(self.network)
        print(path)
        self.animate_path(path, n)

        stats = {
            "Distance parcourue": "TODO",
            "Cout fixe / vehicule": "TODO$",
            "Cout horaire / vehicule": "TODO$",
            "Cout horaire supp / vehicule": "TODO$",
            "Vitesse du vehicule (km/h)": "TODO",
            "Nombre de vehicule": "TODO",
            "Cout de l'operation": "TODO$"
        }
        stats_str = ""
        for key, value in stats.items():
            stats_str += f"{key}: {value}\n"
        self.text_area.setPlainText(stats_str)

    def set_area(self, area):
        self.area_input.setText(area)

    def animate_path(self, path, n=1):
        n_edges = len(path) - 1
        self.edge_colors = np.zeros((len(self.network.edges), 3))
        interval_ms = int(ANIMATION_DURATION * SECOND_IN_MS / n_edges / n)
        n_frames = int(n_edges / n)
        self.edge_dict = dict_edge_index(self.network)

        def update(frame):
            self.edge_colors = node_path2color(
                self.network, path, self.edge_dict, self.edge_colors, frame, n)
            ax = self.figure.add_subplot(111)
            ox.plot_graph(self.network, ax=ax, edge_color=self.edge_colors,
                          node_color=OSMNX_NODE_COLOR,
                          node_size=OSMNX_NODE_SIZE, show=False)
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

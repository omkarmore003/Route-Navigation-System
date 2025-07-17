import sys
import os
import openrouteservice
import pyttsx3
import folium
import speech_recognition as sr
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Replace with your actual OpenRouteService API key
API_KEY = "5b3ce3597851110001cf62488077d64482524ae6a9818beaaba7bcd5"

# ------------------------- Helper Functions -------------------------

def geocode_address(address):
    client = openrouteservice.Client(key=API_KEY)
    try:
        geocode = client.pelias_search(address)
        coords = geocode['features'][0]['geometry']['coordinates']
        return coords  # [lon, lat]
    except:
        return None


def create_route_map(start_coords, end_coords, html_path="route_map.html"):
    client = openrouteservice.Client(key=API_KEY)
    route = client.directions(
        coordinates=[start_coords, end_coords],
        profile='foot-walking',
        format='geojson',
        preference='shortest'
    )

    points = [(pt[1], pt[0]) for pt in route['features'][0]['geometry']['coordinates']]
    map_center = [start_coords[1], start_coords[0]]
    m = folium.Map(location=map_center, zoom_start=15)
    folium.Marker(location=map_center, tooltip="Start").add_to(m)
    folium.Marker(location=[end_coords[1], end_coords[0]], tooltip="End").add_to(m)
    folium.PolyLine(points, color="blue", weight=5, opacity=0.8).add_to(m)
    m.save(html_path)
    return html_path, route


def speak_instructions(route):
    steps = route['features'][0]['properties']['segments'][0]['steps']
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    for step in steps:
        instruction = step['instruction']
        print("Speaking:", instruction)
        engine.say(instruction)
        engine.runAndWait()


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print("Recognized:", text)
            return text
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Speech not understood.")
        except sr.RequestError:
            print("Could not request results from Speech Recognition service.")
        return None

# ------------------------- PyQt5 GUI -------------------------

class RouteNavigationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Vision Route Navigation")
        self.setGeometry(100, 100, 900, 700)

        # Layout
        layout = QVBoxLayout()

        # Start input
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Enter start location")
        layout.addWidget(QLabel("Start Location:"))
        layout.addWidget(self.start_input)

        self.start_voice_button = QPushButton("🎤 Speak Start Location")
        self.start_voice_button.clicked.connect(self.voice_input_start)
        layout.addWidget(self.start_voice_button)

        # End input
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("Enter destination")
        layout.addWidget(QLabel("End Location:"))
        layout.addWidget(self.end_input)

        self.end_voice_button = QPushButton("🎤 Speak End Location")
        self.end_voice_button.clicked.connect(self.voice_input_end)
        layout.addWidget(self.end_voice_button)

        # Route Button
        self.route_button = QPushButton("Get Route")
        self.route_button.clicked.connect(self.calculate_route)
        layout.addWidget(self.route_button)

        # Map Display
        self.map_view = QWebEngineView()
        self.map_view.setFixedHeight(400)
        layout.addWidget(self.map_view)

        # Main Widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def voice_input_start(self):
        text = recognize_speech()
        if text:
            self.start_input.setText(text)

    def voice_input_end(self):
        text = recognize_speech()
        if text:
            self.end_input.setText(text)

    def calculate_route(self):
        start = self.start_input.text()
        end = self.end_input.text()

        start_coords = geocode_address(start)
        end_coords = geocode_address(end)

        if not start_coords or not end_coords:
            print("Could not geocode one of the addresses.")
            return

        html_path, route_data = create_route_map(start_coords, end_coords)
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(html_path)))

        speak_instructions(route_data)


# ------------------------- Main App Runner -------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RouteNavigationWindow()
    window.show()
    sys.exit(app.exec_())

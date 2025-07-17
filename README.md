# 🗺️ Smart Vision Route Navigation with Voice and Map 🧭

This is a **desktop navigation assistant** for visually impaired users, built using **PyQt5**, **OpenRouteService**, **speech recognition**, **text-to-speech**, and **interactive map generation** via **Folium**.

Users can enter or speak both their **start** and **destination** addresses. The app then:
- Calculates the **walking route**
- Displays the route using an interactive **HTML map**
- Reads out **step-by-step directions aloud**

---

## 🚀 Features

- 🎤 **Voice input** for start and destination
- 🧭 **Walking directions** using OpenRouteService
- 🗺️ **Interactive map** with live route (HTML, Leaflet, Folium)
- 🔊 **Text-to-Speech** navigation guidance (pyttsx3)
- 🖥️ Desktop-friendly **PyQt5 GUI**
- 📍 Smart geocoding with address search

---

## 📦 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

### Contents of `requirements.txt`

```txt
PyQt5>=5.15.0
PyQtWebEngine>=5.15.0
folium>=0.14.0
openrouteservice>=2.3.0
pyttsx3>=2.90
SpeechRecognition>=3.8.1
```

---

## 🔑 Setup Instructions

1. **Get a free OpenRouteService API key**
   - Sign up at https://openrouteservice.org/dev/#/signup
   - Replace the API key in your code:

     ```python
     API_KEY = "your-api-key-here"
     ```

2. **Run the Application**

```bash
python route.py
```

---

## 🎯 How It Works

### 📍 Address to Coordinates
- Converts your typed or spoken addresses into GPS coordinates using OpenRouteService geocoding.

### 🗺️ Route and Map
- Calculates a walking route and creates an interactive map using **Folium**
- The map is saved as `route_map.html` and loaded inside the app via `QWebEngineView`

### 🔊 Voice Instructions
- Uses `pyttsx3` to speak each direction step aloud

---

## 📁 Project Structure

```
SmartVisionNavigation/
├── route.py             # Main application script
├── route_map.html       # Auto-generated map (Folium)
├── requirements.txt     # Python libraries required
└── README.md            # This file
```

---

## 🖼️ Demo Screenshot (Optional)

> *(Replace this with a real image if available)*

![Map Demo](route_map.png)

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## 👨‍💻 Author

**Omkar More**  
GitHub: [@omkarmore003](https://github.com/omkarmore003)

---

## 💡 Future Enhancements

- ✅ Real-time GPS tracking
- ✅ Turn-by-turn notification with vibration support
- ⏳ Offline speech recognition
- 🌐 Multi-language support

---

## 🤝 Contribute

Have suggestions or want to contribute? Pull requests and feedback are always welcome!

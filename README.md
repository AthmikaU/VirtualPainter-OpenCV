# Virtual Painter Using Hand Tracking🎨✋

A Python-based virtual painting app that uses your **hand gestures** (tracked by **MediaPipe**) as a brush, powered by **OpenCV** for real-time webcam drawing. You can select colors, switch brush types, erase, and even clear the canvas — all using just your fingers!


## ✨ Features

* **Hand Tracking** using MediaPipe
* **Color Selection** via gesture-based palette
* **Three Brush Types**:

  * Normal
  * Spray
  * Calligraphy
* **Eraser Tool**
* **Clear Canvas Gesture**
* **Brush Toggle Gesture**
* **Real-time Drawing with Webcam**
* **Save Drawing** with a keypress


## 🛠️ Technologies Used

* **Python 3**
* **OpenCV**
* **MediaPipe**
* **NumPy**



## 📦 Installation

1. **Clone this repository**

```bash
git clone https://github.com/AthmikaU/Virtual-Painter-Using-Hand-Tracking
.git
cd Virtual-Painter-Using-Hand-Tracking
```


2. **Create virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


3. **Install dependencies**

```bash
pip install opencv-python mediapipe numpy
```


## ▶️ Running the App

```bash
python app.py
```

* A webcam window will open.
* Use hand gestures to draw and control the interface (explained below).



## ✋ Gesture Controls

| Gesture                          | Action                                           |
| -------------------------------- | ------------------------------------------------ |
| Index finger + Middle up         | Select color from top palette                    |
| Only Index finger up             | Draw on the canvas                               |
| All 5 fingers up                 | Clear the entire canvas                          |
| Index + Middle + Ring fingers up | Toggle brush type (Normal → Spray → Calligraphy) |
| Thumb up                         | Not used                                         |



## 🎨 Tools & UI Elements

* **Top Palette**: Select from 8 predefined colors (last is Eraser).
* **Brush Types**:

  * **Normal**: Basic line
  * **Spray**: Simulated spray effect using random noise
  * **Calligraphy**: Elliptical strokes like a flat nib pen
* **Brush Size**: Fixed size (can be modified in code)
* **Eraser**: Last palette color (black), larger thickness
* **Save Drawing**: Press `s` key to save your artwork
* **Quit Application**: Press `q`


## 🖼️ Output

Your saved drawing will be stored as:

```
my_virtual_painting.png
```



## 📁 File Structure

```
Virtual-Painter-Using-Hand-Tracking/
│
├── app.py       # Main Python script
├── README.md    # This file
```


## 🔧 Customization Tips

* Change brush thickness: modify `brush_thickness` and `eraser_thickness`.
* Add more brush styles or gestures.
* Use dynamic thickness via finger distance.
* Extend for multiple hand support.



## 📜 License

This project is open source under the [MIT License](LICENSE).


## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.


## 🙋‍♀️ Author

**Athmika U**

Feel free to reach out at `athmikaubhat@gmail.com`.



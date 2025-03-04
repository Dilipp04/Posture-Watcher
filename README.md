# Posture Watcher

A desktop application that uses Mediapipe for real-time posture detection and PySide6 for the UI. Posture data is stored locally in a JSON file.

## Features

- Real-time posture detection using Mediapipe.
- User-friendly interface built with PySide6.
- Stores posture data locally in a JSON file.
- Provides feedback on posture status (Good/Bad).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Dilipp04/PostureWatcher.git
   cd PostureWatcher
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run the main script:

```bash
python src/main.py
```

## Usage

1. Launch the application.
2. The application will access your webcam and start detecting your posture in real-time.
3. The posture status will be displayed on the screen.
4. If your posture is good, it will show "Posture Status: Good ✅".
5. If your posture is bad, it will show "Posture Status: Bad ❌".
6. For Yoga Detection:
   Select a yoga pose from the dropdown.
   The application will compare your posture to the selected yoga pose.
   If the detected pose matches with confidence > 80%, it will confirm the correct pose.

## Dependencies

- PySide6
- OpenCV
- Mediapipe
- Tensorflow
- Keras

## Acknowledgements

- [Mediapipe](https://mediapipe.dev/) for the posture detection.
- [PySide6](https://www.qt.io/qt-for-python) for the UI framework.

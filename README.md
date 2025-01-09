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

## File Structure

```
PostureWatcher/
├── assets/                 # Contains images, GIFs, and other assets
├── src/                    # Source code
│   ├── main.py             # Main script to run the application
│   ├── ui/                 # UI components
│   │   ├── dashboard.py    # Dashboard UI
│   │   ├── mainWindow.py   # Main window UI
│   └── components/         # Additional components
│       ├── postureAnalyzer.py  # Posture analysis logic
│       ├── sidePostureDetection.py  # Side posture detection logic
├── requirements.txt        # List of dependencies
├── README.md               # This file
└── venv/                   # Virtual environment (not included in the repository)
```

## Dependencies

- PySide6
- OpenCV
- Mediapipe

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## Acknowledgements

- [Mediapipe](https://mediapipe.dev/) for the posture detection.
- [PySide6](https://www.qt.io/qt-for-python) for the UI framework.

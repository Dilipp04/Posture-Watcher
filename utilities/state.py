from PySide6.QtCore import Signal, QObject

class State(QObject):
    camera_angle_changed = Signal()
    setting_changed = Signal()
    def __init__(self):
        super().__init__()
        self.settings = {
            "camera": 0,                 # Default camera index
            "camera_angle": "Front",      # Possible values: 'front', 'side'
            "delay": 3,                 # Delay in milliseconds (e.g., for timer)
            "position": "Right",        # Default position (e.g., 'center', 'left', 'right')
        }

    # Methods to update or retrieve settings
    def update_setting(self, key, value):
        if key in self.settings:
            self.settings[key] = value
            if key == "camera_angle" or key == "camera":
                self.camera_angle_changed.emit()
            else:
                self.setting_changed.emit()
        else:
            raise KeyError(f"Setting '{key}' does not exist.")

    def get_setting(self, key):
        return self.settings.get(key, None)

    def get_all_settings(self):
        return self.settings

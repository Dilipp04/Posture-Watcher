import time

class Deviation:
    def __init__(self, threshold=40, max_buffer=0):
        self._threshold = threshold
        self._max_buffer = max_buffer
        self._current_buffer = 0
        self._current_deviation = 0

        self._last_updated = 0
        self._last_deviation_passed_threshold = False

    @property
    def max_buffer(self):
        return self._max_buffer

    @property
    def current_buffer(self):
        return self._current_buffer

    @property
    def current_deviation(self):
        return self._current_deviation

    @property
    def deviation_threshold(self):
        return self._threshold

    @property
    def last_updated(self):
        return self._last_updated

    @current_deviation.setter
    def current_deviation(self, value):
        self._current_deviation = value
        self._last_updated = time.time()

    def has_deviated(self):
        deviated = self._current_deviation > self._threshold

        # uses buffer to allow for a deviation before it is alerted
        if deviated:
            if self._current_buffer < self._max_buffer:
                self._current_buffer += 1
                return False
            else:
                self._current_buffer = 0
                return True
        else:
            self._current_buffer = 0
            return False

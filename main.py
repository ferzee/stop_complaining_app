from kivy.config import Config

Config.set('graphics', 'width', '390')  # Set width (in pixels)
Config.set('graphics', 'height', '844')  # Set height (in pixels)

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
import time

# Set the window size for testing

Window.clearcolor = (1, 1, 1, 1)

# Quotes for random display
QUOTES = [
    "Focus on what goes well instead of what doesn’t.",
    "Positive thoughts lead to positive outcomes.",
    "Keep calm and avoid complaining.",
    "Kindness begins with words we choose not to speak."
]

# Explicitly load the .kv file
Builder.load_file("tracker.kv")


class TrackerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Persistent storage setup
        self.store = JsonStore("data.json")
        self.last_reset_time = self.get_last_reset_time()  # Load the reset time
        self.update_time()  # Update the time immediately
        # Schedule periodic updates every second
        Clock.schedule_interval(self.update_time, 1)


    def get_last_reset_time(self):
        # Retrieve or initialize the last reset time
        if self.store.exists("reset_time"):
            return self.store.get("reset_time")["timestamp"]

        current_time = time.time()  # If no reset time exists, use current time
        self.store.put("reset_time", timestamp=current_time)
        return current_time

    def update_time(self, *args):
        # Calculate elapsed time since the last reset
        current_time = time.time()
        elapsed_seconds = int(current_time - self.last_reset_time)

        # Use helper function to determine the time unit and value
        unit, value = self.calculate_time_unit(elapsed_seconds)
        self.ids.counter.text = str(value)
        self.ids.unit.text = unit

    def calculate_time_unit(self, elapsed_seconds):
        """Helper function to calculate appropriate unit and value."""
        if elapsed_seconds < 60:  # Less than 60 seconds
            return "second" if elapsed_seconds == 1 else "seconds", elapsed_seconds
        elif elapsed_seconds < 3600:  # Less than 60 minutes
            minutes = elapsed_seconds // 60
            return "minute" if minutes == 1 else "minutes", minutes
        elif elapsed_seconds < 86400:  # Less than 24 hours
            return "hour" if elapsed_seconds // 3600 == 1 else "hours", elapsed_seconds // 3600
        else:
            return "day" if elapsed_seconds // 86400 == 1 else "days", elapsed_seconds // 86400

    def reset_time(self):
        # Reset the timer and update storage
        self.last_reset_time = time.time()
        self.store.put("reset_time", timestamp=self.last_reset_time)
        self.update_time()


class ComplainingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TrackerScreen(name='complaining'))
        return sm


if __name__ == "__main__":
    ComplainingApp().run()

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class GridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(GridLayout, self).__init__(**kwargs)
        self.rows = 5
        self.cols = 3

        self.name = Label(text="OpenSource AI Watchman")
        self.add_widget(self.name)
        self.description = Label(text="Open source car security software that acts as an AI watchman for your car while you are parked and away.")
        self.add_widget(self.description)

class WatchmanApp(App):
    def build(self):
        return GridLayout()

if __name__ == "__main__":
    WatchmanApp().run()
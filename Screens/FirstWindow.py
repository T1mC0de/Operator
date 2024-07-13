from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from Screens import FirstWindow, SecondWindow, ThirdWindow
from kivy.uix.screenmanager import Screen


kv_first_window = Builder.load_file("../Operator_KHL/Screens/firstwindow.kv")

class FirstWindow(Screen):
    pass
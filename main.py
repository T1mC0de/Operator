from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from Screens import FirstWindow, SecondWindow, ThirdWindow
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

# multitouch disable
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

#Стандартный размер окна при открытии приложения(около 16:9)
from kivy.core.window import Window
Window.size = (1300, 768)

#Ограничение минимального размера окна 800 на 500
Window.minimum_height = 500
Window.minimum_width = 850

#Цвет нашего фона ( серый )
Window.clearcolor = (209/255, 209/255, 209/255, 1)

#-------------------------------------------------------------



#Удаляет базовый курсор, он работает, но его не видно
Window.show_cursor = False


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        Clock.schedule_interval(self.cursorPosition, 1/60)
    
    def cursorPosition(self, *args):
        self.ids.cursor_first.pos = Window.mouse_pos[0] - self.ids.cursor_first.width/2.15, \
                              Window.mouse_pos[1] - self.ids.cursor_first.height/1.5
        self.ids.cursor_second.pos = Window.mouse_pos[0] - self.ids.cursor_second.width/2.15, \
                              Window.mouse_pos[1] - self.ids.cursor_second.height/1.5
        self.ids.cursor_third.pos = Window.mouse_pos[0] - self.ids.cursor_third.width/2.15, \
                              Window.mouse_pos[1] - self.ids.cursor_third.height/1.5
        
        

kv = Builder.load_file("main.kv")

class Operator(App):
    def build(self):
        self.icon = "../Operator_KHL/Images/logo_khl.ico"
        self.title = "Операторская"
        #Window.bind(mouse_pos=self.on_motion)
        return kv

   # def on_motion(self, mouse_pos):
     #   if self.root.ids.butt.collide_point(*mouse_pos):
      #      self.background_normal = "../Operator_KHL/Images/cursor.png"

if __name__ == '__main__':
    Operator().run()


# C каждым окном нашего приложения работай в соотвествующих файлах
# из папки Screens
# 
# Если тебе понадобиться создать четвертое окно, то скопирй оба файла 
# для первого окна поменяв название соответствующих классов
#
# Все фотки в папку Images, если нужно провести 
# какие-то тесты - папка TestFolder
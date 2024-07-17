import os
import random
import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
Window.size = (400,600)
class MyApp(MDApp):
    
    def build(self):
        layout = MDRelativeLayout(md_bg_color = [0,0.5,1,1])
        self.music_dir = 'F:/Project/Parts'
        music_files = os.listdir(self.music_dir)
        
        print(music_files)
        
        self.song_list = [x for x in music_files if x.endswith('mp3')]
        print(self.song_list)
        
        self.song_count = len(self.song_list)
        self.playbutton = MDIconButton(pos_hint={'center_x':0.4, 'center_y':0.05},
                                       icon="play.png",
                                       on_press = self.playaudio)
        
        self.stopbutton = MDIconButton(pos_hint={'center_x':0.55, 'center_y':0.05},
                                       icon="stop.png",
                                       on_press = self.stopaudio)
        layout.add_widget(self.playbutton)
        layout.add_widget(self.stopbutton)        
        
        return layout
    def playaudio(self,obj):
        self.song_title = self.song_list[random.randrange(0, self.song_count)]
        print(self.song_title)
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir, self.song_title))
        self.sound.play()
    def stopaudio(self,obj):
        self.sound.stop()
    
if __name__ == '__main__':
    MyApp().run()
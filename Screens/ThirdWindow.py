from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from Team import Teams

class Turn_Sound:
    def __init__(self) -> None:
        self.siren = SoundLoader.load("../Operator_KHL/Sound/sirena_nhl.mp3")

    def activate_sirena_sound(self):
        if self.siren:
            self.siren.volume = 0.05
            self.siren.play()


class ThirdWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.did_start = False
        self.are_on_pause = 1
        self.disable_goal_button = 1
        self.sound = Turn_Sound()

    def print_time(self):
        self.time_min = str(self.time_min)
        self.time_sec = str(self.time_sec)
        if int(self.time_sec) < 10:
            self.time_sec = '0' + self.time_sec
        if int(self.time_min) < 10:
            self.time_min = '0' + self.time_min
        
        self.ids.time_widget.text = f"{self.time_min}:{self.time_sec}"

    def countdown(self, dt):
        self.print_time()
        self.time_min = int(self.time_min)
        self.time_sec = int(self.time_sec)
        if self.time_sec > 0:
            self.time_sec -= 1
        elif self.time_min > 0:
            self.time_min -= 1
            self.time_sec = 59
        else:
            self.ids.time_widget.color = "red"
            self.ids.time_widget.text = "TIME IS OVER"
            self.ev.cancel()
    
    def start_time(self, *args):
        if self.did_start:
            return
        self.did_start = True
        self.are_on_pause = (self.are_on_pause + 1) % 2
        self.time_min = int(self.ids.time_widget.text.split(':')[0])
        self.time_sec = int(self.ids.time_widget.text.split(':')[1])
        self.ev = Clock.schedule_once(self.countdown)
        self.ev = Clock.schedule_interval(self.countdown, 1)
    
    def change_name_pause(self):
        self.ids.pause_button.text = "PAUSE"
    
    def pause(self):
        self.disable_goal_button = (self.disable_goal_button + 1) % 2
        self.ids.goal_left_team.disabled = self.disable_goal_button
        self.ids.goal_right_team.disabled = self.disable_goal_button
        if self.did_start:
            if self.are_on_pause == 0:
                self.ids.pause_button.text = "START"
                self.ev.cancel()
            else:
                self.ids.pause_button.text = "PAUSE"
                self.ev = Clock.schedule_interval(self.countdown, 1)
            self.are_on_pause = (self.are_on_pause + 1) % 2

    
    def goal_first_team(self):
        self.ids.score_first_team.text = str(int(self.ids.score_first_team.text) + 1)
        self.sound.activate_sirena_sound()
    

    def goal_second_team(self):
        self.ids.score_second_team.text = str(int(self.ids.score_second_team.text) + 1)
        self.sound.activate_sirena_sound()

kv = Builder.load_file("../Operator_KHL/Screens/thirdwindow.kv")

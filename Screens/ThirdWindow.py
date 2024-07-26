from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from Team import Teams
from random import randint

class Turn_Sound:
    def __init__(self) -> None:
        self.siren = SoundLoader.load("../Operator_KHL/Sound/sirena_nhl.mp3")
        self.end_period = SoundLoader.load("../Operator_KHL/Sound/period.mp3")
        self.music_list = [
            SoundLoader.load("../Operator_KHL/Music/Linkin Park - Breaking the Habit.mp3"),
            SoundLoader.load("../Operator_KHL/Music/Linkin Park - In the End.mp3"),
            SoundLoader.load("../Operator_KHL/Music/Linkin Park - New Divide.mp3"),
            SoundLoader.load("../Operator_KHL/Music/Linkin Park - Numb.mp3"),
            SoundLoader.load("../Operator_KHL/Music/Linkin Park - Somewhere I Belong.mp3"),
            SoundLoader.load("../Operator_KHL/Music/Linkin Park - What I&#39;ve Done.mp3")
        ]
        self.last_track = -1
        self.next_track = 0


    def activate_sirena_sound(self):
        if self.siren:
            self.siren.volume = 0.5
            self.siren.play()

    def activate_end_period_sound(self):
        if self.end_period:
            self.end_period.volume = 0.5
            self.end_period.play()


class ThirdWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.are_on_pause = 1
        self.disable_goal_button = 1
        self.sound = Turn_Sound()
        self.periods = 1
        self.period_time = "00:55"
        self.music_var = 0
        Window.bind(on_key_down=self.binds)
        
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
            self.pause()
            self.change_period()
            self.sound.activate_end_period_sound()
            self.ev.cancel()
    
    def pause(self):
        if self.ids.time_widget.text == self.period_time:
            self.sound.activate_end_period_sound()
        self.disable_goal_button = (self.disable_goal_button + 1) % 2
        self.ids.goal_left_team.disabled = self.disable_goal_button
        self.ids.goal_right_team.disabled = self.disable_goal_button
        if self.are_on_pause == 0:
            self.ids.pause_button.text = "START"
            self.ev.cancel()
        else:
            self.time_min = int(self.ids.time_widget.text.split(':')[0])
            self.time_sec = int(self.ids.time_widget.text.split(':')[1])
            self.ids.pause_button.text = "PAUSE"
            self.ev = Clock.schedule_once(self.countdown)
            self.ev = Clock.schedule_interval(self.countdown, 1)
        self.are_on_pause = (self.are_on_pause + 1) % 2

    def goal_first_team(self):
        self.ids.score_first_team.text = str(int(self.ids.score_first_team.text) + 1)
        self.sound.activate_sirena_sound()
    

    def goal_second_team(self):
        self.ids.score_second_team.text = str(int(self.ids.score_second_team.text) + 1)
        self.sound.activate_sirena_sound()

    def change_period(self):
        if self.periods == 3:
            pass
        elif self.periods == 1:
            self.ids.period.text = "2'nd period"
        elif self.periods == 2:
            self.ids.period.text = "3'd period"
        self.periods += 1
        self.ids.time_widget.text = self.period_time
        self.did_start = False  
    
    def binds(self, *args):
        key = list(args)[2]
        print(key)
        if key == 229:
            self.goal_second_team()
            self.pause()
        if key == 225:
            self.goal_first_team()
            self.pause()
        if key == 44:
            self.pause()
    

kv = Builder.load_file("../Operator_KHL/Screens/thirdwindow.kv")

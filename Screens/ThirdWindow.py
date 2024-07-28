from kivy.uix.actionbar import Button
from kivy.uix.accordion import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from Team import Teams
from Screens import SecondWindow
from random import randint

score_left_team = 0
score_right_team = 0
cancel_left = 1

class Turn_Sound:
    def __init__(self) -> None:
        self.siren = SoundLoader.load("../Operator_KHL/Sound/main_goal_siren.mp3")
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
        self.last_minute = SoundLoader.load("../Operator_KHL/Sound/last_m_1.mp3")
        self.count_goal = SoundLoader.load("../Operator_KHL/Sound/goal_ok.mp3")
        self.not_count_goal = SoundLoader.load("../Operator_KHL/Sound/no_goal.mp3")
        self.timeout = SoundLoader.load("../Operator_KHL/Sound/to.mp3")

    def activate_sirena_sound(self, *args):
        if self.siren:
            self.siren.volume = 0.5
            self.siren.play()

    def activate_end_period_sound(self, *args):
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
        self.period_time = "20:00"
        self.music_var = 0
        self.team = 0
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
        if self.time_min == 2 and self.time_sec == 0:
            self.sound.last_minute.play()
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
        self.ids.timeout_left.disabled = (self.disable_goal_button + 1) % 2
        self.ids.timeout_right.disabled = (self.disable_goal_button + 1) % 2
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

    def update_score(self):
        global score_right_team, score_left_team
        self.ids.score_first_team.text = str(score_left_team)
        self.ids.score_second_team.text = str(score_right_team)


    def goal_first_team(self):
        global score_right_team, score_left_team
        score_left_team += 1
        self.update_score()
        self.sound.activate_sirena_sound()
    
    def cancel_goal_first_team(self):
        global score_right_team, score_left_team
        self.ids.score_first_team.text = str(int(self.ids.score_first_team.text) - 1)

    def goal_second_team(self):
        global score_right_team, score_left_team
        score_right_team += 1
        self.update_score()
        self.sound.activate_sirena_sound()
    
    def cancel_goal_second_team(self):
        global score_right_team, score_left_team
        self.ids.score_second_team.text = str(int(self.ids.score_second_team.text) - 1)

    def change_period(self):
        if self.periods == 3:
            pass
        elif self.periods == 0:
            self.ids.period.text = "1'st period"
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
        if key == 229 and not self.are_on_pause:
            self.goal_second_team()
            self.pause()
        if key == 225 and not self.are_on_pause:
            self.goal_first_team()
            self.pause()
        if key == 44:
            self.pause()
    
    def back_button_func(self):
        global score_right_team, score_left_team
        self.are_on_pause = 1
        self.disable_goal_button = 1        
        self.periods = 0
        self.period_time = "20:00"
        self.music_var = 0
        score_left_team = 0
        score_right_team = 0
        self.ids.score_first_team.text = str(score_left_team)
        self.ids.score_second_team.text = str(score_right_team)
        self.ev.cancel()
        if SecondWindow.fans.state == "play":
            SecondWindow.fans.stop()
        self.change_period()
    
    def timeout_button(self):
        self.sound.timeout.play()
        Clock.schedule_once(self.sound.activate_end_period_sound, 30)
        self.pause()


    def choose_team_left(self):
        self.team = 1

    def choose_team_right(self):
        self.team = 2

    def count_goal_for_team(self, *args):
        self.sound.count_goal.play()        

    def not_count_goal_for_team(self, *args):
        global score_right_team, score_left_team, cancel_left

        if self.team == 1:
            score_left_team -= 1
        else:
            score_right_team -= 1

        self.update_score()
        self.sound.not_count_goal.play()

    def cursor_pos_for_popup(self, *args):
        self.cursor.pos = (Window.mouse_pos[0] - self.cursor.width/2,  
                           Window.mouse_pos[1] - self.cursor.height/2)

    def coach_req(self):
        layout = FloatLayout()

        button_accept = Button(text="Засчитываем",
                               size_hint=(0.8, 0.4),
                               pos_hint={"x": 0.1, "y":0.5},
                               on_press=self.count_goal_for_team)
        
        button_not_accept = Button(text="Не засчитываем", 
                                   size_hint=(0.8, 0.4), 
                                   pos_hint={"x": 0.1, "y":0.05},
                                   on_press=self.not_count_goal_for_team)

        self.cursor = Image(source='../Operator_KHL/Images/cursor.png',
                       size_hint = (0.085*2, 0.085*2))
        Clock.schedule_interval(self.cursor_pos_for_popup, 1/60)


        layout.add_widget(button_accept)
        layout.add_widget(button_not_accept)
        layout.add_widget(self.cursor)

        popup = Popup(title="Подтвердите отмену шайбы, либо оставьте счет",
                      content=layout,
                      size_hint=(0.5, 0.5),
                      auto_dismiss = False)
        
        popup.open()

        button_accept.bind(on_release=popup.dismiss)
        button_not_accept.bind(on_release=popup.dismiss)

# class PopupsWindow(Popup):
#     def __init__(self, **kw):
#         super().__init__(**kw)
#         self.sound = Turn_Sound()
#         self.team = 0

#     def choose_team_left(self):
#         self.team = 1

#     def choose_team_right(self):
#         self.team = 2

#     def count_goal_for_team(self):
#         self.sound.count_goal.play()
    
#     def not_count_goal_for_team(self):
#         global score_right_team, score_left_team, cancel_left
#         print(2)
#         score_left_team -= 1
#         self.sound.not_count_goal.play()
        
        
        
        
        
        
        


kv = Builder.load_file("../Operator_KHL/Screens/thirdwindow.kv")

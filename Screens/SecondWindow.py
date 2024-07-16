from kivy.uix.tabbedpanel import StripLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from Team import Teams

kv = Builder.load_file("../Operator_KHL/Screens/secondwindow.kv")

class SecondWindow(Screen):
    def on_checkbox_active(checkbox, instance, value):
        if value:
            print('The checkbox', checkbox, 'is active')
        else:
            print('The checkbox', checkbox, 'is not active')

    def on_button_left_choosing_left_team(self): 
        Teams.index_first_team = abs(Teams.index_first_team - 1)
        Teams.index_first_team %= len(Teams.Teams_list)

        self.ids.name_team1.text = Teams.Teams_list[Teams.index_first_team].name
        self.ids.logo_team1.source = Teams.Teams_list[Teams.index_first_team].source_logo 

    def on_button_right_choosing_left_team(self): 
        Teams.index_first_team += 1
        Teams.index_first_team %= len(Teams.Teams_list)

        self.ids.name_team1.text = Teams.Teams_list[Teams.index_first_team].name
        self.ids.logo_team1.source = Teams.Teams_list[Teams.index_first_team].source_logo

    def on_button_left_choosing_right_team(self):
        Teams.index_second_team = abs(Teams.index_second_team - 1)
        Teams.index_second_team %= len(Teams.Teams_list)

        self.ids.name_team2.text = Teams.Teams_list[Teams.index_second_team].name
        self.ids.logo_team2.source = Teams.Teams_list[Teams.index_second_team].source_logo

    def on_button_right_choosing_right_team(self):
        Teams.index_second_team += 1
        Teams.index_second_team %= len(Teams.Teams_list)

        self.ids.name_team2.text = Teams.Teams_list[Teams.index_second_team].name
        self.ids.logo_team2.source = Teams.Teams_list[Teams.index_second_team].source_logo

    # эту функцию не трогать - рабочий прототип переноса данных 
    # со второго на третий экран
    def on_button_start(self):
        #self.manager.get_screen('third').ids.first_team.text = Teams.Teams_list[Teams.index_first_team].name
        self.manager.get_screen('third').ids.goal_left_team.disabled = 1
        self.manager.get_screen('third').ids.goal_right_team.disabled = 1
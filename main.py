from kivy.app import App
from kivymd.app import MDApp
from kivy.core.window import Window
Window.size = (900,400)
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, Clock, StringProperty, ObjectProperty
from kivy.lang.builder import Builder
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
Builder.load_file("on_game.kv")
Builder.load_file("start_page.kv")
Builder.load_file("record_db.kv")
Builder.load_file("overall_rank.kv")
Builder.load_file("player_detail.kv")

class MainInterface(RelativeLayout):

    start = ObjectProperty()
    game = ObjectProperty()
    record = ObjectProperty()
    rank = ObjectProperty()
    detail = ObjectProperty()

    player_one_name = StringProperty("")
    player_two_name = StringProperty("")
    player_three_name = StringProperty("")
    player_four_name = StringProperty("")
    
    #Base, Tai value
    base = StringProperty("")
    tai = StringProperty("")


    def __init__(self,**kwargs):
        super(RelativeLayout, self).__init__(**kwargs)


    def start_game(self):
        self.start.opacity = 0
        self.game.opacity = 1
        
        #Assign player name to game page
        self.player_one_name = self.start.ids.player_one_name_input.text
        self.player_two_name = self.start.ids.player_two_name_input.text
        self.player_three_name = self.start.ids.player_three_name_input.text
        self.player_four_name = self.start.ids.player_four_name_input.text

        #Assign base and tai value
        self.base = self.start.ids.base.text
        self.tai = self.start.ids.tai.text

        #Initialize the record table
        self.record.init_record_column()

        #Initialize the default game page value
        self.game.init_game_start_state()

    def go_rank(self):
        self.start.opacity = 0
        self.rank.opacity = 1
        self.rank.show_overall_rank()

    
    def back_start_page(self):
        self.game.opacity = 0
        self.start.opacity = 1

    def detail_page(self):
        self.record.opacity = 0.8
        self.game.opacity = 0
        self.start.opacity = 0

    def overall_rank_page(self):
        self.game.stop_animation()
        self.game.opacity = 0
        self.rank.add_database()
        self.rank.opacity = 1
            

class MainApp(MDApp):
    pass

MainApp().run()
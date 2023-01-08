from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.label import Label
from kivy.metrics import dp
import pymongo
from datetime import date

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
#This specify which database you're looking into, if database doesn't exist, create one
mydb = client["Mahjong_tracker"]

#This creates a table called best_score
overall_rank = mydb["overall_rank"]

class Player_detail(RelativeLayout):
    
    def __init__(self,**kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        
        self.opacity = 0
        
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)
    
    def add_record(self):
        
        result = overall_rank.find_one({"name":self.parent.rank.player_detail_name.lower()})

        
        scrollview_layout = ScrollView()

        main_layout = BoxLayout(orientation = "vertical", size_hint = (1, None), height = 800, padding = (dp(0),self.height*.1, dp(0), self.height*.1))

        #The name of the player detail
        name = Label(
            text = self.parent.rank.player_detail_name,
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 32,
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
            )

        #Join Date
        date_title = Label(
            text = "Join Date: "+ result["date"],
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1))

        #TOTAL ROUND
        total_round_box_layout = BoxLayout(spacing = 10, orientation = "horizontal", padding =(dp(0),dp(0), dp(0), self.height*.05) )
        total_round_title = Label(
            text = "TOTAL ROUND",
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        total_round = Label(
            text = str(result["total round"]),
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        total_round_box_layout.add_widget(total_round_title)
        total_round_box_layout.add_widget(total_round)
        #Win rate
        win_rate_box_layout = BoxLayout(spacing = 10, orientation = "horizontal", padding =(dp(0),dp(0), dp(0), self.height*.05) )
        win_rate_title = Label(
            text = "WIN RATE",
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        win_rate = Label(
            text = str(round(result["win rate"],2))+"%",
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        win_rate_box_layout.add_widget(win_rate_title)
        win_rate_box_layout.add_widget(win_rate)
        #Money per game
        money_per_game_box_layout = BoxLayout(spacing = 10, orientation = "horizontal", padding =(dp(0),dp(0), dp(0), self.height*.05) )
        money_per_game_title = Label(
            text = "MONEY PER GAME",
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        money_per_game = Label(
            text = str(round(result["Money"]/result["total round"],2)),
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        money_per_game_box_layout.add_widget(money_per_game_title)
        money_per_game_box_layout.add_widget(money_per_game)

        #Self touch times
        self_touch_time_box_layout = BoxLayout(spacing = 10, orientation = "horizontal", padding =(dp(0),dp(0), dp(0), self.height*.05) )
        self_touch_time_title = Label(
            text = "SELF TOUCH TIMES",
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        self_touch_time = Label(
            text = str(result["self touch time"]),
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        self_touch_time_box_layout.add_widget(self_touch_time_title)
        self_touch_time_box_layout.add_widget(self_touch_time)

        #Win times
        win_time_box_layout = BoxLayout(spacing = 10, orientation = "horizontal", padding =(dp(0),dp(0), dp(0), self.height*.05) )
        win_time_title = Label(
            text = "WIN TIMES",
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        win_time = Label(
            text = str(result["win time"]),
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        win_time_box_layout.add_widget(win_time_title)
        win_time_box_layout.add_widget(win_time)

        #Lose times
        lose_time_box_layout = BoxLayout(spacing = 10, orientation = "horizontal", padding =(dp(0),dp(0), dp(0), self.height*.05) )
        lose_time_title = Label(
            text = "LOSE TIMES",
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        lose_time = Label(
            text = str(result["lose time"]),
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
            font_size = 16, 
            padding = (dp(0),dp(100)),
            color = (1,1,1,1)
        )
        lose_time_box_layout.add_widget(lose_time_title)
        lose_time_box_layout.add_widget(lose_time)



        button = MDRectangleFlatButton(
            text = "BACK", 
            size_hint = (.3,.7), 
            pos_hint = {"y":0.4, "center_x":0.5}, 
            font_size = 16,
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf",
            text_color = (1, 1, 1, 1),
            line_color = (1, 1, 1, 1)
        )
        button.bind(on_release = self.back_to_rank)
        
        #Add widget to the mainlayout (Vertical boxlayout)
        main_layout.add_widget(name)
        main_layout.add_widget(date_title)
        main_layout.add_widget(total_round_box_layout)
        main_layout.add_widget(win_rate_box_layout)
        main_layout.add_widget(money_per_game_box_layout)
        main_layout.add_widget(self_touch_time_box_layout)
        main_layout.add_widget(win_time_box_layout)
        main_layout.add_widget(lose_time_box_layout)
        main_layout.add_widget(button)

        #Add the mainlayout to the scrollview layout
        scrollview_layout.add_widget(main_layout)
        #Add scrollview layout to the class
        self.add_widget(scrollview_layout)

    def back_to_rank(self, instance):
        self.canvas.clear()
        self.opacity = 0
        self.parent.rank.opacity = 1

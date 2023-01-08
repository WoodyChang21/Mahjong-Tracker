from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import Screen
from kivy.metrics import dp
import pymongo
from datetime import date

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
#This specify which database you're looking into, if database doesn't exist, create one
mydb = client["Mahjong_tracker"]

#This creates a table called best_score
overall_rank = mydb["overall_rank"]

class Overall_rank(RelativeLayout):
    
    def __init__(self,**kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        self.opacity = 0
        self.total_record = []
        
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)

    def add_database(self):
        player_list = [
            self.parent.player_one_name,
            self.parent.player_two_name,
            self.parent.player_three_name,
            self.parent.player_four_name
            ]
        player_money = [
            self.parent.game.player_one_money,
            self.parent.game.player_two_money,
            self.parent.game.player_three_money,
            self.parent.game.player_four_money
        ]

        player_info = self.parent.game.player_info[:]

        for index, name in enumerate(player_list):
            result = overall_rank.find_one({"name":name.lower()})
            #If no such name inside the record create one 
            if result == None:
                print("NEW")
                print(date.today())
                if int(player_money[index].text)>0:
                     win_rate = 100
                     win_game = 1
                else:
                    win_rate = 0
                    win_game = 0
                result = overall_rank.insert_one({
                    "date": str(date.today()),
                    "name": name.lower(),
                    "Money": int(player_money[index].text),
                    "total round": 1,
                    "win rate": win_rate,
                    "win game": win_game,
                    "self touch time": player_info[index].self_touch,
                    "win time": player_info[index].win,
                    "lose time": player_info[index].lose
                })
            #Add the money on the player
            #Add total_round
            else:
                print("Update")
                current_money = result["Money"]
                current_round = result["total round"]
                current_win_game = result["win game"]
                current_self_touch_time = result["self touch time"]
                current_win_time = result["win time"]
                current_lose_time = result["lose time"]

                if int(player_money[index].text)>0:
                    win_game = current_win_game + 1
                    win_rate = (win_game/(current_round+1))*100
                else:
                    win_game = current_win_game
                    win_rate = (current_win_game/(current_round+1))*100

                #Update the player info
                overall_rank.update_one({"name":name.lower()},
                {"$set":{
                    "Money": current_money+int(player_money[index].text),
                    "total round": current_round+1,
                    "win game": win_game,
                    "win rate": win_rate,
                    "self touch time": current_self_touch_time + player_info[index].self_touch,
                    "win time": current_win_time + player_info[index].win,
                    "lose time": current_lose_time + player_info[index].lose
                    }})
        
        self.show_overall_rank()
                
                
            

    def show_overall_rank(self):
        rank = 1
        player_detail = []
        scrollview_layout = ScrollView()

        main_layout = BoxLayout(orientation = "vertical", size_hint = (1, None), height = 800, padding = (dp(0),self.height*.1, dp(0), self.height*.1))
        rank_layout = BoxLayout(padding = (dp(0),dp(0), dp(0), dp(50)) )
        rank_label = Label(text = "R A N K", font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", font_size = 40)
        rank_layout.add_widget(rank_label)
        main_layout.add_widget(rank_layout)
        
        result = overall_rank.find().sort("Money", -1)
        for x in result:
            #Every element is a dictionary
            player_detail.append(x)

        
        for i in range(len(player_detail)):
            player_layout = BoxLayout(spacing = 10, orientation = "horizontal", padding =(dp(0),dp(0), dp(0), self.height*.05) )
            #Label for each player (Rank, name, money)
            label_rank = Label(
                text = str(rank), 
                font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
                font_size = 16, 
                padding = (dp(0),dp(100)))
            label_name = Label(
                text = player_detail[i]["name"].capitalize(), 
                font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
                font_size = 16, 
                padding = (dp(0),dp(100)))
            label_money = Label(
                text = str(player_detail[i]["Money"]),
                font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
                font_size = 16, 
                padding = (dp(0),dp(100)))

            detail_button_layout = RelativeLayout(size_hint_y = .5 )
            detail_button = MDRectangleFlatButton(
                text = "DETAIL",
                font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf", 
                font_size = 16,
                size_hint = (.6,.6),
                padding = (dp(50),dp(0)),
                text_color = (1, 1, 1, 1),
                line_color = (1, 1, 1, 1))
            detail_button_layout.add_widget(detail_button)
            
            #Bind the detail button
            detail_button.bind(on_release = self.player_detail_page)

            player_layout.add_widget(label_rank)
            player_layout.add_widget(label_name)
            player_layout.add_widget(label_money)
            player_layout.add_widget(detail_button_layout)
            main_layout.add_widget(player_layout)

            rank+=1

        #Back to home button
        home = MDRectangleFlatButton(
            text = "Home", 
            size_hint = (.5,.7), 
            pos_hint = {"y":0.4, "center_x":0.5}, 
            font_size = 16,
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf",
            text_color = (1, 1, 1, 1),
            line_color = (1, 1, 1, 1))
    
        home.bind(on_release = self.back_to_game)
        main_layout.add_widget(home)

        scrollview_layout.add_widget(main_layout)
        self.add_widget(scrollview_layout)
    

    def back_to_game(self, instance):
        self.canvas.clear()
        self.opacity = 0
        self.parent.start.opacity = 1
    
    def player_detail_page(self, instance):
        print(instance.parent.parent.children[2].text)
        self.player_detail_name = instance.parent.parent.children[2].text
        self.opacity = 0
        self.parent.detail.opacity = 1
        self.parent.detail.add_record()

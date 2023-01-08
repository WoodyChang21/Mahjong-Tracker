from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import Screen
from kivy.metrics import dp
import pymongo
from datetime import date

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
#This specify which database you're looking into, if database doesn't exist, create one
mydb = client["Mahjong_tracker"]

#This creates a table called record_detail
record_detail = mydb["record_detail"]

class Record_db(RelativeLayout):

    def __init__(self,**kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        self.opacity = 0
        self.total_record = []
        self.next_id = record_detail.find().sort('_id', -1).limit(1)[0]['_id']+1

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)

    def update(self):
        self.round = ["E","S","W","N"]
        self.player_one = self.parent.player_one_name
        self.player_two = self.parent.player_two_name
        self.player_three = self.parent.player_three_name
        self.player_four = self.parent.player_four_name
        self.record = self.parent.game.current_state
        self.player_one_money = self.record["player0_money_difference"]
        self.player_two_money = self.record["player1_money_difference"]
        self.player_three_money = self.record["player2_money_difference"]
        self.player_four_money = self.record["player3_money_difference"]

        self.current_round = self.round[self.parent.game.current_round]
        self.dealer = self.current_round+str(self.record['dealer_index']+1)

        #This takes care whenever a new round started
        if self.current_round != "E" and self.record['player0_background_color'] == [.2,.3,.1,.3] and self.record['player0_dealer_count']=="0":
            #Since N is the last round
            if self.current_round != "N":
                self.current_round = self.round[self.parent.game.current_round-1]
            self.dealer = self.current_round+str(4)

        
        self.total_record.append({
            "Round":self.record['total_round'],
            "dealer":self.dealer,
            self.player_one:self.player_one_money,
            self.player_two:self.player_two_money,
            self.player_three:self.player_three_money,
            self.player_four:self.player_four_money
        })

        #If no data inside create an id
        if record_detail.count_documents({"_id":self.next_id})==0:
            result = record_detail.insert_one({
                "_id":self.next_id,
                "date": str(date.today()),
                "record": self.total_record
            })
        #There are data inside, just update the record column
        else:
            record_detail.update_one({"_id":self.next_id},{"$set":{"record":self.total_record}})

    def init_record_column(self):
        
        self.table = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            rows_num = 100,
            column_data = [
                ("Round", dp(30)),
                ("Dealer", dp(30)),
                (self.parent.player_one_name, dp(30)),
                (self.parent.player_two_name, dp(30)),
                (self.parent.player_three_name, dp(30)),
                (self.parent.player_four_name, dp(30))
            ]
        )
        layout = BoxLayout(spacing = 10, orientation = "vertical")
        self.add_widget(self.table)
        back_game = Button(
            text = "Back", 
            size_hint = (.1,.1), 
            pos_hint = {"y":0.05, "center_x":0.5}, 
            font_size = self.height*0.05,
            font_name = "C:\\Users\\User\\Desktop\\Python Project\\font\\Sackers-Gothic-Std-Light.ttf"
            )
        back_game.bind(on_release = self.back_to_game)
        self.add_widget(back_game)
        return layout

    def add_record(self):
        black = "21130d"
        red = "A03a0e"
        player_color = [black, black, black, black]
        last_record = record_detail.find({"_id":self.next_id})
        for record in last_record:
            round = record["record"][-1]["Round"]
            dealer = record["record"][-1]["dealer"]
            player_one_money =  record["record"][-1][self.parent.player_one_name]
            player_two_money =  record["record"][-1][self.parent.player_two_name]
            player_three_money =  record["record"][-1][self.parent.player_three_name]
            player_four_money =  record["record"][-1][self.parent.player_four_name]

        #Make the self_touch player money red in record interface
        player_money_list = [player_one_money, player_two_money, player_three_money, player_four_money]
        for index, player_money in enumerate(player_money_list):
            player_money_list_copy = player_money_list[:]
            player_money_list_copy.pop(index)
            for index_copy, money in enumerate(player_money_list_copy):
                if int(money) < 0:
                    pass
                else:
                    break
                #Will only get here if all the money are negative
                if index_copy == 2:
                    player_color[index] = red
                    break
        self.row_data = [(round,dealer,f"[color=#{player_color[0]}]{player_one_money}[/color]",f"[color=#{player_color[1]}]{player_two_money}[/color]",f"[color=#{player_color[2]}]{player_three_money}[/color]",f"[color=#{player_color[3]}]{player_four_money}[/color]")]   
        self.table.add_row((round,dealer,f"[color=#{player_color[0]}]{player_one_money}[/color]",f"[color=#{player_color[1]}]{player_two_money}[/color]",f"[color=#{player_color[2]}]{player_three_money}[/color]",f"[color=#{player_color[3]}]{player_four_money}[/color]"))

    def remove_row(self):
        #Remove the row in the mddatatable
        self.table.remove_row(self.row_data[-1])

        #Update the database
        self.total_record.pop()
        record_detail.update_one({"_id":self.next_id},{"$set":{"record":self.total_record}})
        self.parent.game.total_round -= 1

    def back_to_game(self, instance):
        self.opacity = 0
        self.parent.game.opacity = 1
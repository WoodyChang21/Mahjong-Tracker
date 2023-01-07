from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, Clock, StringProperty, ObjectProperty
from kivy.animation import Animation
import time

class On_game(RelativeLayout):
    #These are winner/loser attribute
    #These are toggle buttons
    winner_one = ObjectProperty()
    winner_two = ObjectProperty()
    winner_three = ObjectProperty()
    winner_four = ObjectProperty()
    loser_one = ObjectProperty()
    loser_two = ObjectProperty()
    loser_three = ObjectProperty()
    loser_four = ObjectProperty()
    self_touch = ObjectProperty()

    #These are the player money
    #These are labels
    player_one_money = ObjectProperty()
    player_two_money = ObjectProperty()
    player_three_money = ObjectProperty()
    player_four_money = ObjectProperty()

    #Amount of money
    amount_of_tai = ObjectProperty()

    #Dealer
    dealer_one = ObjectProperty()
    dealer_two = ObjectProperty()
    dealer_three = ObjectProperty()
    dealer_four = ObjectProperty()

    #Dealer background
    player_one_background = ObjectProperty()
    player_two_background = ObjectProperty()
    player_three_background = ObjectProperty()
    player_four_background = ObjectProperty()

    #Round (E S W N)
    round_E = ObjectProperty()
    round_S = ObjectProperty()
    round_W = ObjectProperty()
    round_N = ObjectProperty()

    #Record current round (E S W N)
    current_round = 0

    #Record the total round 
    total_round = 0

    #Undo usage state: previous_state
    previous_state = {}

    #Detail page usage state, Database usage state: Current State
    current_state = {}

    #Animation Object
    anim_player_color = Animation(player_color=(.2,.3,.1,.3), duration = .5) +  Animation(player_color=(1, 1, 1, 1), duration=.5)
    anim_player_color.repeat = True
    anim_round = Animation(round_color = (.2,.3,.1,.6), duration = .5) + Animation(round_color = (1,1,1,1), duration = .5)
    anim_round.repeat = True
    finish_button = Animation(color = (1,.2,.3,.6), duration = .5) + Animation(color = (0,0,0,1), duration = .5)
    finish_button.repeat = True

    #Store player info
    player_one = type("player_one",(),{})
    player_two = type("player_two",(),{})
    player_three = type("player_three",(),{})
    player_four = type("player_four",(),{})

    def __init__(self,**kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        #Initialize the previous state
        self.init_previous_state()
        self.init_current_state()
    
    def on_touch_down(self, touch):
        if self.parent.record.opacity != 0 or self.parent.start.opacity != 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)

    #This is called everytime the start button from the start page is pressed
    def init_game_start_state(self):
        self.total_round = 0

        #Round background
        self.round_E.round_color = (.2,.3,.1,.6)
        self.round_S.round_color = (1,1,1,1)
        self.round_W.round_color = (1,1,1,1)
        self.round_N.round_color = (1,1,1,1)

        #Player background
        self.player_one_background.player_color = (.2,.3,.1,.3)
        self.player_two_background.player_color = (1,1,1,1) 
        self.player_three_background.player_color = (1,1,1,1)
        self.player_four_background.player_color = (1,1,1,1)

        #Player money
        self.player_one_money.text = "0"
        self.player_two_money.text = "0"
        self.player_three_money.text = "0"
        self.player_four_money.text = "0"

        #Dealer text
        self.dealer_one.text = "0"
        self.dealer_two.text = ""
        self.dealer_three.text = ""
        self.dealer_four.text = ""

        #Finish button color
        self.ids.finish_button.color = (0,0,0,1)

        #Store self_touch times, win_times, lose_times
        self.player_info = [self.player_one, self.player_two, self.player_three, self.player_four]
        for player in self.player_info:
            player.self_touch = 0
            player.win = 0
            player.lose = 0

    def init_previous_state(self):
        self.previous_state = {
            #Track total round
            "total_round": self.total_round,

            #Track winner_index, dealer_index, loser_index
            "winner_index": 0,
            "loser_index": 0,
            "dealer_index":0,

            #player background color
            "player0_background_color": (.2,.3,.1,.3),
            "player1_background_color": (1,1,1,1),
            "player2_background_color": (1,1,1,1),
            "player3_background_color": (1,1,1,1),

            #player money
            "player0_money": "0",
            "player1_money": "0",
            "player2_money": "0",
            "player3_money": "0",

            #Dealer count
            "player0_dealer_count": "0",
            "player1_dealer_count": "",
            "player1_dealer_count": "",
            "player1_dealer_count": "",

            #Current round background color
            "round_E_background_color": (.2,.3,.1,.6),
            "round_S_background_color": (1,1,1,1),
            "round_W_background_color": (1,1,1,1),
            "round_N_background_color": (1,1,1,1),
        }
    def init_current_state(self):
        self.current_state = {
            #Track total round
            "total_round": self.total_round,

            #Track winner_index, dealer_index, loser_index
            "winner_index": 0,
            "loser_index": 0,
            "dealer_index":0,

            #player background color
            "player0_background_color": (.2,.3,.1,.3),
            "player1_background_color": (1,1,1,1),
            "player2_background_color": (1,1,1,1),
            "player3_background_color": (1,1,1,1),

            #player money
            "player0_money": "0",
            "player1_money": "0",
            "player2_money": "0",
            "player3_money": "0",

            #Dealer count
            "player0_dealer_count": "0",
            "player1_dealer_count": "",
            "player1_dealer_count": "",
            "player1_dealer_count": "",

            #Current round background color
            "round_E_background_color": (.2,.3,.1,.6),
            "round_S_background_color": (1,1,1,1),
            "round_W_background_color": (1,1,1,1),
            "round_N_background_color": (1,1,1,1),
        }

    def submit_button(self):

        #Update previous state before doing any changes
        self.update_previous_state()

        player_money = [self.player_one_money, self.player_two_money, self.player_three_money, self.player_four_money]
        winner = [self.winner_one, self.winner_two, self.winner_three, self.winner_four]
        loser = [self.loser_one, self.loser_two, self.loser_three, self.loser_four]
        dealer = [self.dealer_one, self.dealer_two, self.dealer_three, self.dealer_four]
        background = [self.player_one_background, self.player_two_background, self.player_three_background, self.player_four_background]
        round = [self.round_E, self.round_S, self.round_W, self.round_N]

        base = int(self.parent.base)
        tai = int(self.parent.tai)

        winner_index = None
        loser_index = None
        dealer_index = None

        
        #Find the index of the dealer
        #dealer_index is the index of the dealer
        for index, dealers in enumerate(dealer):
            if dealers.text != "":
                dealer_index = index
                dealer_tai = 2*int(dealer[index].text)+1
        
        #Find the winner index
        for index, winners in enumerate(winner):
            if winners.state == "down":
                    winner_index = index
        
        #Find the loser index
        for index, losers in enumerate(loser):
            if losers.state == "down":
                    loser_index = index

        #Check if loser, winner and self touch is actually pressed
        if winner_index == None or (loser_index == None and self.self_touch.state == "normal"):
            return False


        #Check if self-touch is pressed
        #This part only takes care of the winner money
        if self.self_touch.state == "down":
            if self.amount_of_tai.text.isdigit():
                #Update player info
                self.player_info[winner_index].self_touch += 1
                #First:
                #Self touch: dealer
                if winner_index == dealer_index:
                    player_money[winner_index].text = str(int(player_money[winner_index].text)+ (base+tai*(int(self.amount_of_tai.text)+dealer_tai))*3) 
                    #Loser loses money
                    for index, losers in enumerate(loser):
                        if index == winner_index:
                            pass
                        else:
                            #Update player info
                            self.player_info[index].lose+=1
                            print(self.player_info[index].lose)
                            
                            player_money[index].text = str(int(player_money[index].text)-(base+tai*(int(self.amount_of_tai.text)+dealer_tai)))
                #Self touch: not dealer
                else:
                    player_money[winner_index].text = str(int(player_money[winner_index].text)+ (base+tai*(int(self.amount_of_tai.text)))*2+(base+tai*(int(self.amount_of_tai.text)+dealer_tai)))
                    #Loser loses money
                    for index, losers in enumerate(loser):
                        if index == winner_index:
                            pass
                        elif index == dealer_index:
                            #Update player info
                            self.player_info[index].lose+=1
                            print(self.player_info[index].lose)
                            player_money[index].text = str(int(player_money[index].text)-(base+tai*(int(self.amount_of_tai.text)+dealer_tai)))
                        else:
                            #Update player info
                            self.player_info[index].lose+=1
                            print(self.player_info[index].lose)
                            player_money[index].text = str(int(player_money[index].text)-(base+tai*(int(self.amount_of_tai.text))))
            else:
                pass

        #Self touch is not pressed
        else:
            if self.amount_of_tai.text.isdigit():
                #Loser: Dealer or Loser: Not Dealer, Winner is dealer
                if loser_index == dealer_index or winner_index == dealer_index:
                    #Update player info
                    self.player_info[loser_index].lose+=1
                    self.player_info[winner_index].win+=1

                    player_money[loser_index].text = str(int(player_money[loser_index].text)-(base+tai*(int(self.amount_of_tai.text)+dealer_tai)))
                    player_money[winner_index].text = str(int(player_money[winner_index].text)+(base+tai*(int(self.amount_of_tai.text)+dealer_tai)))
                #Loser is not dealer, winner is not dealer
                else:
                    #Update player info
                    self.player_info[loser_index].lose+=1
                    self.player_info[winner_index].win+=1

                    player_money[loser_index].text = str(int(player_money[loser_index].text)-(base+tai*(int(self.amount_of_tai.text))))
                    player_money[winner_index].text = str(int(player_money[winner_index].text)+(base+tai*(int(self.amount_of_tai.text))))


        #Change the dealer state
        if winner_index != dealer_index:
            #Dealer has changed
            dealer[dealer_index].text = ""
            #It is at the last person of the round
            if dealer_index+1 > 3:
                #This check if the current round is at N or not
                if self.current_round == 3:
                    print("FINISH")
                    
                    #Start animation
                    self.anim_player_color.start(background[dealer_index])
                    self.anim_round.start(round[self.current_round])
                    self.finish_button.start(self.ids.finish_button)
                else:
                    dealer[0].text = "0"
                    background[dealer_index].player_color = (1,1,1,1)
                    background[0].player_color = (.2,.3,.1,.3)

                    round[self.current_round].round_color = (1,1,1,1)
                    self.current_round+=1
                    round[self.current_round].round_color = (.2,.3,.1,.6)
            else:
                dealer[dealer_index+1].text = "0"
                background[dealer_index].player_color = (1,1,1,1)
                background[dealer_index+1].player_color = (.2,.3,.1,.3)
        else:
            #Increase dealer count
            dealer[dealer_index].text = str(int(dealer[dealer_index].text)+1)
        #amount of money is empty after pressing submit button
        self.amount_of_tai.text = ""
        self.total_round += 1

        #Update the current state in the database
        #add one row of record
        self.update_current_state()
        self.parent.record.update()
        self.parent.record.add_record()

        #Set the default toggle button state back
        #If self touch is pressed (loser_index == None)
        if loser_index == None:
            self.self_touch.state = "normal"
        else:
            loser[loser_index].state = "normal"
        winner[winner_index].state = "normal"

    def stop_animation(self):
        self.anim_player_color.stop(self.player_four_background)
        self.anim_round.stop(self.round_N)
        self.finish_button.stop(self.ids.finish_button)

    def update_current_state(self):
        player_money = [self.player_one_money, self.player_two_money, self.player_three_money, self.player_four_money]
        winner = [self.winner_one, self.winner_two, self.winner_three, self.winner_four]
        loser = [self.loser_one, self.loser_two, self.loser_three, self.loser_four]
        dealer = [self.dealer_one, self.dealer_two, self.dealer_three, self.dealer_four]
        background = [self.player_one_background, self.player_two_background, self.player_three_background, self.player_four_background]
        round = [self.round_E, self.round_S, self.round_W, self.round_N]

        winner_index = None
        loser_index = None
        dealer_index = None

        #Find the index of the dealer
        #dealer_index is the index of the dealer
        for index, dealers in enumerate(dealer):
            if dealers.text != "":
                dealer_index = index
        
        #Find the winner index
        for index, winners in enumerate(winner):
            if winners.state == "down":
                    winner_index = index
        
        #Find the loser index
        for index, losers in enumerate(loser):
            if losers.state == "down":
                    loser_index = index
        #update current state
        
        #Update total round
        self.current_state["total_round"] = self.total_round

        #Update dealer_index, winner_index, loser_index
        
        #Update current state
        #Update winner,loser,dealer index
        self.current_state["winner_index"] = winner_index
        self.current_state["loser_index"] = loser_index


        #Winner, loser, dealer index are updated in submit_button()

        #update player color
        self.current_state["player0_background_color"] = background[0].player_color
        self.current_state["player1_background_color"] = background[1].player_color
        self.current_state["player2_background_color"] = background[2].player_color
        self.current_state["player3_background_color"] = background[3].player_color

        #update dealer count
        self.current_state['player0_dealer_count'] = dealer[0].text
        self.current_state['player1_dealer_count'] = dealer[1].text
        self.current_state['player2_dealer_count'] = dealer[2].text
        self.current_state['player3_dealer_count'] = dealer[3].text

        #update player money
        self.current_state['player0_money_difference'] = str(int(player_money[0].text)-int(self.previous_state['player0_money']))
        self.current_state['player1_money_difference'] = str(int(player_money[1].text)-int(self.previous_state['player1_money']))
        self.current_state['player2_money_difference'] = str(int(player_money[2].text)-int(self.previous_state['player2_money']))
        self.current_state['player3_money_difference'] = str(int(player_money[3].text)-int(self.previous_state['player3_money']))

        #update current round background color (E S W N)
        self.current_state['round_E_background_color'] = round[0].round_color
        self.current_state['round_S_background_color'] = round[1].round_color
        self.current_state['round_W_background_color'] = round[2].round_color
        self.current_state['round_N_background_color'] = round[3].round_color
    
        #This dealer index is the new dealer index
        #Have to offset the change
        #When dealer_index changes the round is still count as previous dealer round
        if self.previous_state["dealer_index"]!=dealer_index:
            self.current_state["dealer_index"] = self.previous_state["dealer_index"]

        #If dealer wins, dealer_index will remain the same
        else:
            self.current_state["dealer_index"] = dealer_index

    
    def update_previous_state(self):
        player_money = [self.player_one_money, self.player_two_money, self.player_three_money, self.player_four_money]
        winner = [self.winner_one, self.winner_two, self.winner_three, self.winner_four]
        loser = [self.loser_one, self.loser_two, self.loser_three, self.loser_four]
        dealer = [self.dealer_one, self.dealer_two, self.dealer_three, self.dealer_four]
        background = [self.player_one_background, self.player_two_background, self.player_three_background, self.player_four_background]
        round = [self.round_E, self.round_S, self.round_W, self.round_N]

        winner_index = None
        loser_index = None
        dealer_index = None

        #Find the index of the dealer
        #dealer_index is the index of the dealer
        for index, dealers in enumerate(dealer):
            if dealers.text != "":
                dealer_index = index
                dealer_tai = 2*int(dealer[index].text)+1
        
        #Find the winner index
        for index, winners in enumerate(winner):
            if winners.state == "down":
                    winner_index = index
        
        #Find the loser index
        for index, losers in enumerate(loser):
            if losers.state == "down":
                    loser_index = index
        #update previous state
        
        #Update total round
        self.previous_state["total_round"] = self.total_round

        #Update dealer_index, winner_index, loser_index
        
        #Update previous state
        #Update winner,loser,dealer index
        self.previous_state["winner_index"] = winner_index
        self.previous_state["loser_index"] = loser_index
        self.previous_state["dealer_index"] = dealer_index

        #Winner, loser, dealer index are updated in submit_button()

        #update player color
        self.previous_state["player0_background_color"] = background[0].player_color
        self.previous_state["player1_background_color"] = background[1].player_color
        self.previous_state["player2_background_color"] = background[2].player_color
        self.previous_state["player3_background_color"] = background[3].player_color

        #update dealer count
        self.previous_state['player0_dealer_count'] = dealer[0].text
        self.previous_state['player1_dealer_count'] = dealer[1].text
        self.previous_state['player2_dealer_count'] = dealer[2].text
        self.previous_state['player3_dealer_count'] = dealer[3].text

        #update player money
        self.previous_state['player0_money'] = player_money[0].text
        self.previous_state['player1_money'] = player_money[1].text
        self.previous_state['player2_money'] = player_money[2].text
        self.previous_state['player3_money'] = player_money[3].text

        #update current round background color (E S W N)
        self.previous_state['round_E_background_color'] = round[0].round_color
        self.previous_state['round_S_background_color'] = round[1].round_color
        self.previous_state['round_W_background_color'] = round[2].round_color
        self.previous_state['round_N_background_color'] = round[3].round_color
    
    def undo_button_pressed(self):
        player_money = [self.player_one_money, self.player_two_money, self.player_three_money, self.player_four_money]
        winner = [self.winner_one, self.winner_two, self.winner_three, self.winner_four]
        loser = [self.loser_one, self.loser_two, self.loser_three, self.loser_four]
        dealer = [self.dealer_one, self.dealer_two, self.dealer_three, self.dealer_four]
        background = [self.player_one_background, self.player_two_background, self.player_three_background, self.player_four_background]
        round = [self.round_E, self.round_S, self.round_W, self.round_N]
        
        if dealer[0].text == "0" and self.current_round!=0:
            self.current_round -= 1

        background[0].player_color = self.previous_state["player0_background_color"]
        background[1].player_color = self.previous_state["player1_background_color"]
        background[2].player_color = self.previous_state["player2_background_color"]
        background[3].player_color = self.previous_state["player3_background_color"]

        #update dealer count
        dealer[0].text = self.previous_state['player0_dealer_count']
        dealer[1].text = self.previous_state['player1_dealer_count'] 
        dealer[2].text = self.previous_state['player2_dealer_count']
        dealer[3].text = self.previous_state['player3_dealer_count']

        #update player money
        player_money[0].text = self.previous_state['player0_money']
        player_money[1].text = self.previous_state['player1_money']
        player_money[2].text = self.previous_state['player2_money']
        player_money[3].text = self.previous_state['player3_money']

        #update current round background color (E S W N)
        round[0].round_color = self.previous_state['round_E_background_color']
        round[1].round_color = self.previous_state['round_S_background_color']
        round[2].round_color = self.previous_state['round_W_background_color']
        round[3].round_color = self.previous_state['round_N_background_color']

        self.parent.record.remove_row()










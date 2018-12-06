# -*- coding: UTF-8 -*-
import random
import sys
import time
import os

slow = False
inning = 0 #inning number
appearances = 0#number of total plate appearances
out = 0 #number of outs
game_tally = 0
#0=no runners, 1 = 1st, 2 = 2nd, 4 = 3rd; --(3 = 1st and 2nd, 5 = 1st and 3rd, 6 = 2nd and 3rd, 7 = bases loaded)--
runners = 0 #runners on base
hit = 0 #0 = out, 1 = single, 2 = double, 3 = triple, 4 = homerun
hit_total = 0 #number of hit in entire game
runs = 0    #runs scored during game
delay = 0.5 #delay of state operations (seconds)
seed = random.randint(0,10000000) #number for seeding random number generator
curr_runs = 0
inning_arr = ['-','-','-','-','-','-','-','-','-','-','-']

hit_type = {0: """
   ____        __  __
  / __ \__  __/ /_/ /
 / / / / / / / __/ / 
/ /_/ / /_/ / /_/_/  
\____/\__,_/\__(_)   
                     
""",
1:"""
   _____ _             __     __
  / ___/(_)___  ____ _/ /__  / /
  \__ \/ / __ \/ __ `/ / _ \/ / 
 ___/ / / / / / /_/ / /  __/_/  
/____/_/_/ /_/\__, /_/\___(_)   
             /____/             
""",
2:"""
    ____              __    __     __
   / __ \____  __  __/ /_  / /__  / /
  / / / / __ \/ / / / __ \/ / _ \/ / 
 / /_/ / /_/ / /_/ / /_/ / /  __/_/  
/_____/\____/\__,_/_.___/_/\___(_)   
                                     
""",
3:"""
  ______     _       __     __
 /_  __/____(_)___  / /__  / /
  / / / ___/ / __ \/ / _ \/ / 
 / / / /  / / /_/ / /  __/_/  
/_/ /_/  /_/ .___/_/\___(_)   
          /_/                 
""",
4:"""
    __  __                        ____              __
   / / / /___  ____ ___  ___     / __ \__  ______  / /
  / /_/ / __ \/ __ `__ \/ _ \   / /_/ / / / / __ \/ / 
 / __  / /_/ / / / / / /  __/  / _, _/ /_/ / / / /_/  
/_/ /_/\____/_/ /_/ /_/\___/  /_/ |_|\__,_/_/ /_(_)   
                                                      
""", 
5:"""
    ____                                    ____        ____     __
   / __ )____ _________     ____  ____     / __ )____ _/ / /____/ /
  / __  / __ `/ ___/ _ \   / __ \/ __ \   / __  / __ `/ / / ___/ / 
 / /_/ / /_/ (__  )  __/  / /_/ / / / /  / /_/ / /_/ / / (__  )_/  
/_____/\__,_/____/\___/   \____/_/ /_/  /_____/\__,_/_/_/____(_)   
                                                                   
"""}
#runners_loc = {0: "Nobody on", 1: "Runner on 1st", 2: "Runner on 2nd", 3: "Runners on 1st and 2nd", 4: "Runner on 3rd", 5: "Runners on 1st and 3rd", 6: "Runners on 2nd and 3rd", 7: "Bases loaded"}
runners_loc = {0: """
             [ ]
         , '      ' ,
     , '              ' ,
  [ ]                    [ ]
     ' ,              , '
         ' ,      , ' 
              H""", 
                1: """
             [ ]
         , '      ' ,
     , '              ' ,
  [ ]                    [R]
     ' ,              , '
         ' ,      , ' 
              H""", 
                2: """
              [R]
         , '      ' ,
     , '              ' ,
  [ ]                    [ ]
     ' ,              , '
         ' ,      , ' 
              H""", 
                3: """
              [R]
         , '      ' ,
     , '              ' ,
  [ ]                    [R]
     ' ,              , '
         ' ,      , ' 
              H""", 
                4: """
             [ ]
         , '      ' ,
     , '              ' ,
  [R]                    [ ]
     ' ,              , '
         ' ,      , ' 
              H""", 
                5: """
             [ ]
         , '      ' ,
     , '              ' ,
  [R]                    [R]
     ' ,              , '
         ' ,      , ' 
              H""", 
                6: """
             [R]
         , '      ' ,
     , '              ' ,
  [R]                    [ ]
     ' ,              , '
         ' ,      , ' 
              H""", 
                7: """
             [R]
         , '      ' ,
     , '              ' ,
  [R]                    [R]
     ' ,              , '
         ' ,      , ' 
              H"""}


class State(object):
    def __init__(self,FSM):
        self.FSM = FSM
    def Enter(self):
        pass
    def Execute(self):
        pass
    def Exit(self):
        pass


class FSM(object):
    def __init__(self):
        self.transitions = {}
        self.states = {}
        self.curState = None
        self.prevState = None
        self.trans = None
    
    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition
    
    def AddState(self, stateName, state):
        self.states[stateName] = state
    
    def SetState(self, stateName):
        self.prevState = self.curState
        self.curState = self.states[stateName]

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]

    def Execute(self):
        if(self.trans):
            self.curState.Exit()
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.curState.Enter()
            self.trans = None
        self.curState.Execute()

Char = type("Char",(object,),{})

class Simulation(Char):
    def __init__(self):

        self.FSM = FSM()

        self.FSM.AddState("New_Inning", New_Inning(self.FSM))
        self.FSM.AddState("At_Bat", At_Bat(self.FSM))
        self.FSM.AddState("Determine_Hit", Determine_Hit(self.FSM))
        self.FSM.AddState("Determine_Runners", Determine_Runners(self.FSM))
        self.FSM.AddState("R0", R0(self.FSM))
        self.FSM.AddState("R1", R1(self.FSM))
        self.FSM.AddState("R2", R2(self.FSM))
        self.FSM.AddState("R3", R3(self.FSM))
        self.FSM.AddState("R4", R4(self.FSM))
        self.FSM.AddState("R5", R5(self.FSM))
        self.FSM.AddState("R6", R6(self.FSM))
        self.FSM.AddState("R7", R7(self.FSM))

        self.FSM.AddTransition("toNew_Inning", Transition("New_Inning"))
        self.FSM.AddTransition("toAt_Bat", Transition("At_Bat"))
        self.FSM.AddTransition("toDetermine_Hit", Transition("Determine_Hit"))
        self.FSM.AddTransition("toDetermine_Runners", Transition("Determine_Runners"))
        self.FSM.AddTransition("toR0", Transition("R0"))
        self.FSM.AddTransition("toR1", Transition("R1"))
        self.FSM.AddTransition("toR2", Transition("R2"))
        self.FSM.AddTransition("toR3", Transition("R3"))
        self.FSM.AddTransition("toR4", Transition("R4"))
        self.FSM.AddTransition("toR5", Transition("R5"))
        self.FSM.AddTransition("toR6", Transition("R6"))
        self.FSM.AddTransition("toR7", Transition("R7"))

        self.FSM.SetState("New_Inning")
    
    def Execute(self):
        self.FSM.Execute()



class Transition(object):
    def __init__(self,toState):
        self.toState = toState

    def Execute(self):
        pass
        #print("Transitioning...")


class Batter():
    def __init__(self):
        self.batting_average = 0
        self.num_hits = 0
        self.num_singles = 0
        self.num_doubles = 0
        self.num_triples = 0
        self.num_homeruns = 0
        self.num_plate_appearances = 0
        self.num_walks = 0
        self.num_strikeouts = 0
        self.num_sac_flies = 0
        self.player_name = ""
    
    def single_probability(self):
        return self.num_singles/self.num_plate_appearances
    def double_probability(self):
        return self.num_doubles/self.num_plate_appearances
    def triple_probability(self):
        return self.num_triples/self.num_plate_appearances
    def homerun_probability(self):
        return self.num_homeruns/self.num_plate_appearances
    def walk_probability(self):
        return self.num_walks/self.num_plate_appearances

    def setStats(self,name,appearances,hits,doubles,triples,homeruns,walks):
        self.player_name = name
        self.num_hits = hits
        self.num_doubles = doubles
        self.num_triples = triples
        self.num_homeruns = homeruns
        self.num_plate_appearances = appearances
        self.num_singles = hits - doubles - triples - homeruns
        self.num_walks = walks


class New_Inning(State):
    def __init__(self, FSM):
        super(New_Inning,self).__init__(FSM)

    def Enter(self):
        super(New_Inning,self).Enter()

    def Execute(self):
        self.FSM.ToTransition("toAt_Bat")

    def Exit(self):
        global inning, out , runners, hit_total, game_tally, curr_runs, inning_arr
        inning += 1
        out = 0
        runners = 0
        curr_runs = runs
        if(inning ==10):
            game_tally += 1
            print(f"---- BALL GAME #{game_tally} ---- \nTotal Hits: {hit_total}  \n Total Runs: {runs}")
        if slow and inning != 10:
            print("\n---- inning #", inning, "----\n")
            print("---------------------------------------------")
            print("| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | H | R |")
            print("---------------------------------------------")
            for i in range (9):
                print(f"| {inning_arr[i]} ", end ="")
            print(f"| {hit_total} | {runs} |")
            print("---------------------------------------------")

class At_Bat(State):
    def __init__(self, FSM):
        super(At_Bat,self).__init__(FSM)
    def Enter(self):
        super(At_Bat,self).Enter()
        if slow:
            print(f"\n {runners_loc[runners]}\n_______________________________")
    def Execute(self):
        global appearances, curr_runs, out, inning_arr
        if slow and inning != 10:
            print("outs:", out)
        if(out ==3):
            inning_arr[inning-1] = runs-curr_runs
            appearances = appearances - 1
            self.FSM.ToTransition("toNew_Inning")
        else:
            self.FSM.ToTransition("toDetermine_Hit")
    def Exit(self):
        global appearances
        appearances += 1

class Determine_Hit(State):
    def __init__(self, FSM):
        super(Determine_Hit, self).__init__(FSM)
    def Enter(self):
        global hit, hit_total
        b = lineup[determine_curr_batter()]
        if slow:
            print(f"Now batting: {b.player_name}")
        rand = random.randint(0,99)
        #print(b.single_probability(), " ", b.double_probability(), " ", b.triple_probability(), " ", b.homerun_probability())
        #print(rand)
        if rand < b.single_probability()*100:
            hit = 1
        elif rand < (b.double_probability()+b.single_probability())*100:
            hit = 2
        elif rand < (b.single_probability()+b.double_probability() + b.triple_probability())*100:
            hit = 3
        elif rand < (b.single_probability()+b.double_probability() + b.triple_probability() + b.homerun_probability())*100:
            hit = 4
        elif rand < (b.single_probability()+b.double_probability() + b.triple_probability() + b.homerun_probability() + b.walk_probability())*100:
            hit = 5
        else:
            hit = 0
        if hit != 0 and hit != 5:
            hit_total += 1
        super(Determine_Hit,self).Enter()
    def Execute(self):
        global out, hit, hit_type
        if slow:
            print(f'\n{hit_type[hit]}')
        if hit == 0:
            out += 1
            self.FSM.ToTransition("toAt_Bat")
        else:
            self.FSM.ToTransition("toDetermine_Runners")
    def Exit(self):
        pass

class Determine_Runners(State):
    def __init__(self,FSM):
        super(Determine_Runners,self).__init__(FSM)
    def Enter(self):
        super(Determine_Runners,self).Enter()
    def Execute(self):
        global runners, runners_loc
        if runners == 0:
            self.FSM.ToTransition("toR0")
            #runner0
        elif runners == 1:
            #runner1
            self.FSM.ToTransition("toR1")
        elif runners == 2:
            #runner2
            self.FSM.ToTransition("toR2")
        elif runners == 3:
            #runner3
            self.FSM.ToTransition("toR3")
        elif runners == 4:
            #runner4
            self.FSM.ToTransition("toR4")
        elif runners == 5:
            #runner5
            self.FSM.ToTransition("toR5")
        elif runners == 6:
            #runner6
            self.FSM.ToTransition("toR6")
        elif runners == 7:
            #runner7
            self.FSM.ToTransition("toR7")           
    def Exit(self):
        pass


class R0(State):
    def __init__(self,FSM):
        super(R0,self).__init__(FSM)
    def Enter(self):
        super(R0,self).Enter()
    def Execute(self):
        global runners, runs, hit, runners_loc
        if hit == 4:
            runs += 1
        elif hit == 3:
            runners = 4
        elif hit == 5:
            runners = 1
        else:
            runners = hit
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self):
        pass

class R1(State):
    def __init__(self,FSM):
        super(R1,self).__init__(FSM)
    def Enter(self):
        super(R1,self).Enter()
    def Execute(self):
        global runners, runs, hit, runners_loc
        if hit == 4:
            runs += 2
            runners = 0
        elif hit == 3:
            runs += 1
            runners = 4
        elif hit == 2:
            runs += 1
            runners = 2
        elif hit == 1:
            runners = 3
        elif hit == 5:
            runners = 3
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self):
        pass

class R2(State):
    def __init__(self,FSM):
        super(R2,self).__init__(FSM)
    def Enter(self):
        super(R2,self).Enter()
    def Execute(self):
        global runners, runs, hit, runners_loc
        if hit == 4:
            runs += 2
            runners = 0
        elif hit == 3:
            runs += 1
            runners = 4
        elif hit == 2:
            runners = 2
            runs += 1
        elif hit == 1:
            runners = 1
            runs += 1
        elif hit == 5:
            runners = 3
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self): 
        pass

class R4(State):
    def __init__(self,FSM):
        super(R4,self).__init__(FSM)
    def Enter(self):
        super(R4,self).Enter()
    def Execute(self):
        global runners, runs, hit, runners_loc
        if hit == 4:
            runs += 2
            runners = 0
        elif hit == 3:
            runs += 1
            runners = 4
        elif hit == 5:
            runners = 5
        else:
            runners = hit
            runs += 1
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self):
        pass

class R3(State):
    def __init__(self,FSM):
        super(R3,self).__init__(FSM)
    def Enter(self):
        super(R3,self).Enter()
    def Execute(self):
        global runners, runs, hit, runners_loc
        if hit == 4:
            runs += 3
            runners = 0
        elif hit == 3:
            runs += 2
            runners = 4
        elif hit == 2:
            runners = 6
            runs += 1
        elif hit == 1:
            runners = 5
            runs += 1
        elif hit == 5:
            runners = 7
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self):
        pass

class R5(State):
    def __init__(self,FSM):
        super(R5,self).__init__(FSM)
    def Enter(self):
        super(R5,self).Enter()
    def Execute(self):
        global runners, runs, hit, runners_loc
        if hit == 4:
            runs += 3
            runners = 0
        elif hit == 3:
            runs += 2
            runners = 4
        elif hit == 2:
            runners = 2
            runs += 2
        elif hit == 1:
            runners = 3
            runs += 1
        elif hit == 5:
            runners = 7
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self):
        pass

class R6(State):
    def __init__(self,FSM):
        super(R6, self).__init__(FSM)
    def Enter(self):
        super(R6,self).Enter()
    def Execute(self):
        global runners, runs,  hit, runners_loc
        if hit == 4:
            runs+= 3
            runners = 0
        elif hit == 3:
            runs += 2
            runners = 4
        elif hit == 2:
            runs += 2
            runners = 2
        elif hit == 1:
            runs += 2
            runners = 1
        elif hit == 5:
            runners = 7
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self):
        pass

class R7(State):
    def __init__(self,FSM):
        super(R7, self).__init__(FSM)
    def Enter(self):
        super(R7,self).Enter()
    def Execute(self):
        global runners, runs, hit, runners_loc
        if hit == 4:
            runs += 4
            runners = 0
        elif hit == 3:
            runs += 3
            runners = 4
        elif hit == 2:
            runs += 2
            runners = 6
        elif hit == 1:
            runs += 2
            runners = 1
        elif hit == 5:
            runs += 1
            runners = 7
        self.FSM.ToTransition("toAt_Bat")
    def Exit(self):
        pass

def import_stats(self, file):
    global lineup
    lineup_txt = []
    input_file = open(file)
    input_file.readline()
    for i in range (0, 9):
        lineup_txt.append(input_file.readline().split(','))
        i += 1
    #print(lineup_txt)

    counter = 0
    for a in self:
        a.setStats(lineup_txt[counter][2],int(lineup_txt[counter][5]),int(lineup_txt[counter][8]),int(lineup_txt[counter][9]),int(lineup_txt[counter][10]),int(lineup_txt[counter][11]), int(lineup_txt[counter][15]))
        #print(counter)
        #print(lineup_txt[counter][2],int(lineup_txt[counter][4]),int(lineup_txt[counter][5]),int(lineup_txt[counter][6]),int(lineup_txt[counter][7]),int(lineup_txt[counter][8]))
        counter += 1
        
def determine_curr_batter():
    global appearances
    return appearances % 9

def print_curr_batter_info():
    player_number = determine_curr_batter()
    if slow:
        print(lineup[player_number].player_name)

def choose_csv():
    file_dir = os.listdir('./')
    roster_arr = []
    for filename in file_dir:
        if 'csv' in filename:
            roster_arr.append(filename)
    for i, filename in enumerate(roster_arr):
        print(f"{i} :: {filename}")
    while 1:
        choice = int(input("Choose file: "))
        if choice < 0 or choice >= len(roster_arr):
            print("invalid selection!")
        else:
            return roster_arr[choice]


        
#TODO:
# walks/HBP, more accurate baserunning
b1 = Batter() #batter instance
b2 = Batter() #batter instance
b3 = Batter() #batter instance
b4 = Batter() #batter instance
b5 = Batter() #batter instance
b6 = Batter() #batter instance
b7 = Batter() #batter instance
b8 = Batter() #batter instance
b9 = Batter() #batter instance
 
lineup = [b1,b2,b3,b4,b5,b6,b7,b8,b9]


file_name = choose_csv()
random.seed(seed)
if __name__ == '__main__':
    while 1:
        num_games = int (input('How many games would you like to simulate?'))
        if(num_games > 0):
            break
        else:
            print('Number of games must be more than 0')
    while 1:
        speed = input('Would you like to view individual game stats?(y/n)')
        if(speed == "y" or speed == "Y"):
            slow = True
            break
        elif(speed == "n" or speed == "N"):
            break
        else:
            print('Must answer (y)es or (n)o: ')


    import_stats(lineup, file_name)
    for i in range(num_games):
        print("---- PLAY BALL ----")
        s = Simulation()
        #b1.setStats(196,48,1,33,629)
        while inning < 10:
            if slow:
                time.sleep(delay)
            s.Execute()
        inning = 0
    print(f'Number of games simulated: {game_tally}')
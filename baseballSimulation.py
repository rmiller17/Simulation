import random
import sys
import time

out = 0
inning = 0
#0=no runners, 1 = 1st, 2 = 2nd, 4 = 3rd; --(3 = 1st and 2nd, 5 = 1st and 3rd, 6 = 2nd and 3rd, 7 = bases loaded)--
runners = 0
hit = 0 #0 = out, 1 = single, 2 = double, 3 = triple, 4 = homerun
hit_total = 0
runs = 0


delay = 0.5 #seconds
seed = 13


hit_type = {0: "Out",1:"Single",2:"Double",3:"Triple",4:"Home Run"}
runners_loc = {0: "Nobody on", 1: "Runner on 1st", 2: "Runner on 2nd", 3: "Runners on 1st and 2nd", 4: "Runner on 3rd", 5: "Runners on 1st and 3rd", 6: "Runners on 2nd and 3rd", 7: "Bases loaded"}

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
        self.FSM.AddState("Increment_Inning", Increment_Inning(self.FSM))
        self.FSM.AddState("Determine_Hit", Determine_Hit(self.FSM))
        self.FSM.AddState("Determine_Runners", Determine_Runners(self.FSM))
        self.FSM.AddState("R0", R0(self.FSM))
        self.FSM.AddState("R1", R1(self.FSM))
        self.FSM.AddState("R2", R2(self.FSM))
        self.FSM.AddState("R3", R3(self.FSM))
        self.FSM.AddState("R4", R4(self.FSM))

        self.FSM.AddTransition("toNew_Inning", Transition("New_Inning"))
        self.FSM.AddTransition("toIncrement_Inning", Transition("Increment_Inning"))
        self.FSM.AddTransition("toDetermine_Hit", Transition("Determine_Hit"))
        self.FSM.AddTransition("toDetermine_Runners", Transition("Determine_Runners"))
        self.FSM.AddTransition("toR0", Transition("R0"))
        self.FSM.AddTransition("toR1", Transition("R1"))
        self.FSM.AddTransition("toR2", Transition("R2"))
        self.FSM.AddTransition("toR3", Transition("R3"))
        self.FSM.AddTransition("toR4", Transition("R4"))
        
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
        self. num_strikeouts = 0
    
    def single_probability(self):
        return self.num_singles/self.num_plate_appearances
    def double_probability(self):
        return self.num_doubles/self.num_plate_appearances
    def triple_probability(self):
        return self.num_triples/self.num_plate_appearances
    def homerun_probability(self):
        return self.num_homeruns/self.num_plate_appearances

    def setStats(self,hits,doubles,triples,homeruns,appearances):
        self.num_hits = hits
        self.num_doubles = doubles
        self.num_triples = triples
        self.num_homeruns = homeruns
        self.num_plate_appearances = appearances
        self.num_singles = hits - doubles - triples - homeruns


class New_Inning(State):
    def __init__(self, FSM):
        super(New_Inning,self).__init__(FSM)

    def Enter(self):
        super(New_Inning,self).Enter()

    def Execute(self):
        self.FSM.ToTransition("toIncrement_Inning")

    def Exit(self):
        global inning, out , runners, hit_total
        inning += 1
        out = 0
        runners = 0
        if(inning ==10):
            print("---- BALL GAME ---- \nTotal Hits: ", hit_total)
            sys.exit()
        print("\n---- inning #", inning, "----\n")

class Increment_Inning(State):
    def __init__(self, FSM):
        super(Increment_Inning,self).__init__(FSM)
    def Enter(self):
        print(runners_loc[runners], "\nRuns:", runs)
        super(Increment_Inning,self).Enter()
    def Execute(self):
        global out
        print("outs:", out)
        if(out ==3):
            self.FSM.ToTransition("toNew_Inning")
        else:
            self.FSM.ToTransition("toDetermine_Hit")
    def Exit(self):
        pass

class Determine_Hit(State):
    def __init__(self, FSM):
        super(Determine_Hit, self).__init__(FSM)
    def Enter(self):
        global hit,  b, hit_total
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
        else:
            hit = 0
        if hit != 0:
            hit_total += 1
        super(Determine_Hit,self).Enter()
    def Execute(self):
        global out, hit, hit_type
        print(hit_type[hit])
        if hit == 0:
            out += 1
            self.FSM.ToTransition("toIncrement_Inning")
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
            self.FSM.ToTransition("toIncrement_Inning")
        elif runners == 6:
            #runner6
            self.FSM.ToTransition("toIncrement_Inning")
        elif runners == 7:
            #runner7
            self.FSM.ToTransition("toIncrement_Inning")           
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
        else:
            runners = hit
        self.FSM.ToTransition("toIncrement_Inning")
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
            runners = 6
        elif hit == 1:
            runners = 3
        self.FSM.ToTransition("toIncrement_Inning")
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
            runs += 2
        elif hit == 1:
            runners = 5
        self.FSM.ToTransition("toIncrement_Inning")
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
        else:
            runners = hit
            runs += 1
        self.FSM.ToTransition("toIncrement_Inning")
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
        self.FSM.ToTransition("toIncrement_Inning")
    def Exit(self):
        pass

#TODO
# R3, R5, R6, R7, walks/HBP, more accurate baserunning
b = Batter() #batter instance
random.seed(seed)
if __name__ == '__main__':
    print("---- PLAY BALL ----")
    s = Simulation()
    b.setStats(178,29,3,10,519)
    while True:
        time.sleep(delay)
        s.Execute()
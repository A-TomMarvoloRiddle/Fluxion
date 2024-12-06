import test.Test_3 as ul
#import test.RL as rl
import numpy as np
#ul.start_system("C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/North.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/South.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/East.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/West.mp4")
#t.Thread(target=ul.start_system, args=("C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/North.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/South.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/East.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/West.mp4")).start()
#t.Thread(target=ul.start_system, args=("C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/East.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/West.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/North.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/South.mp4")).start()

class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.state = "Red"  # Initial state
        self.duration = 0  # Initial duration
        self.vc=0 # Initial Vehicle Count        

    def set_state(self, state,duration = None):
        self.state = state
        self.duration=duration
        print(f">> {self.direction} >>> {self.state} >>> {self.duration} seconds" if self.state in ["Green", "Yellow"] else f"{self.direction} >> {self.state} >> {self.duration} seconds")

directions=[]

def create_junc(ndir):
    global directions
    d=np.arange(1,ndir+1)
    dl=list(map(lambda x:"d"+ str(x),d))
    print(dl)
    for dir in dl:
        directions.append(TrafficLight(dir))

def feeds(*args):
    for x in args:
        ul.start_system(x)


create_junc(3)
print(directions)
feeds("dfhdf","dfshdfshd","dfs","dshf")
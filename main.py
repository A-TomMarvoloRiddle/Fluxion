import test.vid_vc as vid
import test.RL as rl
import time

class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.state = "Red"  # Initial state
        self.duration = 0  # Initial duration
        self.vc=0 # Initial Vehicle Count      
        self.gt=0 #Inital Green Time
        self.rt=0 #Inital Red Time

    def set_state(self, state,duration = None):
        self.state = state
        self.duration=duration
        print(f">> {self.direction} >>> {self.state} >>> {self.duration} seconds" if self.state in ["Green", "Yellow"] else f"{self.direction} >> {self.state} >> {self.duration} seconds")

    def start_vid(self,path):
        vid.start_sys(path)

    def assign_vc(self): 
        self.vc= vid.get_vc()
        #return self.vc

directions={}
dl=[]

def create_junc(*args):
    i=1
    for path in args:
        directions[i]=TrafficLight(i)
        directions[i].start_vid(path)
        time.sleep(5)
        directions[i].assign_vc()
        i+=1
        self.gt=rl.update_green_time()


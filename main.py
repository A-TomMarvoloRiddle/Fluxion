import test.vid_vc as vid
import test.RL as rl
import time
import threading as t


class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.state = "Red"  # Initial state
        self.duration = 0  # Initial duration
        self.vc=0 # Initial Vehicle Count      
        self.gt=0 #Inital Green Time

    def set_state(self, state,duration = None):
        self.state = state
        self.duration=duration
        print(f">> {self.direction} >>> {self.state} >>> {self.duration} seconds" if self.state in ["Green", "Yellow"] else f"{self.direction} >> {self.state} >> {self.duration} seconds")

    def start_vid(self,i,path):
        vid.start_sys(i,path)

    def assign_vc(self): 
        self.vc= vid.get_vc()

    def get_vc(self):
        return self.vc

directions={}

def gcal():
    global directions
    gt=[]
    for d in directions:
        print("\n",d,"\n")
        vc=d.get_vc()
        d.gt=rl.update_green_time(vc)
        gt.append(d,d.gt,0)
    return gt

def rcal(temp):
    for i in range(1, len(temp)):
        temp[i][2] = sum(temp[j][1] + 5 for j in range(i))
    '''for d in directions:
        d.rt=(gt[i][2] for i in range(len(gt)))'''

def change_light(schedule):
    global direction
    while schedule:
        print(f"\nFinal Schedule: {schedule}\n")
        current = schedule[0]
        next_directions = schedule[1:4]

        directions[current[0]].set_state("Green", current[1])
        for dir in next_directions:
            directions[dir[0]].set_state("Red", dir[2])

        time.sleep(current[1])
        
        directions[current[0]].set_state("Yellow", 5)
        for dir in next_directions:
            dir[2]=dir[2]-current[1]
            directions[dir[0]].set_state("Red", dir[2])

        time.sleep(5)

        left=current[0].assign_vc()
        rl.update_penalty(left)

        schedule.pop(0)
        schedule=rcal(schedule)

        if current[0]==1:
            schedule.extend(gcal())
            schedule=rcal(schedule)

def create_junc(temp):
    global directions
    i=1
    for path in temp:
        directions[i]=TrafficLight(i)
        directions[i].start_vid(i,path)
        time.sleep(5)
        directions[i].assign_vc()
        i+=1
    #print(directions)

def start_system(paths):
    print("\n       FLUXION by ERROR 505\n")
    create_junc(paths)
    #time.sleep(5)
    schedule = gcal()
    schedule = rcal(schedule)
    print("\n",schedule,"\n")
    t.Thread(target=change_light, args=(schedule,)).start()

start_system(("C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/North.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/South.mp4","C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/East.mp4"))


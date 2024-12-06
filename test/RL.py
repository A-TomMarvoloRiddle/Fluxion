# Initialize data structures
historical_data = {}  # Stores last green time and penalty status for each vehicle count
penalty_free_counter = {}  # Tracks penalty-free cycles for specific vehicle counts
fixed_green_times = {}  # Stores fixed green times for specific vehicle counts
gt_history=[1][2]  #stores last vehicle count and its green time

# Function to update green time for a specific vehicle count
def update_green_time(x_new):
    global historical_data, penalty_free_counter, fixed_green_times, gt_
    penalty_adjustment = 2  # Increment/decrement for green time when penalty is received
    penalty_threshold = 3  # Number of penalty-free cycles needed to fix a green time
    # Check if x_new has a fixed green time
    if x_new in fixed_green_times:
        print(f"Using fixed green time for {x_new} vehicles: {fixed_green_times[x_new]} seconds")
        return fixed_green_times[x_new]
    
    # Get last vehicle count and last green time and penalty status for the given vehicle count
    x_old,t_old_gt,punishment_received=gt_history[-1][0],historical_data.get(x_new, {"last_gt": 10, "penalty": 1})

    # Calculate new green time based on the punishment condition
    if punishment_received==1:
        if x_new > x_old:  # Traffic increased, increase green time
            t_new_gt = t_old_gt + penalty_adjustment
        elif x_new < x_old:  # Traffic decreased, decrease green time
            t_new_gt = max(5, t_old_gt - penalty_adjustment)  # Ensure minimum green time
        else:  # Traffic unchanged
            t_new_gt = t_old_gt
        # Reset penalty-free counter since a penalty was received
        penalty_free_counter[x_new] = 0
    elif punishment_received==-1:
        t_new_gt = t_old_gt-1
        # Reset penalty-free counter since a penalty was received
        penalty_free_counter[x_new] = 0
    else:
        # Keep the green time unchanged        
        t_new_gt=t_old_gt
        # No penalty received, increment penalty-free counter
        penalty_free_counter[x_new] = penalty_free_counter.get(x_new, 0) + 1
        # Check if penalty-free for the required threshold cycles
        if penalty_free_counter[x_new] >= penalty_threshold:
            fixed_green_times[x_new] = t_old_gt
            print(f"Fixed green time set for {x_new} vehicles: {t_old_gt} seconds")

    #print(f"Updated green time for {vehicle_count} vehicles: {t_new_gt} seconds")
    
    gt_history[-1]=x_new,t_new_gt  #storing current cycle's vehicle count and green time
    historical_data[x_new]["last_gt"]=t_new_gt #storing current cycle's green time for specified vc
    return t_new_gt

def update_penalty(vehicle_count):
    global historical_data
    vc_threshold=5  # Threshold for vehicle count to trigger penalty
    if vehicle_count > vc_threshold:
        punish=1
    elif vehicle_count < vc_threshold/2:
        punish=-1
    else:
        punish=0
    historical_data[vehicle_count]["penalty"]=punish
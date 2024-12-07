data = {}  # Stores last green time and penalty status for each vehicle count
prev_cycle = [0]*2  # stores last vehicle count and its green time

def update_green_time(curr_vc):
    global data
    print("\n Update prev_cycle", prev_cycle, "\n")
    print("\n Update curr_vc", curr_vc, "\n")
    max_vc=60
    if curr_vc>(2*max_vc)//3:
        factor=1.5
    elif curr_vc<max_vc//3:
        factor=.5
    else:
        factor=1
    

    # Get last vehicle count and last green time and penalty status for the given vehicle count
    data_prev = data[curr_vc] = {"last_gt": 10,"penalty": 1}  if curr_vc not in data else data.get(curr_vc)
    last_gt = data_prev["last_gt"]
    penalty = data_prev["penalty"]
    prev_vc, perv_gt, penalty = prev_cycle[0], last_gt, penalty

    # Calculate new green time based on the punishment condition
    if penalty == 1:
        if curr_vc > prev_vc:  # Traffic increased, increase green time
            delta_gt = (factor * (curr_vc - prev_vc))//1
            curr_gt = min(50, perv_gt + delta_gt)
        elif curr_vc < prev_vc:  # Traffic decreased, decrease green time
            delta_gt = (factor * (prev_vc - curr_vc))//1
            curr_gt = max(5, perv_gt - delta_gt)  # Ensure minimum green time
        else:  # Traffic unchanged
            curr_gt = perv_gt
    elif penalty == -1:
        curr_gt = max(5, perv_gt - 1)
    else:
        # Keep the green time unchanged
        curr_gt = perv_gt

    prev_cycle[0],prev_cycle[1] = curr_vc,curr_gt # storing current cycle's vehicle count and green time
    data[curr_vc] = {"last_gt": curr_gt,"penalty": penalty}  # storing current cycle's green time for specified vc, 0 is for no significance
    print("\n Update Data", data, "\n")
    return curr_gt

def update_penalty(left_vc):
    global data
    vc_threshold = 5  # Threshold for vehicle count to trigger penalty

    # Check if vehicle_count exists in historical_data
    if left_vc not in data:
        # Initialize with a default value if vehicle_count does not exist
        data[left_vc] = {"last_gt": 10,"penalty": 1}  # Set appropriate default values for other keys

    if left_vc > vc_threshold:
        punish = 1
    elif left_vc < vc_threshold // 2:
        punish = -1
    else:
        punish = 0
    data[left_vc]["penalty"] = punish
    print("\nPenalty Historical", data, "\n")

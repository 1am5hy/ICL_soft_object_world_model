import os
import subprocess

names_agent = [
    "agent0", 
    "agent1_norl", 
    "agent1_withrl", 
    "agent2_norl", 
    "agent2_withrl", 
    "agent5_norl", 
    "agent5_withrl", 
    "agent6_norl", 
    "agent6_withrl", 
]
names_dataset = [
    "reach_goal",
    "play_full",
    "play_stitch",
]

for d in names_dataset:
    for a in names_agent:
        for i in range(0,10,1):
            path_in = "./"+d+"/vid_"+a+"_seed_"+str(i)+".mp4"
            path_out = "./push_"+d+"_"+a+"_eval_"+str(i)+".mp4"
            cmd = "ffmpeg -i "+path_in+" -vcodec libx265 -crf 28 "+path_out
            print(cmd)
            os.system(cmd)


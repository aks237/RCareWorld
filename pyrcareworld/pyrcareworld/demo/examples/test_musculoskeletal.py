import json
from pyrcareworld.envs.musculoskeletal_env import MusculoskeletalEnv
import numpy as np
import cv2
import argparse
from pyrcareworld.utils.sample_joint_data import SampleData
from pyrcareworld.utils.musculoskeletal_solver import MusculoskeletalSolver
import time

def _main(use_graphics=False, dev=None):
    if use_graphics:
        text = """
        Testing musculoskeletal analysis using a controller object to control joints
        and solving for the drive forces they exert.
        """
        print(text) 
    
    # Initialize solver class and visualize with rerun
    solver = MusculoskeletalSolver(visualize=True)
    time.sleep(2)

    # Initialize object to stream sample data
    joint_data = SampleData()

    # Initialize the environment
    env = MusculoskeletalEnv(graphics=use_graphics) if dev == None else MusculoskeletalEnv(graphics=use_graphics, executable_file="@editor")
    print(env.attrs)

    person = env.get_person()
    person.EnabledNativeIK(False)
    env.step()

    step_pause = 2
    count = 1
    angles = [[0.0, 0.0, 0.0]] * 22
    update_torques = True

    while True:
        angle_dict = joint_data.get_next_frame()
        for joint in angle_dict.keys():
            angles[joint_data.joint_indices[joint]] = angle_dict[joint]
        
        # Introduce a pause to allow simulation to settle every time
        # the data is looped
        if joint_data.first_frame:
            print("\nLOOPING")
            person.SetJointPositionsEulerDirectly(angles)
            env.step(500)
            solver.initialized = False
            continue
        
        person.SetJointPositionsEuler(angles)
        env.step(step_pause)
        joint_data.index += step_pause - 1

        # Only update every 25 steps to avoid heavy lag
        if count % 25 == 0:
            person.UpdateTendonsToCurrent(update_torques)
            env.step()
            solver.update(person.data, update_torques)
        
        count += 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RCareWorld bathing environment simulation.')
    parser.add_argument('-g', '--graphics', action='store_true', help='Enable graphics')
    parser.add_argument('-d', '--dev', action='store_true', help='Run in developer mode')
    args = parser.parse_args()
    _main(use_graphics=args.graphics, dev=args.dev)

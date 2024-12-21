import pandas as pd
import numpy as np
import os

"""
Helper class to simulate livestreaming motion capture data from Unity.
Converts joint angle representations to Unity coordinates and loops through
frames from sample data to 'stream' it.
"""

class SampleData:
    def __init__(self, csv_file=os.path.join("raw_joint_data","Daniele003.csv")):
        self.csv_file = csv_file
        self.data = []
        self.joint_names = [
            "Pelvis", "Spine1", "Spine2", "Spine3", "Neck", "Head",
            "RightShoulder", "RightUpperArm", "RightLowerArm", "RightHand",
            "LeftShoulder", "LeftUpperArm", "LeftLowerArm", "LeftHand",
            "RightUpperLeg", "RightLowerLeg", "RightFoot", "RightToes",
            "LeftUpperLeg", "LeftLowerLeg", "LeftFoot", "LeftToes"
        ]

        self.joint_indices = {
                "Pelvis": 0,
                "LeftUpperLeg": 1,
                "LeftLowerLeg": 2,
                "LeftFoot": 3,
                "LeftToes": 4,
                "RightUpperLeg": 5,
                "RightLowerLeg": 6,
                "RightFoot": 7,
                "RightToes": 8,
                "Spine1": 9,
                "Spine2": 10,
                "Spine3": 11,
                "LeftShoulder": 12,
                "LeftUpperArm": 13,
                "LeftLowerArm": 14,
                "LeftHand": 15,
                "Neck": 16,
                "Head": 17,
                "RightShoulder": 18,
                "RightUpperArm": 19,
                "RightLowerArm": 20,
                "RightHand": 21
            }

        self.read_and_transform_data()
        self.frames = len(self.data)
        self.index = 0
        self.first_frame = True

    
    def get_next_frame(self):
        # loop back to first frame if reached last frame
        if self.index >= self.frames:
            self.first_frame = True
            self.index = 0
        elif self.index > 0:
            self.first_frame = False

        out = self.data[self.index]
        self.index += 1
        return out
        
        
    def read_and_transform_data(self):
        # Read CSV file
        df = pd.read_csv(self.csv_file)

        # Exclude 'Frame' column
        data_columns = df.columns[1:]

        # For each timestep, process the data
        for index, row in df.iterrows():
            # Extract the data columns
            data_row = row[1:].values  # Exclude 'Frame'

            # Arrange into 'angles' array (22x3)
            angles = np.zeros((22, 3))
            for i in range(22):
                angles[i, :] = data_row[i*3:(i+1)*3]

            # Perform transformations
            unity_eulers = self.transform_jointangles(angles)

            # Create a dictionary with joint names as keys and transformed angles as values
            timestep_data = {}
            for idx, joint_name in enumerate(self.joint_names):
                # Map joint index to unity_eulers index
                unity_euler_index = idx
                if unity_euler_index >= 4:
                    unity_euler_index += 1  # Skip index 4 (unity_eulers[4] is unused)

                euler_angles = unity_eulers[unity_euler_index]
                timestep_data[joint_name] = euler_angles.tolist()
            self.data.append(timestep_data)

    def transform_jointangles(self, angles):
        # Initialize unity_eulers as zeros (24x3)
        unity_eulers = np.zeros((24, 3))

        # Transformations as per MATLAB function
        # Pelvis
        pel = angles[0, :]  # angles(1,:)
        unity_eulers[0, :] = [0, -pel[2]-10, 0]

        # Right Hip
        rh = angles[14, :]  # angles(15,:)
        unity_eulers[15, :] = [rh[1], rh[2]-pel[2]-40, rh[0]]

        # Left Hip
        lh = angles[18, :]  # angles(19,:)
        unity_eulers[19, :] = [lh[1], lh[2]-pel[2]-40, -lh[0]]

        # Right Knee
        rk = angles[15, :]  # angles(16,:)
        unity_eulers[16, :] = [rk[2], 0, 0]

        # Left Knee
        lk = angles[19, :]  # angles(20,:)
        unity_eulers[20, :] = [lk[2], 0, 0]

        # Right Ankle
        ra = angles[16, :]  # angles(17,:)
        unity_eulers[17, :] = [ra[1], ra[2], -ra[0]]

        # Left Ankle
        la = angles[20, :]  # angles(21,:)
        unity_eulers[21, :] = [la[1], la[2], -la[0]]

        # Right Ball Foot
        rf = angles[17, :]  # angles(18,:)
        unity_eulers[18, :] = [rf[1], rf[2], -rf[0]]

        # Left Ball Foot
        lf = angles[21, :]  # angles(22,:)
        unity_eulers[22, :] = [lf[1], lf[2], -lf[0]]

        # Right T4 Shoulder
        rc = angles[6, :]  # angles(7,:)
        unity_eulers[7, :] = [-30 - rc[2], 0, 0]

        # Right Shoulder
        rs = angles[7, :]  # angles(8,:)
        unity_eulers[8, :] = [-rs[2], rs[1], rs[0]-90]

        # Right Elbow
        re = angles[8, :]  # angles(9,:)
        unity_eulers[9, :] = [-re[2], 0, 0]

        # Right Wrist
        rw = angles[9, :]  # angles(10,:)
        unity_eulers[10, :] = [-rw[2], rw[1], rw[0]]

        # Left T4 Shoulder
        lc = angles[10, :]  # angles(11,:)
        unity_eulers[11, :] = [30 + lc[2], 0, 0]

        # Left Shoulder
        ls = angles[11, :]  # angles(12,:)
        unity_eulers[12, :] = [ls[1], ls[2], -ls[0]+90]

        # Left Elbow
        le = angles[12, :]  # angles(13,:)
        unity_eulers[13, :] = [le[2], 0, 0]

        # Left Wrist
        lw = angles[13, :]  # angles(14,:)
        unity_eulers[14, :] = [lw[1], lw[2], -lw[0]]

        # Spine1
        s1 = angles[1, :]  # angles(2,:)
        unity_eulers[1, :] = [s1[2]-pel[2], 0, 0]

        # Spine2
        s2 = angles[2, :]  # angles(3,:)
        unity_eulers[2, :] = [s2[2], 0, 0]

        # Spine3
        s3 = angles[3, :]  # angles(4,:)
        unity_eulers[3, :] = [s3[2], 0, 0]

        # Neck
        n = angles[4, :]   # angles(5,:)
        unity_eulers[5, :] = [n[1], -n[2], -n[0]]

        # Head
        h = angles[5, :]   # angles(6,:)
        unity_eulers[6, :] = [h[2]-10, 0, 0]

        return unity_eulers

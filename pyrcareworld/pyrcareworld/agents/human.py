from pyrcareworld.objects import RCareWorldBaseObject
from typing import Optional


class Human(RCareWorldBaseObject):
    """
    Humans in RCareWorld
    """

    def __init__(self, env, id: int, name: str, is_in_scene: bool = False):
        super().__init__(env=env, id=id, name=name, is_in_scene=is_in_scene)
        self.name_list = [
            "Pelvis",
            "Spine1",
            "Spine2",
            "Spine3",
            "LeftShoulder",
            "LeftUpperArm",
            "LeftLowerArm",
            "LeftHand",
            "RightShoulder",
            "RightUpperArm",
            "RightLowerArm",
            "RightHand",
            "LeftUpperLeg",
            "LeftLowerLeg",
            "LeftFoot",
            "LeftToes",
            "RightUpperLeg",
            "RightLowerLeg",
            "RightFoot",
            "RightToes",
            "Neck",
            "Head",
            "LeftEye",
            "RightEye",
            "Jaw",
            "LeftThumb1",
            "LeftThumb2",
            "LeftThumb3",
            "LeftIndex1",
            "LeftIndex2",
            "LeftIndex3",
            "LeftMiddle1",
            "LeftMiddle2",
            "LeftMiddle3",
            "LeftRing1",
            "LeftRing2",
            "LeftRing3",
            "LeftPinky1",
            "LeftPinky2",
            "LeftPinky3",
            "RightThumb1",
            "RightThumb2",
            "RightThumb3",
            "RightIndex1",
            "RightIndex2",
            "RightIndex3",
            "RightMiddle1",
            "RightMiddle2",
            "RightMiddle3",
            "RightRing1",
            "RightRing2",
            "RightRing3",
            "RightPinky1",
            "RightPinky2",
            "RightPinky3",
        ]

        self.muscle_groups = {"NeckGroup": {},
                              "ShoulderGroup": {},
                              "ArmGroup": {},
                              "ForearmGroup": {},
                              "HipGroup": {},
                              "ThighGroup": {},
                              "LegGroup": {},
                              "FootGroup": {},
                              "TorsoGroup": {},
                              "ThoracicGroup": {},
                              "VertebralGroup": {},
                              "AbdomenGroup": {}
                              }
        
        self.groups_instantiated = False
        self.muscle_tendons = {}

    def get_activation_dict_all(self):
        """
        Function to return a dictionary of kv pairs 
        """
        if not self.groups_instantiated:
            data = self.env.instance_channel.data[self.id]
            #print(data)
            for group in self.muscle_groups.keys():
                group_data = data.get(group,None)
                if group_data:
                    for tendon in group_data.keys():
                        self.muscle_groups[group][tendon] = 0.0
                        self.muscle_tendons[tendon] = 0.0
                else:
                    print(group)
                    raise ValueError("Error retrieving data from Unity.")
            self.groups_instantiated = True
        
        return self.muscle_tendons

    def get_activation_dict_group(self,group: str):
        """
        Function to return a dictionary of kv pairs of muscles and activation
        constants of specified muscle group (all set to zero so user can modify with their own values)
        """
        if not self.groups_instantiated:
            self.get_activation_dict_all()
        if group in self.muscle_groups:
            return self.muscle_groups[group]
        else:
            raise ValueError(f"Unrecognized muscle group '{group}'.")

    def set_muscle_activation(self, muscle_name: str, activation: float):
        """
        Sets the activation of a single muscle tendon unit.

        Args:
            muscle_name: The name of the muscle tendon unit.
            activation: The activation value (0.0 to 1.0).
        """

        #print(muscle_name)
        self.env.instance_channel.set_action(
            "SetMuscleActivation",
            id=self.id,
            muscle_name=muscle_name,
            activation=activation,
        )

    def set_multiple_muscle_activations(self, activation_dict: dict):
        """
        Sets the activations of any group of muscle tendon units.

        Args:
            activation_dict: A dictionary mapping muscle names to activation values (0.0 to 1.0).
        """
        self.env.instance_channel.set_action(
            "SetMultipleMuscleActivations",
            id=self.id,
            activation_data=activation_dict,
        )

    def setBasePosition(self, position: list):
        print(type(self.env.instance_channel))
        self.env.instance_channel.set_action(
            "SetTransform", id=self.id, position=position
        )

    def setRootRotation(self, rotation: list):
        self.env.instance_channel.set_action(
            "SetTransform", id=self.id, rotation=rotation
        )

    def setJointRotationByName(self, joint_name: str, position: list):
        if joint_name not in self.name_list:
            raise ValueError("The joint name is not in the list")
        self.env.instance_channel.set_action(
            "SetNameBonePosition",
            id=self.id,
            bone_name=joint_name,
            bone_position=position[0],
            bone_position_y=position[1],
            bone_position_z=position[2],
        )

    def setJointLimits(
        self,
        joint_name: str,
        lower_limit: float,
        upper_limit: float,
        axis: Optional[str] = None,
    ):
        """
        Sets the joint limits for this human object in Unity.

        Args:
            joint_name: The name of the joint (or bone).
            lower_limit: The lower limit of the joint.
            upper_limit: The upper limit of the joint.
            axis: The axis of the joint. If None, all axes are set.
        """
        if joint_name not in self.name_list:
            raise ValueError("The joint name is not in the list")

        if (axis in ["X", "Y", "Z"]) is False:
            self.env.instance_channel.set_action(
                "SetJointLimits",
                id=self.id,
                bone_name=joint_name,
                lower_limit=lower_limit,
                upper_limit=upper_limit,
            )
        else:
            self.env.instance_channel.set_action(
                "SetJointLimits",
                id=self.id,
                bone_name=joint_name,
                lower_limit=lower_limit,
                upper_limit=upper_limit,
                axis=axis,
            )

    def setJointRotationByNameDirectly(self, joint_name: str, position: list):
        if joint_name not in self.name_list:
            raise ValueError("The joint name is not in the list")
        self.env.instance_channel.set_action(
            "SetNameBonePositionDirectly",
            id=self.id,
            bone_name=joint_name,
            bone_position=position[0],
            bone_position_y=position[1],
            bone_position_z=position[2],
        )

    def getJointStateByName(self, joint_name: str):
        if joint_name not in self.name_list:
            raise ValueError("The joint name is not in the list")
        # print(self.env.instance_channel.data)
        joint_states = self.env.instance_channel.data[self.id][joint_name]
        return joint_states

    def getJointPositionByName(self, joint_name: str):
        """
        Position in the world coordinate
        """
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["position"]

    def getJointGlobalRotationByName(self, joint_name: str):
        """
        Euler angles in degrees
        """
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["rotation"]

    def getJointQuaternionByName(self, joint_name: str):
        """
        Quaternion
        """
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["quaternion"]

    def getJointLocalRotationByName(self, joint_name: str):
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["local_rotation"]

    def getJointLocalQuaternionByName(self, joint_name: str):
        """
        Quaternion
        """
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["local_quaternion"]

    def getJointVelocityByName(self, joint_name: str):
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["velocity"]

    def getJointRotationByName(self, joint_name: str):
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["joint_position"]

    def getJointAccelerationByName(self, joint_name: str):
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["acceleration"]

    def getJointForceByName(self, joint_name: str):
        joint_states = self.getJointStateByName(joint_name)
        return joint_states["joint_force"]

    def saveArticulationBoneData(self, path: str):
        self.env.instance_channel.set_action(
            "SaveArticulationBoneData", id=self.id, path=path
        )

    def enableSoftBody(self):
        """
        TODO: enable soft body
        """
        self.env.instance_channel.set_action("EnableSoftBody", id=self.id)


    '''def refresh_muscle_data_all(self):
        """
        Helper function to get the most recent muscle data for all tendons
        """
        for group in self.muscle_groups.keys():
            self.refresh_muscle_data_group(group)

    def refresh_muscle_data_group(self,group: str):
        """
        Helper function to get the most recent data for group of tendons
        """
        group_data = self.env.instance_channel.data[self.id].get(group,None)
        if group_data == None:
            raise ValueError("Error retrieving muscle data from Unity.")
        else:
            for tendon,tendon_info in group_data.items():
                self.muscle_tendons[tendon] = tendon_info

    def get_all_muscle_data(self):
        """
        Retrieves data of all muscle tendons.
        """
        self.refresh_muscle_data_all()
        return self.muscle_tendons

    def get_muscle_group_data(self,group: str):
        """
        Retrieves data of all muscle tendon units in a given muscle group.
        """
        if group not in self.muscle_groups:
            raise ValueError(f"Invalid muscle group '{group}' requested")
        self.refresh_muscle_data_group(group)
        out = {}
        for tendon in self.muscle_groups[group]:
            out[tendon] = self.muscle_tendons[tendon]
        return out

    def get_muscle_data(self, muscle_name: str):
        """
        Retrieves data of a single muscle tendon unit.
        """
        self.refresh_muscle_data_all()
        if muscle_name in self.muscle_tendons:
            return self.muscle_tendons[muscle_name]
        else:
            raise ValueError(f"Muscle '{muscle_name}' not found.")'''
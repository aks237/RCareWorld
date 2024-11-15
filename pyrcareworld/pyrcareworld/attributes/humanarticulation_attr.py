import pyrcareworld.attributes as attr
from pyrcareworld.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
import pyrcareworld.utils.utility as utility


def parse_message(msg: IncomingMessage) -> dict:
    this_object_data = attr.base_attr.parse_message(msg)
    count_joints = msg.read_int32()
    # print(count)
    for _ in range(count_joints):
        name = msg.read_string()
        # print(_)
        # print(this_object_data)
        this_object_data[name] = {}
        this_object_data[name]["position"] = [msg.read_float32() for _ in range(3)]
        this_object_data[name]["rotation"] = [msg.read_float32() for _ in range(3)]
        this_object_data[name]["quaternion"] = [msg.read_float32() for _ in range(4)]
        this_object_data[name]["local_rotation"] = [
            msg.read_float32() for _ in range(3)
        ]
        this_object_data[name]["local_quaternion"] = [
            msg.read_float32() for _ in range(4)
        ]
        this_object_data[name]["velocity"] = [msg.read_float32() for _ in range(3)]

        this_object_data[name]["joint_position"] = [msg.read_float32()]
        this_object_data[name]["joint_velocity"] = [msg.read_float32()]
        this_object_data[name]["joint_acceleration"] = [msg.read_float32()]
        this_object_data[name]["joint_force"] = [msg.read_float32()]
    
    count_groups = msg.read_int32()
    for _ in range(count_groups):
        group_name = msg.read_string()
        this_object_data[group_name] = {}
        count_muscles = msg.read_int32()
        for _ in range(count_muscles):
            muscle_name = msg.read_string()
            this_object_data[group_name][muscle_name] = {}
            this_object_data[group_name][muscle_name]["excitation"] = msg.read_float32()
            this_object_data[group_name][muscle_name]["length"] = msg.read_float32()
    
    return this_object_data


# bone name list:
# Pelvis
# Spine1
# Spine2
# Spine3
# LeftShoulder
# LeftUpperArm
# LeftLowerArm
# LeftHand
# RightShoulder
# RightUpperArm
# RightLowerArm
# RightHand
# LeftUpperLeg
# LeftLowerLeg
# LeftFoot
# LeftToes
# RightUpperLeg
# RightLowerLeg
# RightFoot
# RightToes
# Neck
# Head
# LeftEye
# RightEye
# Jaw
# LeftThumb1
# LeftThumb2
# LeftThumb3
# LeftIndex1
# LeftIndex2
# LeftIndex3
# LeftMiddle1
# LeftMiddle2
# LeftMiddle3
# LeftRing1
# LeftRing2
# LeftRing3
# LeftPinky1
# LeftPinky2
# LeftPinky3
# RightThumb1
# RightThumb2
# RightThumb3
# RightIndex1
# RightIndex2
# RightIndex3
# RightMiddle1
# RightMiddle2
# RightMiddle3
# RightRing1
# RightRing2
# RightRing3
# RightPinky1
# RightPinky2
# RightPinky3

def SetMuscleActivation(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ["id", "muscle_name", "activation"]
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()

    msg.write_int32(kwargs["id"])
    msg.write_string("SetMuscleActivation")
    msg.write_string(kwargs["muscle_name"])
    msg.write_float32(kwargs["activation"])
    return msg

def SetMultipleMuscleActivations(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ["id", "activation_data"]
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs["id"])
    msg.write_string("SetMultipleMuscleActivations")
    count = len(kwargs["activation_data"])
    msg.write_int32(count)
    for (muscle,activation) in kwargs["activation_data"].items():
        msg.write_string(muscle)
        msg.write_float32(activation)
    return msg
        

def SetNameBonePosition(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ["id", "bone_name", "bone_position"]
    optional_params = ["bone_position_y", "bone_position_z"]
    utility.CheckKwargs(kwargs, compulsory_params)
    # print(kwargs)
    msg = OutgoingMessage()

    msg.write_int32(kwargs["id"])
    msg.write_string("SetNameBonePosition")
    msg.write_string(kwargs["bone_name"])
    msg.write_float32(kwargs["bone_position"])
    msg.write_bool("bone_position_y" in kwargs)
    if "bone_position_y" in kwargs:
        msg.write_float32(kwargs["bone_position_y"])
    msg.write_bool("bone_position_z" in kwargs)
    if "bone_position_z" in kwargs:
        msg.write_float32(kwargs["bone_position_z"])

    return msg


def SetNameBonePositionDirectly(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ["id", "bone_name", "bone_position"]
    optional_params = ["bone_position_y", "bone_position_z"]
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()

    msg.write_int32(kwargs["id"])
    msg.write_string("SetNameBonePositionDirectly")
    msg.write_string(kwargs["bone_name"])
    msg.write_float32(kwargs["bone_position"])
    msg.write_bool("bone_position_y" in kwargs)
    if "bone_position_y" in kwargs:
        msg.write_float32(kwargs["bone_position_y"])
    msg.write_bool("bone_position_z" in kwargs)
    if "bone_position_z" in kwargs:
        msg.write_float32(kwargs["bone_position_z"])

    return msg


def SaveArticulationBoneData(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ["id", "path"]
    optional_params = []
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()

    msg.write_int32(kwargs["id"])
    msg.write_string("SaveArticulationBoneData")
    msg.write_string(kwargs["path"])

    return msg


def SetJointLimits(kwargs: dict) -> OutgoingMessage:
    """
    Set joint limits for a specific bone in an ArticulationBody. Will apply to the joint connecting that bone to the previous bone in the hierarchy.

    Args:
        Compulsory:
            id: The id of the ArticulationBody object.
            bone_name: The name of the bone to select a joint for.
            lower_limit: The lower limit of the joint.
            upper_limit: The upper limit of the joint.
        Optional:
            axis: The axis of the joint to set the limits for: {"X", "Y", or "Z"}.

            If not specified, sets all limits (often fine since most joints only have 1 free axis).
    """
    compulsory_params = ["id", "bone_name", "lower_limit", "upper_limit"]
    optional_params = ["axis"]
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()

    msg.write_int32(kwargs["id"])
    msg.write_string("SetJointLimits")
    msg.write_string(kwargs["bone_name"])
    msg.write_float32(kwargs["lower_limit"])
    msg.write_float32(kwargs["upper_limit"])
    msg.write_bool("axis" in kwargs)
    if "axis" in kwargs:
        msg.write_string(kwargs["axis"])

    return msg

import os
from pyrcareworld.envs import RCareWorld
import random

# The corresponding scene in RCareUnity is Assets/Musculoskeletal/Scenes/Musculoskeletal.unity

env = RCareWorld(executable_file="@Editor", assets=["HumanArticulation"])

human = env.create_human(id=123456, name="HumanArticulation", is_in_scene=True)

human.setBasePosition([0, 2, 0])
env._step()

'''
The activation dict returned has keys with the names of the muscles and the values of 
the activation signals (by default set to 0). By modifying the values of the desired muscles
in the same dictionary, the user can pass it in to set multiple muscle activations at once.
''' 

# Get the muscles in the whole body
activations = human.get_activation_dict_all()
print(activations)

while True:

    #Set all the activations to random values
    for muscle in activations.keys():
        activations[muscle] = min(0.9, random.random()+0.4)

    human.set_multiple_muscle_activations(activations)

    env._step()


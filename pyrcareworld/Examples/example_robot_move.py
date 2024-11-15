from pyrcareworld.envs import RCareWorld

env = RCareWorld()
robot = env.create_robot(
    id=315893,
    gripper_list=["3158930"],
    robot_name="kinova_gen3_7dof-robotiq85",
    base_pos=[0, 0, 1],
)
target = env.create_object(id=315867, name="Cube", is_in_scene=True)
while True:
    position = target.getPosition()
    robot.directlyMoveTo(position)
    env.step()

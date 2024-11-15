from pyrcareworld.envs import RCareWorld

env = RCareWorld(assets=["Cube"])
cube = env.create_object(id=12345, name="Cube", is_in_scene=False)
cube.load()
for i in range(500):
    env._step()
    print(env.instance_channel.data)
env.close()

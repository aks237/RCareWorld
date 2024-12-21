import numpy as np
import rerun as rr
from scipy.optimize import lsq_linear
import cvxpy as cp

"""
Class to solve for tendon activations and
visualize musculoskeletal model from Unity using Rerun.
(gizmo rendering currently not functional in Unity)
"""

class MusculoskeletalSolver:

    def __init__(self, visualize=False):

        self.tendons = {}
        self.visualize = visualize
        self.desired_torque_vector = np.zeros((66,1))
        self.torque_matrix = np.zeros((66,332))
        self.activations = None
        self.initialized = False
        if self.visualize:
            rr.init("tendon_visualization", spawn=True)
        

    def update(self, data, solve):
        '''
        Update the tendon nodes and unit torques. If solve is true,
        solve for tendon activations at this timestep.
        ''' 
        # Initialize tendon dictionary if emtpy
        if len(self.tendons.keys()) == 0:
            for key in data.keys():
                if "nodes" in key:
                    self.tendons[key[:key.index("nodes")]] = []
            print(self.tendons)
        
        self.torque_matrix = np.zeros((66,332))
        for i,key in enumerate(self.tendons.keys()):
            nodes = key + "nodes"
            self.tendons[key] = data[nodes]
            if solve:
                torques = key + "torques"
                self.torque_matrix[:,i] = np.array(data[torques]).reshape(66)

        if solve:
            self.desired_torque_vector = np.array(data['drive_forces']).reshape((66,))
            self.solve_activations()

        if self.visualize:
            self.create_rerun_lines()

    
    def solve_activations(self):
        '''
        Solve for the current activations based on current muscle tendon unit torques and desired torques
        in body joints. If activations have been solved for previously, solve while minimizing changes in activations.
        If solving for the first time, choose any solution.
        '''
        if(self.initialized):
            n = self.torque_matrix.shape[1]

            a = cp.Variable(n)
            curr = cp.Variable(n)
            curr.value = self.activations
            epsilon = 10
            constraints = [a >= 0, a <= 1, cp.norm(self.torque_matrix @ a - self.desired_torque_vector, 2) <= epsilon]

            objective = cp.Minimize(cp.sum_squares(a-self.activations))
            prob = cp.Problem(objective, constraints)
            prob.solve()

            self.activations = a.value
            
        if(not self.initialized or self.activations is None):
            self.activations = lsq_linear(self.torque_matrix, self.desired_torque_vector, bounds=(0, 1)).x
        
        print(self.activations)
        self.initialized = True


    def create_rerun_lines(self):
        '''
        Function to visualize tendons on python side using rerun.
        Used because Unity gizmo rendering currently not working.
        '''
        q1 = []
        q2 = []

        for i, nodes in enumerate(self.tendons.values()):
            for i in range(len(nodes)-1):
                q1.append(np.array([nodes[i][0], nodes[i][2], nodes[i][1]]))
                q2.append(np.array([nodes[i+1][0], nodes[i+1][2], nodes[i+1][1]]))
            if(self.initialized):
                multiplier = self.activations[i]
            else:
                multiplier = 0
            rr.log(
                "musculoskeletal/tendon" + str(i),
                rr.LineStrips3D(np.stack((q1,q2), axis=1), radii=0.001, colors=[255*multiplier,0,0])
            )
        

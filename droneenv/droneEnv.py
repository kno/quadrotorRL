#./vrep.sh -gREMOTEAPISERVERSERVICE_19999_TRUE_TRUE ../ejemplos/GYM/oneDrone.ttt
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import vrep

def distance(a,b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

class DroneEnv(gym.Env):
    def __init__(self):
        high = np.array([
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max,
            np.finfo(np.float32).max])

        self.action_space = spaces.Discrete(9) #0 do nothing, 1 acelerate rotor 1, 2 acelerate rotor 2... 5 decelerate rotor 1, 6 decelerate rotor 2...
        self.observation_space = spaces.Box(-high, high) # Position and speed of drone & objetive position
        self.state = None
        self.particleVelocities = [4,]
        #Connect with simulator
        self.clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
        if self.clientID!=-1:
            logger.warn ('Connected to remote API server')

    def getDistance(self):
        return distance(self.getQuadricopterPosition(),self.getQuadricopterTargetPosition())

    def getQuadricopterPosition(self):
        status,quadPosition = vrep.simxGetObjectPosition(self.clientID,self.quadricopter,-1,vrep.simx_opmode_blocking)
        return quadPosition

    def getQuadricopterTargetPosition(self):
        status,quadPosition = vrep.simxGetObjectPosition(self.clientID,self.quadricopterTarget,-1,vrep.simx_opmode_blocking)
        return quadPosition

    def getStatus(self):
        return self.getQuadricopterPosition(),self.getQuadricopterTargetPosition()

    def getParticleVelocity(self, propeler):
        print ("Getting velocity for propeler ", propeler)
        emptyBuff = bytearray()
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(self.clientID,\
            'Quadricopter_propeller_respondable' + `propeler`,\
            vrep.sim_scripttype_childscript,\
            'getParticleVelocity',\
            [],[],[],emptyBuff,vrep.simx_opmode_blocking)
        if res==vrep.simx_return_ok:
            return(retInts[0])
        else:
            return("None")

    def setParticleVelocity(self, propeler, newVel):
        print("Set propeler #", propeler, " to ", newVel)
        emptyBuff = bytearray()
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(self.clientID,\
            'Quadricopter_propeller_respondable' + `propeler`,\
            vrep.sim_scripttype_childscript,\
            'setParticleVelocity',\
            [newVel],[],[],emptyBuff,vrep.simx_opmode_blocking)
        if res==vrep.simx_return_ok:
            return(1)
        else:
            return(None)

    def reset(self):
        vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_blocking)
        vrep.simxStartSimulation(self.clientID,vrep.simx_opmode_blocking)
        status,self.quadricopter = vrep.simxGetObjectHandle(self.clientID,"Quadricopter",vrep.simx_opmode_blocking)
        status,self.quadricopterTarget = vrep.simxGetObjectHandle(self.clientID,"Quadricopter_target",vrep.simx_opmode_blocking)
        self.distance = self.getDistance()
        print("Distance ", self.distance)

        return None

    def render(self):
        return None

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        print("QP ", self.getQuadricopterPosition())
        print("QTP ", self.getQuadricopterTargetPosition())
        print("Distance ", self.getDistance())
        reward = 0
        done = False
        print ("Accion: ", action)
        if (action == 0):
            return np.array(self.state), reward, done, {}
        elif (action <= 4):
            v = self.getParticleVelocity(action)
            print("V->", v)
            self.setParticleVelocity(action, v + 1)
        else:
            v = self.getParticleVelocity(action - 4)
            print("V->", v)
            self.setParticleVelocity(action - 4, v - 1)

        newDistance = self.getDistance();
        if (newDistance > self.distance):
            reward = -1
        elif (newDistance < self.distance):
            reward = 1
        self.distance = newDistance

        return np.array(self.getStatus()), reward, done, {}
    def stop(self):
        vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_blocking)

import gym
import random
import numpy as np
from math import sqrt
from gym import spaces

class ShepherdEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    # action_space ... actions of an agent
    # action_space ... the environment’s data to be observed by the agent

    def init_sheep_table (self):

        sheep_x = random.sample(range(1, self.field_size), self.sheep_num)
        sheep_y = random.sample(range(1, self.field_size), self.sheep_num)
        herd = zip(sheep_x, sheep_y)
        dog = (0,0)

        return herd, dog

    def __init__(self, state):

        
        self.finish = False
        self.curr_episode = 0
        self.current_step = 0
        self.episode_length = 0
        self.episode_reward = 0

        self.max_num_of_steps = 1000 
        self.target_distance = 10
        self.calculated_distance = self.field_size*sqrt(2)

        self.sheep_num = 5
        self.field_size = 20
        self.herd, self.dog = self.init_sheep_table()

        self.action_space = spaces.Discrete(4)
        obs_low = np.array(3*[0])
        obs_high = np.ones(3)
        self.observation_space = spaces.Box(low=obs_low, high=obs_high)
        
    def step(self, action):

        """
            The dog takes a step in the environment
            Parameters
            ----------
            action : float array
            Returns
            -------
            ob, reward, episode_over, info : tuple
                observation (float array) : 
                    observation after dog position is updated.
                reward (float) : 
                    amount of reward achieved by dog in the previous step.
                episode_over (bool) : 
                    flag that indicates if the environment is reset or not.
                info (dict) :
                    useful information about the environment for debugging.
            """
        
        success = False

        # TODO (Nika) posodobi pozicijo psa
        self.current_step += 1
        self._take_action(action)
        
        # get reward and state 
        # TODO (Ada) nastavi not self.calculated_distance - to je max razdalja ovce od centra
        ob = self._get_state()
        reward = self._get_reward()

        # bad terminal conditions
        if self.current_step > self.max_num_of_steps:
            self.finish = True

        # good terminal conditions
        if self.calculated_distance <= self.target_distance:
            success = True
            self.finish = True

        # update rl parameters
        self.episode_length += 1
        self.episode_reward += reward

        # generate info return parameter
        if self.info_mode == 1 and self.finish:
            info = {'r':self.episode_reward, 'l':self.episode_length, 's': success}
        else:
            info = {'n':self.num_sheep, 's': success}

        return ob, reward, self.finish, info

    def reset(self):

        self.finish = False
        self.curr_episode += 1
        self.current_step = 0
        self.episode_length = 0
        self.episode_reward = 0

        self.current_step = 0
        self.herd, self.dog = self.init_sheep_table()

        state = self._get_state()
        return state

    def render(self, mode='human'):
        ...

    def _get_state(self):
        """Return state based on action of the dog
           Stack all variables and return state array
          
        state = np.hstack((self.sheep_com, self.farthest_sheep, 
                    self.target, self.dog_pose, self.radius_sheep, 
                    self.target_distance))
        return state
        """
        return [0, 0.25, 0.5]
        
    def _get_reward(self):
            """Return reward based on action of the dog"""
            return 0.25

    def _take_action(self, action):
        """Update position of dog based on action and env"""
        self._update_environment()

    def _update_environment(self):
        """Update environment based on new position of dog"""
   
        state = self.herd
        pes = self.dog
        n = self.field_size

        newState = []
        (x, y) = pes
        for ovca in state:
            (i, j) = ovca

            #ali je blizu psa
            r_x = x-i
            r_y = y-j
            if r_x**2+r_y**2<=25:
                ii = jj = 0
                if abs(r_x)<abs(r_y):
                    if r_x>0:
                        ii = 1
                    else:
                        ii = -1
                else:
                    if r_y>0:
                        jj = 1
                    else:
                        jj = -1
                
                
                if (i +ii, j +jj) not in newState and 0<=i+ii<=n and 0<=j+jj<=n:
                    newState.append((i +ii, j +jj))
                else:
                    if ii == 0:
                        if (i +ii + 1, j +jj) not in newState and 0<=i+ii +1<=n and 0<=j+jj<=n:
                            newState.append((i +ii +1, j +jj))
                        elif (i +ii -1, j +jj) not in newState and 0<=i+ii-1<=n and 0<=j+jj<=n:
                            newState.append((i +ii -1, j +jj))
                        else:
                            newState.append(ovca)
                    else:
                        if (i +ii, j +jj +1) not in newState and 0<=i+ii<=n and 0<=j+jj+1<=n:
                            newState.append((i +ii, j +jj +1))
                        elif (i +ii, j +jj -1) not in newState and 0<=i+ii<=n and 0<=j+jj-1<=n:
                            newState.append((i +ii, j +jj -1))
                        else:
                            newState.append(ovca)
            else:
                a=random.randint(-1,1)
                if a>0: #gor dol
                    b = random.randint(-1,1)
                    if (i, j +b) not in newState and 0<=j+b<=n:
                            newState.append((i, j +b))
                    elif (i - 1, j + b) not in newState and 0<=j+b<=n and 0<=i-1<=n:
                            newState.append((i-1, j +b))
                    elif (i + 1, j + b) not in newState and 0<=j+b<=n and 0<=i+1<=n:
                            newState.append((i+1, j +b))
                    else:
                            newState.append(ovca)
                
                else:
                    b = random.randint(-1,1)
                    if (i +b , j) not in newState and 0<=i+b<=n:
                            newState.append((i + b, j))
                    elif (i+b, j + 1) not in newState and 0<=i+b<=n and 0<=j+1<=n:
                            newState.append((i+b, j +1))
                    elif (i + b, j - 1) not in newState and 0<=i+b<=n and 0<=j-1<=n:
                            newState.append((i+b, j -1))
                    else:
                            newState.append(ovca)

        self.herd = newState
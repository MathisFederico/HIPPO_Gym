'''
This is a demo file to be replaced by the researcher as required.
This file is imported by trial.py and trial.py will call:
start()
step()
render()
reset()
close()
These functions are mandatory. This file contains minimum working versions 
of these functions, adapt as required for individual research goals.
'''
import gym

def start(game:str):
    '''
    Starts an OpenAI gym environment.
    Caller:
        - Trial.start()
    Inputs:
        -   game (Type: str corresponding to allowable gym environments)
    Returs:
        - env (Type: OpenAI gym Environment as returned by gym.make())
        Mandatory
    '''
    env = gym.make(game)
    return env

def step(env, action:int):
    '''
    Takes a game step.
    Caller: 
        - Trial.take_step()
    Inputs:
        - env (Type: OpenAI gym Environment)
        - action (Type: int corresponding to action in env.action_space)
    Returns:
        - envState (Type: dict containing all information to be recorded for future use)
          change contents of dict as desired, but return must be type dict.
    '''
    observation, reward, done, info = env.step(action)
    envState = {'observation': observation, 'reward': reward, 'done': done, 'info': info}
    return envState

def render(env):
    '''
    Gets render from gym.
    Caller:
        - Trial.get_render()
    Inputs:
        - env (Type: OpenAI gym Environment)
    Returns:
        - return from env.render('rgb_array') (Type: npArray)
          must return the unchanged rgb_array
    '''
    return env.render('rgb_array')

def reset(env):
    '''
    Resets the environment to start new episode.
    Caller: 
        - Trial.reset()
    Inputs:
        - env (Type: OpenAI gym Environment)
    Returns: 
        No Return
    '''
    env.reset()

def close(env):
    '''
    Closes the environment at the end of the trial.
    Caller:
        - Trial.close()
    Inputs:
        - env (Type: OpenAI gym Environment)
    Returns:
        No Return
    '''
    env.close()
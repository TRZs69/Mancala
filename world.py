import numpy as np
import time

startState=(4,4,4,4,4,4,0,4,4,4,4,4,4,0,True)

def transition(state,action):
    newstate=list(state)
    newstate[-1]=not newstate[-1]
    if state[-1]:
        point=action+1
        times=state[action]
        newstate[action]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point<6) and (newstate[12-point]>0):
                newstate[6]+=1+newstate[12-point]
                newstate[12-point]=0
                break
            newstate[point]+=1
            point+=1
            if point==14:
                point=0
    else:
        point=action+8
        times=state[action+7]
        newstate[action+7]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point>6) and (newstate[12-point]>0):
                newstate[13]+=1+newstate[12-point]
                newstate[12-point]=0
                break
            newstate[point]+=1
            point+=1
            if point==14:
                point=0
    return tuple(newstate)

def transitionIterating(state,action):
    newstate=list(state)
    newstate[-1]=not newstate[-1]
    if state[-1]:
        point=action+1
        times=state[action]
        newstate[action]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point<6) and (newstate[12-point]>0):
                time.sleep(0.5)
                yield newstate,action,point,1
                newstate[6]+=1+newstate[12-point]
                buf=newstate[12-point]
                time.sleep(0.5)
                yield newstate,point,6,1
                newstate[12-point]=0
                yield newstate,12-point,6,buf
                break
            newstate[point]+=1
            time.sleep(0.5)
            yield newstate,action,point,1
            point+=1
            if point==14:
                point=0
    else:
        point=action+8
        times=state[action+7]
        newstate[action+7]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point>6) and (newstate[12-point]>0):
                time.sleep(0.5)
                yield newstate,action+7,point,1
                newstate[13]+=1+newstate[12-point]
                buf=newstate[12-point]
                time.sleep(0.5)
                yield newstate,point,13,1
                newstate[12-point]=0
                yield newstate,12-point,13,buf
                break
            newstate[point]+=1
            time.sleep(0.5)
            yield newstate,action+7,point,1
            point+=1
            if point==14:
                point=0

def getLegalActions(state):  
    actions=[]
    if state[-1]==True:
        for i in range(0,6):
            if state[i]>0:
                actions.append(i)
    else:
        for i in range(7,13):
            if state[i]>0:
                actions.append(i-7)
    return actions


def isTerminal(state):  
    if (np.sum(state[:6])==0) or (np.sum(state[7:13])==0):
        return True
    return False

def getSum(state):  
    return np.sum(state[:7]),np.sum(state[7:-1])

import pickle
import mpu

# serialize
def save_agent(agent):
    with open('agent.dat', 'wb') as f:
        pickle.dump(agent, f)
    
    # mpu.io.write('agent.dat', agent) 
# deserialize
def load_agent():
    with open('agent.dat', 'rb') as f:
        data = pickle.load(f)
        print((data, type(data)))
        return data
    # return mpu.io.read('agent.dat')
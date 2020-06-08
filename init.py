from src.system import System
import pickle

def bootstrap_system():

    f = open("system.pickle", "rb")
    sys = pickle.load(f)
  

    #f = open("system.pickle", "wb")
    #pickle.dump(sys, f)

    return sys

from src.mro import MRO
from src.namespaces import Namespaces


def main(alg):
    if alg == "MRO":
        mro = MRO()
        mro.run()
    elif alg == "NS":
        ns = Namespaces()
        ns.run()
    else:
        raise Exception("InputError: wrong input were specified")
    
    
if __name__ == '__main__':
    algo = input("Enter a model to run (MRO - 'MRO C3', NS - 'Namespaces model'): ")
    main(algo)
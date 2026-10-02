import argparse
from trainers.checkpoints.store import JsonCheckpointStore
def main():
    p=argparse.ArgumentParser(); p.add_argument("directory"); args=p.parse_args()
    store=JsonCheckpointStore(args.directory)
    print(store.load().step)
if __name__=="__main__": main()

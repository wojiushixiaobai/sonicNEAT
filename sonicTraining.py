import os
import retro        # pip install gym-retro
import numpy as np  # pip install numpy
import cv2          # pip install opencv-python
import neat         # pip install neat-python
import pickle       # pip install cloudpickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

resume = False

files=os.listdir(BASE_DIR)
checkpoint=[]
for file in files:
    if "neat-checkpoint-" in file:
        checkpoint.append(int(file.rsplit('-', maxsplit=1)[1]))

if checkpoint:
    restore_file = "neat-checkpoint-%s" %(max(checkpoint))
    resume = True
else:
    restore_file = "neat-checkpoint-0"

class Worker(object):
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config

    def work(self):

        self.env = retro.make(game = "SonicTheHedgehog-Genesis", state='GreenHillZone.Act2')

        self.env.reset()

        ob, _, _, _ = self.env.step(self.env.action_space.sample())

        inx = int(ob.shape[0]/8)
        iny = int(ob.shape[1]/8)
        done = False

        net = neat.nn.recurrent.RecurrentNetwork.create(self.genome, self.config)

        fitness = 0
        xpos = 0
        xpos_max = 0
        counter = 0
        imgarray = []

        while not done:
            #cv2.namedWindow("main", cv2.WINDOW_NORMAL)
            ob = cv2.resize(ob, (inx, iny))
            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            ob = np.reshape(ob, (inx, iny))

            imgarray = np.ndarray.flatten(ob)

            actions = net.activate(imgarray)

            ob, rew, done, info = self.env.step(actions)

            xpos = info['x']


            if xpos > xpos_max:
                xpos_max = xpos
                counter = 0
                fitness += 10
            else:
                counter += 1

            if counter > 250:
                done = True

        print(fitness)
        return fitness

def eval_genomes(genome, config):
    worky = Worker(genome, config)
    return worky.work()

def main():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')

    if resume == True:
        p = neat.Checkpointer.restore_checkpoint(restore_file)
    else:
        p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    pe = neat.ParallelEvaluator(32, eval_genomes)

    winner = p.run(pe.evaluate)

    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)


if __name__ == '__main__':
    main()

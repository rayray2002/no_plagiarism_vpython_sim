import numpy as np
import vpython as vp


class ghistogram:

    def __init__(self, graph, bins, color=vp.color.red):
        self.bins = bins
        self.slotnumber = len(bins)
        self.slotwidth = bins[1] - bins[0]
        self.n = 0
        self.slots = np.zeros(len(bins))
        self.bars = vp.gvbars(graph=graph, delta=self.slotwidth, color=color)

    def plot(self, data):
        currentslots = np.zeros(self.slotnumber)
        for value in data:
            currentslots[min(max(int((value - self.bins[0]) / self.slotwidth), 0), self.slotnumber - 1)] += 1
        self.slots = (self.slots * self.n + currentslots) / (self.n + 1)
        self.n += 1
        if self.n == 1:
            for (currentbin, barlength) in zip(self.bins, self.slots):
                self.bars.plot(pos=(currentbin, barlength))
        else:
            self.bars.data = list(zip(self.bins, self.slots))


if __name__ == '__main__':
    vdist = vp.graph(width=450)
    observation = ghistogram(graph=vdist, bins=np.arange(1, 3, 0.5))
    observation.plot(data=[1.2, 2.3, 4])
    observation.plot(data=[1, 1.7, 2.6])
    observation.plot(data=[-0.5, 2, 2.3])

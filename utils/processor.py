import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from . import parser
from . import Anova

class Processor(object):
    def __init__(self, dir):
        self.file_list = parser.getFiles(dir)
        self.raw_data = []
        self.device = set()
        for file in self.file_list:
            file_data = parser.parseFile(file)
            if file_data == None or len(file_data)==0:
                print('warning: file ', file, ' cannot be read!')
                continue
            self.raw_data = self.raw_data + file_data
        self.fitts_data = self._genFittsData(self.raw_data) #{name, device, ID, MT}

    def _genFittsData(self, raw_data):
        fitts_data = []
        for raw_d in raw_data:
            fitts_d = {}
            fitts_d['name'] = raw_d['name']
            fitts_d['device'] = raw_d['device']
            self.device.add(fitts_d['device'])
            fitts_d['ID'] = math.log2(2*raw_d['distance']/raw_d['width'])
            fitts_d['MT'] = raw_d['time']
            fitts_data.append(fitts_d)
        return fitts_data

    def showScatterGraph(self):
        plt.clf()
        data_buf = {}
        # get device
        for d in self.fitts_data:
            data_buf[d['device']] = ([], [])
        # set data
        for d in self.fitts_data:
            data_buf[d['device']][0].append(d['ID']) #ID
            data_buf[d['device']][1].append(d['MT']) #MT
        # draw
        for device in data_buf:
            plt.scatter(data_buf[device][0], data_buf[device][1], marker = 'o', s = 40 ,label = device)
        plt.legend(loc = 'best')
        plt.show()

    def regression(self, device):
        if device not in self.device:
            print(f"No device named: {device}, please check your input!")
            return 
        # prepare data
        ID = []
        MT = []
        name = set()
        for d in self.fitts_data:
            if d['device'] == device:
                ID.append(d['ID'])
                MT.append(d['MT'])
                name.add(d['name'])
        ID = np.array(ID).reshape((-1,1))
        MT = np.array(MT)
        # generate regression
        model = LinearRegression().fit(ID, MT)
        # print report
        print("========== MT=a+bID regression report ===========")
        print("using device: ", device)
        print("users: ", name)
        print("coefficient of determination(r^2) : ", model.score(ID, MT))
        print("intercept(a) : ", model.intercept_)
        print("slope(b) : ", model.coef_[0])
        print(" ")

    def anova(self, params=['name', 'device']):
        Anova.multi_analyze(self.raw_data, params)

    def getRawData(self):
        return self.raw_data

    def getFittsData(self):
        return self.fitts_data


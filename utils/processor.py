import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from prettytable import PrettyTable, MARKDOWN
from . import parser
from . import Anova

class Processor(object):
    def __init__(self, dir):
        self.file_list = parser.getFiles(dir)
        self.dir = dir
        self.raw_data = [] # raw data directly obtained from the parser
        self.device = set() # types of device
        for file in self.file_list:
            file_data = parser.parseFile(file)
            if file_data == None or len(file_data)==0:
                print('warning: file ', file, ' cannot be read!')
                continue
            self.raw_data = self.raw_data + file_data
        # generate fitts data from raw data
        self.fitts_data = self._genFittsData(self.raw_data) #{name, device, ID, MT}

    def _genFittsData(self, raw_data):
        fitts_data = []
        for raw_d in raw_data:
            fitts_d = {}
            fitts_d['name'] = raw_d['name']
            fitts_d['device'] = raw_d['device']
            self.device.add(fitts_d['device'])
            # MT = a + b*ID
            # T = a + b*log2(A/W + 1)
            fitts_d['ID'] = math.log2(raw_d['distance']/raw_d['width'] + 1)
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
            plt.xlabel('ID = log2(A/W+1)')
            plt.ylabel('MT = time')
        plt.legend(loc = 'best')
        plt.show()

    def _regression(self, device):
        if device not in self.device:
            print(f"No device named: {device}, please check your input!")
            return 
        # prepare data
        ID = []
        MT = []
        name = set()
        name.add('all')
        group = {}
        group['all'] = [[], []] # [ID], [MT]
        for d in self.fitts_data:
            if d['device'] == device:
                if(d['name']) not in name:
                    name.add(d['name'])
                    group[d['name']] = [[], []]
                group[d['name']][0].append(d['ID'])
                group[d['name']][1].append(d['MT'])
                group['all'][0].append(d['ID'])
                group['all'][1].append(d['MT'])
        # show data
        table = PrettyTable()
        table.field_names = ["user", "a", 'b', 'r^2']
        table.set_style(MARKDOWN)
        print(f" regression report on [{device}] ")
        print("(This table can be copied to markdown as a table directly)")
        for result in group:
            name = result
            ID = np.array(group[result][0]).reshape((-1,1))
            MT = np.array(group[result][1])
            # generate regression
            model = LinearRegression().fit(ID, MT)
            a = model.intercept_
            b = model.coef_[0]
            # print report
            table.add_row([name, a, b, model.score(ID, MT)])
            x = np.linspace(1.8,4.1)
            plt.scatter(ID,MT, marker='o')
            plt.plot(x, a+b*x, label=name)
            plt.xlabel('ID = log2(A/W+1)')
            plt.ylabel('MT = time')
        print(table)
        print(" ")
        plt.legend()
        plt.savefig(f"./{device}_regress.png")
        plt.clf()
            

    def regression(self):
        for device in self.device:
            self._regression(device)

    def anova(self, params=['name', 'device']):
        Anova.multi_analyze(self.raw_data, params)

    def print_data(self):
        pd_data = pd.DataFrame(self.raw_data)
        print(pd_data)

    def getRawData(self):
        return self.raw_data

    def getFittsData(self):
        return self.fitts_data
import argparse

from utils.processor import Processor

def parseArgs():
    parser = argparse.ArgumentParser(prog="Fitts law analyzer", description="welcome to use fittslaw analyser!",epilog="Copyright © 2020 pptrick. All rights reserved.")
    parser.add_argument("data_dir", type=str, help='data directory, containing multiple .csv files collected from http://39.97.170.246/fitts/')
    parser.add_argument("-g", "--graph", help='show data distribution in a graph', action="store_true")
    parser.add_argument("-r", "--regression", help='show regression result of each device', action="store_true")
    parser.add_argument("-p", "--print", help='print raw data collected from data directory', action="store_true")
    parser.add_argument("-a", "--anova", nargs='*', type=str, help='show anova analyse result, you can choose which factor to be analyse, e.g. -a device name width, default: [name, device]')
    return parser

if __name__ == "__main__":
    parser = parseArgs()
    args = parser.parse_args()
    processor = Processor(args.data_dir)
    if args.print:
        processor.print_data()
    if args.regression:
        processor.regression()
    if args.anova != None:
        if len(args.anova) == 0:
            processor.anova()
        else:
            processor.anova(args.anova)
    if args.graph:
        processor.showScatterGraph()

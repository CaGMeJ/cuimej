import argparse
import sys
import re

class graph:
    def __init__(self, L):
        self.L = L
        self.dup = {}
        self.end = set()
        self.graph = {}
        self.cnt = 1
        self.fm_list = {}

    def make(self, fn):
        with open(fn) as lines:
            name = None
            fm = None
            flag = None
            for line in lines:
                x = re.findall("process(.*){", line.replace(" ", ""))
                if len(x):
                    name = x[0]
                if name:
                    if line.replace(" ", "") in {"input:\n", "output:\n", "\"\"\"\n"}:
                        flag = line.replace(" ", "")
                        continue
                    if flag == "input:\n":
                        x = re.findall(" from (.*)\.?.*\n$", line)
                        if len(x):
                            if "?" in x[0]:
                                x = re.findall("\?(.*?)\.", x[0])
                            elif "." in x[0]:
                                x = re.findall("(.*?)\.", x[0])

                            if not name in self.graph:
                                self.graph[name] = {}
                            if not "fm" in self.graph[name]:
                                self.graph[name]["fm"] = []
                            self.graph[name]["fm"] += x[0].replace(" ", "").split(",")

                            continue
                        continue

                    if flag == "output:\n":
                        x = re.findall(" into (.*)", line)
                        if len(x):
                            if not name in self.graph:
                                self.graph[name] = {}
                            if not "to" in self.graph[name]:
                                self.graph[name]["to"] = []
                            self.graph[name]["to"] += x[0].replace(" ", "").split(",")

                            continue
                        continue
    def show(self):

        fm_list = {}
        to_list = {}
        no_fm = []
        for node in self.graph:
            if "fm" in self.graph[node]:
                for n in self.graph[node]["fm"]:
                    if n in fm_list:
                        fm_list[n].append(node)
                    else:
                        fm_list[n] = [node]
            else:
                no_fm.append(node)
            if "to" in self.graph[node]:
                for n in self.graph[node]["to"]:
                    if n in fm_list:
                        to_list[n].append(node)
                    else:
                        to_list[n] = [node]

        org_cand = set(fm_list.keys()) - set(to_list.keys())
        org = set()
        for node in org_cand:
            for process in fm_list[node]:
                if set(self.graph[process]["fm"]) < org_cand:
                    org.add(process)

        self.fm_list = fm_list
        for p in org:
            self.search(p, 0, False)

        self.end = set()
        for p in org:
            self.search(p, 0, True)

    def search(self, process, d, f):
        if d == self.L:
            return 0
        arrow = ""
        if d:
            arrow = (d*2*"-") + " "
        if process in self.end and not process in self.dup:
            self.dup[process] = self.cnt
            self.cnt += 1
        self.end.add(process)
        if f:
            print(arrow + process, end='')

        flag = True
        if "to" in self.graph[process]:
            for n in self.graph[process]["to"]:
                if n in self.fm_list:
                    for p in self.fm_list[n]:
                        if flag and f:
                            print()
                        flag = False
                        self.search(p, d+1, f)
        if f:
            if process in self.dup and flag :
                print(" " + ("*"*self.dup[process]) + " ")
            elif flag:
                print() 
        

parser = argparse.ArgumentParser()
parser.add_argument('nf')
parser.add_argument('-L',type=int, default=-1)
args = parser.parse_args()

g = graph(args.L)
g.make(args.nf)
g.show()

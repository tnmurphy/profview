import csv
import sys
from collections import defaultdict


class Profile:
    def __init__(self):
        self.notional_cpus={}

    @classmethod
    def from_file(cls, filename):
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            notional_cpus=defaultdict(list)
            header = True
            for row in spamreader:
                if header:
                    header = False
                    continue
                start, duration, notional_cpu_id, target = row
                notional_cpus[int(notional_cpu_id)].append((float(start),float(duration),target))
            pr = cls()
            pr.notional_cpus = notional_cpus
            return pr

    def print(self):
        for cpu in self.notional_cpus.keys():
            print(f"nCPU({cpu})")
            print(len(self.notional_cpus[cpu]))
            for t in self.notional_cpus[cpu]:
                start, duration, target = t 
                print(f"  {start} {duration} {target}")
                
if __name__ == "__main__":
    #print_csv(sys.argv[1])
    p = Profile.from_file(sys.argv[1])
    p.print()

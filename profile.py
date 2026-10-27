#!/bin/env python3
"""

GNU Make profile viewer

"""

import csv
import sys
from collections import defaultdict


class Profile:
    """Profiling information from GNU Make"""

    def __init__(self):
        self.notional_cpus = []
        self.start_time = None
        self.end_time = None

    @classmethod
    def from_file(cls, filename):
        """Read profiling data about a GNU make build from a CSV"""
        with open(filename, newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
            notional_cpus = defaultdict(list)
            header = True
            pr = cls()
            for row in spamreader:
                if header:
                    header = False
                    continue
                start, duration, notional_cpu_id, target = row
                target = target.rstrip(' "').strip(' "')
                notional_cpus[int(notional_cpu_id)].append(
                    (float(start), float(duration), target)
                )
                if pr.start_time == None:
                    pr.start_time = float(start)
                pr.end_time = float(start) + float(duration)

            cpus = sorted(notional_cpus.keys())
            pr.notional_cpus = [notional_cpus[c] for c in cpus]
            return pr

    def print(self):
        for cpu in range(0, len(self.notional_cpus)):
            print(f"nCPU({cpu})")
            print(len(self.notional_cpus[cpu]))
            oldend = 0.0
            for t in self.notional_cpus[cpu]:
                start, duration, target = t
                if start < oldend:
                    print(f"  {start} {duration} {target} [misorder]")
                else:
                    print(f"  {start} {duration} {target}")
                oldend = start + duration

    @classmethod
    def merge(cls, otherprofile: Profile):
        pass

if __name__ == "__main__":
    # print_csv(sys.argv[1])
    p = Profile.from_file(sys.argv[1])
    p.print()

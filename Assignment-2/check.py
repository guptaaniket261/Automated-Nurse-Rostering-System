import sys
import csv
import json
import numpy as np

##### CONSTRAINTS #####
# 
# 1. One shift per day 
# 2. M-M not allowed
# 3. E-M not allowed
# 4. #morning, #afternoon, #evening = m,a,e
# 5. Atleast one R per nurse per week
#
#######################

def correct(n,d,m,a,e):
    f = open("solution.json",)
    dic = json.load(f)
    c1,c2,c3,c4,c5 = True,True,True,True,True
    if len(dic.keys())==0:
        return c1,c2,c3,c4,c5 
    shift = {"R": 0, "M": 1, "A": 2, "E": 3}
    day_summary = [[0,0,0,0] for i in range(d)]
    for i in range(n):
        prev = "A"
        rest = False
        for j in range(d):
            curr = dic["N" + str(i) + "_" + str(j)]
            day_summary[j][shift[curr]] += 1
            if prev == "M" and curr == "M":
                c2 = False
                return c1,c2,c3,c4,c5
            if prev == "E" and curr == "M":
                c3 = False
                return c1,c2,c3,c4,c5
            if curr == "R":
                rest = True
            if j!=0 and j%7 == 6:
                if not rest:
                    c5 = False
                    return c1,c2,c3,c4,c5
                rest = False
            prev = curr
    r = n-m-a-e
    c4 = all(day == [r,m,a,e] for day in day_summary)
    return c1,c2,c3,c4,c5 




if __name__ == '__main__':
    file_name = sys.argv[1]
    file_in = open(file_name)
    csvReader = csv.reader(file_in)
    next(csvReader)
    for row in csvReader:
        n,d,m,a,e = list(map(int,row[:5]))
        output = list(correct(n,d,m,a,e))
        valid = all(constraint == True for constraint in output)
        if not valid :
            print("WRONG!!!")
            print(output)
        else:
            print("CORRECT")
    file_in.close()

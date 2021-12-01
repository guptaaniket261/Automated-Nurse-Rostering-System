##### ASSIGNMENT 2, COL 333 ##### 
##### FINAL #####
import sys
import numpy as np
import pandas as pd
import time
import json
sys.setrecursionlimit(100000)

assigned_var = {}
unassigned_var = {}
domains = {}
assignments = {}
week_summary = {}
day_summary = {}
val_map = {0:'R', 1:'M', 2:'A', 3:'E'}
bestScore = -1



def getUnassignedVar(unass_var, domains, D, part, S = 0):
    if part == 'A':
        var = -1
        min_dom = 10000
        min_day = 10000
        for k in unass_var:
            nurse, day = int(k/D), k%D
            if var == -1 or day < min_day:
                min_day = day
                min_dom = len(domains[k])
                var = k
            elif day==min_day and len(domains[k])<min_dom:
                min_dom = len(domains[k])
                var = k
        # print(var//D, var%D)
        return var
    else:
        var = -1
        min_dom = 10000
        min_day = 10000
        important = False
        for k in unass_var:
            nurse, day = int(k/D), k%D
            if var == -1 or day < min_day:
                min_day = day
                min_dom = len(domains[k])
                var = k
                if nurse<S:
                    important = True
                else:
                    important = False
            elif day==min_day and nurse<S and not important:
                important = True
                min_dom = len(domains[k])
                var = k
            elif day==min_day and nurse<S and len(domains[k])<min_dom:
                min_dom = len(domains[k])
                var = k
            elif day == min_day and (not important) and len(domains[k])<min_dom:
                min_dom = len(domains[k])
                var = k
        #print(var)
        return var

def isConsistent(var, val, N, D, m, a, e):
    nurse, day = int(var/D), var%D 
    week = int(day/7)
    n_rest = N-(m+a+e)
    req = [n_rest, m, a, e]
    if val!=0:
        if week_summary[week][nurse][1]+week_summary[week][nurse][2]+week_summary[week][nurse][3]+1==7:
            return False
    if day_summary[day][val]+1>req[val]:
        return False
    return True


def order(domains, nurse, day, N, D, m, a, e, part, S = 0):
    if part == 'A':
        # rem_day = [m - day_summary[day][1], a - day_summary[day][2], e - day_summary[day][3]]
        # ord = np.argsort(rem_day)
        # temp = [ord[2]+1, ord[1]+1, ord[0]+1]
        temp = [1, 3, 2]
        if day_summary[day][0] >= N-(m+a+e):
            temp = temp + [0]
        elif week_summary[int(day/7)][nurse][0]>0:
            temp = temp + [0]
        else:
            temp = [0] + temp
        sol = []
        for val in temp:
            if val in domains:
                sol.append(val)
        return sol
    else:
        if nurse>=S:
            temp = [1, 3, 2]
            if day_summary[day][0] >= N-(m+a+e):
                temp = temp + [0]
            elif week_summary[int(day/7)][nurse][0]>0:
                temp = temp + [0]
            else:
                temp = [0] + temp
            sol = []
            for val in temp:
                if val in domains:
                    sol.append(val)
            return sol
        else:
            temp = [1, 3, 2]
            total_weeks = (D+6)//7
            current_week = day//7
            if (D%7 != 0 and total_weeks == current_week+1):
                temp = temp + [0]
            elif day_summary[day][0] >= N-(m+a+e):
                temp = temp + [0]
            elif week_summary[int(day/7)][nurse][0]>0:
                temp = temp + [0]
            else:
                temp = [0] + temp
            sol = []
            for val in temp:
                if val in domains:
                    sol.append(val)
            return sol 

def cspA(N, D, m, a, e):
    global assigned_var, unassigned_var, domains, assignments, week_summary, day_summary
    if len(unassigned_var) == 0:    
        return True, assignments
    # print(len(assigned_var))
    var = getUnassignedVar(unassigned_var, domains, D, "A")
    assigned_var.add(var)
    unassigned_var.remove(var)
    nurse, day = int(var/D), var%D
    week = int(day/7)
    req = [N-(m+a+e), m, a, e]
    for val in order(domains[var], nurse, day, N, D, m, a, e, "A"):
        if isConsistent(var, val, N, D, m, a, e):   
            if day_summary[day][val] + 1 > req[val]:
                continue
            assignments[nurse][day] = val
            week_summary[week][nurse][val] += 1
            day_summary[day][val] += 1
            
            ########## INFERENCE ###########
            
            deleted = False
            flag = False
            flagDel = []
            if day+1<D and (val == 3 or val==1) and ((var+1) in unassigned_var) and (1 in domains[var+1]):
                domains[var+1].remove(1)
                deleted = True
            if (req[0]+req[2] == req[1]) and (val==0 or val==2) and day+1<D and ((var+1) in unassigned_var):
                flag = True
                for i in (0,2,3):
                    if i in domains[var+1]:
                        domains[var+1].remove(i)
                        flagDel.append(i)
            
            result, assigns = cspA(N, D, m,a,e)
            if result:
                return (result, assigns)
            
            assignments[nurse][day] = -1
            week_summary[week][nurse][val] -= 1
            day_summary[day][val] -= 1
            if deleted:
                domains[var+1].append(1)
            if flag:
                for i in flagDel:
                    domains[var+1].append(i)

    assigned_var.remove(var)
    unassigned_var.add(var)
    return False, assignments
    

def partA_csp(N, D, m, a, e):
    n_rest = N-(m+a+e)
    if (m+a+e>N):
        print("NO-SOLUTION")
        return False, {}
    if (D>=7 and 7*(m+a+e) > 6*N):
        print("NO-SOLUTION")
        return False, {}
    if (D>1 and n_rest + a < m):
        print("NO-SOLUTION")
        return False, {}
    if (D >= 7 and 7*n_rest < N):
        print("NO-SOLUTION")
        return False, {}
    
    global assigned_var, unassigned_var, domains, assignments, week_summary, day_summary
    assigned_var = set([])
    unassigned_var = set([i for i in range(N*D)])
    domains = [[0,1,2,3] for i in  range(N*D)]
    assignments = [[-1 for i in range(D)] for j in range(N)]
    week_summary = [[[0,0,0,0] for i in range(N)] for j in range(int((D+6)/7))]
    day_summary = [[0,0,0,0] for i in range(D)]
    result, assigned =  cspA(N, D, m, a, e)
    if result:
        # print_screen(assignments, N, D, m, a, e)
        print_outputFile(assignments,N, D, m, a, e)
    else:
        print("NO-SOLUTION")
    return result, assigned


def permute(S, assignments):
    curr_score = 0
    score_list = []
    for i in range(len(assignments)):
        cr_score = 0
        for j in range(len(assignments[0])):
            if assignments[i][j] == 1 or assignments[i][j] == 3:
                cr_score += 1
        score_list.append((cr_score, i))
    score_list.sort()
    permuted_assignment = []
    n = len(assignments)
    for i in range(n):
        permuted_assignment.append(assignments[score_list[n-i-1][1]])
        if i<S:
            curr_score += score_list[n-i-1][0]
    return curr_score, permuted_assignment

def getScore(ass, S):
    score = 0
    for i in range(S):
        for j in range(len(ass[i])):
            if ass[i][j] == 1 or ass[i][j] == 3:
                score += 1
    return score
    

def cspB(N, D, m, a, e, S, score, T, start):
    global assigned_var, unassigned_var, domains, assignments, week_summary, day_summary, bestScore
    if (time.time()-start>= T):
        if bestScore == -1:
            print("NO-SOLUTION") 
        sys.exit()

    if len(unassigned_var) == 0:
        permutedScore, permutedAssignment = permute(S, assignments)
        if permutedScore> bestScore:
            bestScore = permutedScore
            print(permutedScore)  
            print(getScore(permutedAssignment, S))
            # print_screen(permutedAssignment,N,D,m,a,e)
            # print()
            # print_screen(assignments,N,D,m,a,e)
            print_outputFile(permutedAssignment, N, D, m, a, e)
        return
    
    var = getUnassignedVar(unassigned_var, domains, D, "B", S)
    assigned_var.add(var)
    unassigned_var.remove(var)
    nurse, day = int(var/D), var%D
    week = int(day/7)
    req = [N-(m+a+e), m, a, e]
    for val in order(domains[var], nurse, day, N, D, m, a, e, "B", S):
        if isConsistent(var, val, N, D, m, a, e):   
            if day_summary[day][val] + 1 > req[val]:
                continue
            assignments[nurse][day] = val
            week_summary[week][nurse][val] += 1
            day_summary[day][val] += 1
            temp_score = score
            if nurse<S and (val == 1 or val == 3):
                temp_score = score + 1
            
            ########## INFERENCE ###########
            
            deleted = False
            flag = False
            flagDel = []
            if day+1<D and (val == 3 or val==1) and ((var+1) in unassigned_var) and (1 in domains[var+1]):
                domains[var+1].remove(1)
                deleted = True
            if (req[0]+req[2] == req[1]) and (val==0 or val==2) and day+1<D and ((var+1) in unassigned_var):
                flag = True
                for i in (0,2,3):
                    if i in domains[var+1]:
                        domains[var+1].remove(i)
                        flagDel.append(i)



            cspB(N, D, m, a, e, S, temp_score, T, start)
            
            assignments[nurse][day] = -1
            week_summary[week][nurse][val] -= 1
            day_summary[day][val] -= 1
            if deleted:
                domains[var+1].append(1)
            if flag:
                for i in flagDel:
                    domains[var+1].append(i)

    assigned_var.remove(var)
    unassigned_var.add(var)


def partB_csp(N, D, m, a, e, S, T, start):
    n_rest = N-(m+a+e)
    if (m+a+e>N):
        print("NO-SOLUTION")
        return False, {}
    if (D>=7 and 7*(m+a+e) > 6*N):
        print("NO-SOLUTION")
        return False, {}
    if (D>1 and n_rest + a < m):
        print("NO-SOLUTION")
        return False, {}
    if (D>=7 and 7*n_rest < N):
        print("NO-SOLUTION")
        return False, {}

    global assigned_var, unassigned_var, domains, assignments, week_summary, day_summary, bestScore
    bestScore = -1
    assigned_var = set([])
    unassigned_var = set([i for i in range(N*D)])
    domains = [[0,1,2,3] for i in  range(N*D)]
    assignments = [[-1 for i in range(D)] for j in range(N)]
    week_summary = [[[0,0,0,0] for i in range(N)] for j in range(int((D+6)/7))]
    day_summary = [[0,0,0,0] for i in range(D)]
    cspB(N, D, m, a, e, S, 0, T, start)
    if bestScore == -1:
        print("NO-SOLUTION")
    
    


def print_screen(assignments, N, D, m, a, e):
    for i in range(N):
        for j in range(D):
            print(val_map[assignments[i][j]], end = " ")
        print()

def print_outputFile(assignments, N, D, m, a, e):
    shift = {0: "R", 1: "M", 2: "A", 3: "E"}
    dic = {}
    for i in range(N):
        for j in range(D):
            key = "N" + str(i) + "_" + str(j)
            dic[key] = shift[assignments[i][j]]
    with open("solution.json", "w") as outfile:
        json.dump(dic,outfile)  
    


if __name__ == '__main__':
    input_file = sys.argv[1]
    input_data = pd.read_csv(input_file).values
    if input_data.shape[1] == 5:
        question = 'A'
    else:
        question = 'B'
    with open("solution.json", "w") as outfile:
        json.dump({},outfile)  
    if question == 'A':
        for i in range(input_data.shape[0]):
            N, D, m, a, e = list(map(int,input_data[i, :]))
            start = time.time()
            result, assignments = partA_csp(N, D, m, a, e)
            end = time.time()
            # print("Time taken: " +str(end-start) + " sec")
    
    else:
        for i in range(input_data.shape[0]):
            N, D, m, a, e, S, T  = list(map(int,input_data[i, :]))
            #print(N, D, m, a, e, S, T)
            start = time.time()
            partB_csp(N, D, m, a, e, S, T, start)
            end = time.time()
            # print("Time taken: " +str(end-start) + " sec")







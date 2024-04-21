import numpy as np
import skfuzzy as skf
from MFIS_Classes import *
from MFIS_Read_Functions import *
import matplotlib.pyplot as plt

inputs = readFuzzySetsFile('InputVarSets.txt')
inputs.printFuzzySetsDict()
risks = readFuzzySetsFile('Risks.txt')
# risks.printFuzzySetsDict()
rules = readRulesFile('Rules.txt')
rules.printRuleList()
apps = readApplicationsFile('Applications.txt')
# for app in apps:
#     print(app.data)

colors = ['b', 'g', 'r', 'c', 'm', 'y']
col_cnt = 0

age_sets = {}
inc_sets = {}
ass_sets = {}
amt_sets = {}
job_sets = {}
hist_sets = {}
for set in inputs:
    if "Age" in set:
        age_sets.update( { set : inputs.get(set) } )
    elif "IncomeLevel" in set:
        inc_sets.update( { set : inputs.get(set) } )
    elif "Assets" in set:
        ass_sets.update( { set : inputs.get(set) } )
    elif "Amount" in set:
        amt_sets.update( { set : inputs.get(set) } )
    elif "Job" in set:
        job_sets.update( { set : inputs.get(set) } )
    elif "History" in set:
        hist_sets.update( { set : inputs.get(set) } )

def plotSet(set):
    col_cnt = 0
    for var in set:
        fuzz = set.get(var)
        plt.plot(fuzz.x, fuzz.y, colors[col_cnt])
        col_cnt += 1

# Plot for Age
plt.subplot(3, 2, 1)  # Subplot with 3 rows, 2 columns, and this being the first plot
plotSet(age_sets)
plt.title('Age Sets')

# Plot for Income
plt.subplot(3, 2, 2)  # Subplot with 3 rows, 2 columns, and this being the second plot
plotSet(inc_sets)
plt.title('Income Sets')

# Plot for Assets
plt.subplot(3, 2, 3)  # Subplot with 3 rows, 2 columns, and this being the third plot
plotSet(ass_sets)
plt.title('Asset Sets')

# Plot for Amount
plt.subplot(3, 2, 4)  # Subplot with 3 rows, 2 columns, and this being the fourth plot
plotSet(amt_sets)
plt.title('Amount Sets')

# Plot for Job
plt.subplot(3, 2, 5)  # Subplot with 3 rows, 2 columns, and this being the fifth plot
plotSet(job_sets)
plt.title('Job Sets')

# Plot for History
plt.subplot(3, 2, 6)  # Subplot with 3 rows, 2 columns, and this being the sixth plot
plotSet(hist_sets)
plt.title('History Sets')

plt.tight_layout()  # Adjust layout to prevent overlap


def calcVars(val, sets):
    vars = {}
    for tag in sets:
        set = sets.get(tag)
        if val == set.x[-1] + 1:
            val -= 1
        vars.update({ tag: set.y[val] })
    return vars

def calcMembScore(app):
    data_sets = [age_sets, inc_sets, ass_sets, amt_sets, job_sets, hist_sets]
    member_vals = {}
    
    for data, data_set in zip(app.data, data_sets):
        var = calcVars(data[1], data_set)
        member_vals.update(var)
        
    return member_vals

def calcRiskValues(scores):
    return

apps[0].printApplication()
print(calcMembScore(apps[0]))
calcRiskValues(calcMembScore(apps[0]))

# plt.show()


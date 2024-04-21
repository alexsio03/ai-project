import numpy as np
import skfuzzy as skf
from MFIS_Classes import *
from MFIS_Read_Functions import *
import matplotlib.pyplot as plt

inputs = readFuzzySetsFile('InputVarSets.txt')
# inputs.printFuzzySetsDict()
risks = readFuzzySetsFile('Risks.txt')
# risks.printFuzzySetsDict()
rules = readRulesFile('Rules.txt')
# rules.printRuleList()
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
risk_sets = {}
for risk in risks:
    risk_sets.update( { risk: risks.get(risk) }) 

def plotSet(set):
    col_cnt = 0
    for var in set:
        fuzz = set.get(var)
        plt.plot(fuzz.x, fuzz.y, colors[col_cnt])
        col_cnt += 1

# # Plot for Age
# plt.subplot(4, 2, 1)  # Subplot with 3 rows, 2 columns, and this being the first plot
# plotSet(age_sets)
# plt.title('Age Sets')

# # Plot for Income
# plt.subplot(4, 2, 2)  # Subplot with 3 rows, 2 columns, and this being the second plot
# plotSet(inc_sets)
# plt.title('Income Sets')

# # Plot for Assets
# plt.subplot(4, 2, 3)  # Subplot with 3 rows, 2 columns, and this being the third plot
# plotSet(ass_sets)
# plt.title('Asset Sets')

# # Plot for Amount
# plt.subplot(4, 2, 4)  # Subplot with 3 rows, 2 columns, and this being the fourth plot
# plotSet(amt_sets)
# plt.title('Amount Sets')

# # Plot for Job
# plt.subplot(4, 2, 5)  # Subplot with 3 rows, 2 columns, and this being the fifth plot
# plotSet(job_sets)
# plt.title('Job Sets')

# # Plot for History
# plt.subplot(4, 2, 6)  # Subplot with 3 rows, 2 columns, and this being the sixth plot
# plotSet(hist_sets)
# plt.title('History Sets')

# plt.subplot(4, 2, 7)
# plotSet(risk_sets)
# plt.title('Risk Sets')

# plt.tight_layout()  # Adjust layout to prevent overlap


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

def calcRuleValues(scores):
    risk_scores = []
    rule_vals = {}
    for rule in rules:
        for ant in rule.antecedent:
            risk_scores.append(scores.get(ant))
        rule_vals.update( { rule.ruleName: [rule.consequent, min(risk_scores)] })
        risk_scores = []
    return rule_vals

def calcRisks(rules):
    low = []
    medium = []
    high = []
    for rule in rules:
        val = rules.get(rule)
        if 'Low' in val[0]:
            low.append(val[1])
        if 'Medium' in val[0]:
            medium.append(val[1])
        if 'High' in val[0]:
            high.append(val[1])
    return [max(low), max(medium), max(high)]

def calc_defuzz(risk_mins):
    # Defuzzify using scikit-fuzzy
    risk_values = ['Low', 'Medium', 'High']
    risk_mins_array = np.array(risk_mins)
    defuzz_value = skf.defuzz(np.arange(3), risk_mins_array, 'centroid')

    # Print the defuzzified value
    print("Defuzzified Risk:", risk_values[int(defuzz_value)])

def get_risk_value(app):
    scores = calcMembScore(app)
    rule_vals = calcRuleValues(scores)
    risk_mins = calcRisks(rule_vals)
    calc_defuzz(risk_mins)
    app.printApplication()

for app in apps:
    get_risk_value(app)

# plt.show()


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

show_plots = False

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
    risk_strs = ['Low', 'Medium', 'High']
    x = risks.get('Risk=LowR').x
    low_ad = risks.get('Risk=LowR').a_d
    med_ad = risks.get('Risk=MediumR').a_d
    high_ad = risks.get('Risk=HighR').a_d
    mf1 = skf.trapmf(x, low_ad)
    mf2 = skf.trapmf(x, med_ad)
    mf3 = skf.trapmf(x, high_ad)
    print(risk_mins)
    mf1_weighted = risk_mins[0] * mf1
    mf2_weighted = risk_mins[1] * mf2
    mf3_weighted = risk_mins[2] * mf3

    # Element-wise maximum
    mf = np.maximum(mf2_weighted, np.maximum(mf1_weighted, mf3_weighted))
    plotSet(risk_sets)
    plt.title('Risk Sets')
    plt.show()
    xCentroid = skf.defuzz(x,mf,'centroid')
    print(int(xCentroid))
    membs = list(calcVars(int(xCentroid), risk_sets).values())
    print(membs)
    max_memb = 0
    for i in range(len(membs)):
        if membs[i] > membs[max_memb]:
            max_memb = i
    plt.axvline(x=xCentroid, ymin=-0.2, ymax=1.2, color='k')
    plt.plot(x, mf, 'k')
    plt.show()

    # Print the defuzzified value
    return "Risk Value: " + risk_strs[max_memb]

# MAIN FUNCTION
def get_risk_value(app):
    scores = calcMembScore(app)
    rule_vals = calcRuleValues(scores)
    risk_mins = calcRisks(rule_vals)
    print("Applicant " + app.appId,  calc_defuzz(risk_mins))

get_risk_value(apps[33])
# for app in apps:
#     get_risk_value(app)


# --------------------------------

if show_plots:
    # Plot for Age
    plt.subplot(4, 2, 1)  # Subplot with 3 rows, 2 columns, and this being the first plot
    plotSet(age_sets)
    plt.title('Age Sets')

    # Plot for Income
    plt.subplot(4, 2, 2)  # Subplot with 3 rows, 2 columns, and this being the second plot
    plotSet(inc_sets)
    plt.title('Income Sets')

    # Plot for Assets
    plt.subplot(4, 2, 3)  # Subplot with 3 rows, 2 columns, and this being the third plot
    plotSet(ass_sets)
    plt.title('Asset Sets')

    # Plot for Amount
    plt.subplot(4, 2, 4)  # Subplot with 3 rows, 2 columns, and this being the fourth plot
    plotSet(amt_sets)
    plt.title('Amount Sets')

    # Plot for Job
    plt.subplot(4, 2, 5)  # Subplot with 3 rows, 2 columns, and this being the fifth plot
    plotSet(job_sets)
    plt.title('Job Sets')

    # Plot for History
    plt.subplot(4, 2, 6)  # Subplot with 3 rows, 2 columns, and this being the sixth plot
    plotSet(hist_sets)
    plt.title('History Sets')

    plt.subplot(4, 2, 7)
    plotSet(risk_sets)
    plt.title('Risk Sets')

    plt.tight_layout()  # Adjust layout to prevent overlap

    plt.show()


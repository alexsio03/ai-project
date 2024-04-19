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
# rules.printRuleList()
apps = readApplicationsFile('Applications.txt')
# for app in apps:
#     app.printApplication()

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

# Plot for Age
plt.subplot(3, 2, 1)  # Subplot with 3 rows, 2 columns, and this being the first plot
col_cnt = 0
for age in age_sets:
    age_fuzz = age_sets.get(age)
    plt.plot(age_fuzz.x, age_fuzz.y, colors[col_cnt])
    col_cnt += 1
plt.title('Age Sets')

# Plot for Income
plt.subplot(3, 2, 2)  # Subplot with 3 rows, 2 columns, and this being the second plot
col_cnt = 0
for income in inc_sets:
    inc_fuzz = inc_sets.get(income)
    plt.plot(inc_fuzz.x, inc_fuzz.y, colors[col_cnt])
    col_cnt += 1
plt.title('Income Sets')

# Plot for Assets
plt.subplot(3, 2, 3)  # Subplot with 3 rows, 2 columns, and this being the third plot
col_cnt = 0
for asset in ass_sets:
    asset_fuzz = ass_sets.get(asset)
    plt.plot(asset_fuzz.x, asset_fuzz.y, colors[col_cnt])
    col_cnt += 1
plt.title('Asset Sets')

# Plot for Amount
plt.subplot(3, 2, 4)  # Subplot with 3 rows, 2 columns, and this being the fourth plot
col_cnt = 0
for amount in amt_sets:
    amt_fuzz = amt_sets.get(amount)
    plt.plot(amt_fuzz.x, amt_fuzz.y, colors[col_cnt])
    col_cnt += 1
plt.title('Amount Sets')

# Plot for Job
plt.subplot(3, 2, 5)  # Subplot with 3 rows, 2 columns, and this being the fifth plot
col_cnt = 0
for job in job_sets:
    job_fuzz = job_sets.get(job)
    plt.plot(job_fuzz.x, job_fuzz.y, colors[col_cnt])
    col_cnt += 1
plt.title('Job Sets')

# Plot for History
plt.subplot(3, 2, 6)  # Subplot with 3 rows, 2 columns, and this being the sixth plot
col_cnt = 0
for history in hist_sets:
    hist_fuzz = hist_sets.get(history)
    plt.plot(hist_fuzz.x, hist_fuzz.y, colors[col_cnt])
    col_cnt += 1
plt.title('History Sets')

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

import os
import openai
from openai import OpenAI
import pandas as pd
from Ultimatum_Function import ultimatum_game
from LauryHoltSingle import laurylotterysingle
import random
import numpy as np


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ages



# Names
names = pd.read_csv("Surnames.csv")
surnames = names[["Last Name"]]


numprompts = 50

younger_ages = np.round(np.random.normal(loc = 31.9, scale = 4.7, size = numprompts))
older_ages = np.round(np.random.normal(loc = 71.2, scale = 8.4, size = numprompts))

player1 = random.sample(range(453), numprompts)
#player2s = random.sample(range(453), numprompts)


title1 = np.random.choice([0, 1], size=numprompts, replace=True)
#title2s = np.random.choice([0, 1], size=numprompts, replace=True)
titles = ["Mr.", "Ms."]

payouts = pd.read_csv("Laury-Holt-Payouts.csv")

# Probability Processing 
payouts['AProbability1'] = payouts['AProbability1'].apply(lambda x: f"{int(x*100)}%")
payouts['AProbability2'] = payouts['AProbability2'].apply(lambda x: f"{int(x*100)}%")
payouts['BProbability1'] = payouts['BProbability1'].apply(lambda x: f"{int(x*100)}%")
payouts['BProbability2'] = payouts['BProbability2'].apply(lambda x: f"{int(x*100)}%")
payouts['APayout1'] = "$" + (payouts['APayout1']*10).astype(str) + ".00"
payouts['APayout2'] = "$" + (payouts['APayout2']*10).astype(str) + ".00"
payouts['BPayout1'] = "$" + (payouts['BPayout1']*10).astype(str) + "0"
payouts['BPayout2'] = "$" + (payouts['BPayout2']*10).astype(str) + ".00"


formatted_df = pd.DataFrame()
formatted_df["Choice"] = payouts["Round"]
formatted_df["Option A"] = payouts["AProbability1"] + " chance of winning " + payouts["APayout1"] + ", " + payouts["AProbability2"] + " chance of winning " + payouts["APayout2"]
formatted_df["Option B"] = payouts["BProbability1"] + " chance of winning " + payouts["BPayout1"] + ", " + payouts["BProbability2"] + " chance of winning " + payouts["BPayout2"]

payouts = payouts.drop(columns=["ExpectedPayoutA", "ExpectedPayoutB", "RelativePayoutA"])


#markdown_table = payouts.to_markdown(index=False)
#print(markdown_table)

def count_alternations(s):
    count = 0
    for i in range(1, len(s)):
        if s[i] != s[i - 1]:  # Check if current char is different from the previous one
            count += 1
    return count

invalid_response = 0
num_safe_choices = []
response_array = None

for i in range(0, len(player1)):
    responses = []
    for round in formatted_df["Choice"]:
        response = laurylotterysingle(client = client, player1 = surnames.loc[player1[i], "Last Name"], title1 = titles[title1[i]], 
                            payoutmatrix = formatted_df, round = round, age = older_ages[i])
        responses.append(response)
    if count_alternations(responses) > 1:
        invalid_response += 1
    else:
        count_A = responses.count("A")
        num_safe_choices.append(count_A)
    response_array_new = np.array(list(responses))
    print(response_array_new)
    if response_array is None:
        response_array = response_array_new  # First iteration
    else:
        response_array = np.vstack([response_array, response_array_new])  # Stack correctly

print(response_array)
mask = response_array == 'A'
rates = np.sum(mask, axis = 0)
rates = rates/numprompts
print(rates)
print(invalid_response/numprompts)
print(num_safe_choices)


import matplotlib.pyplot as plt

# Example data
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

plt.scatter(x, rates, color='red', label='Data Points')  # Scatter plot
plt.plot(x, rates, color='blue', linestyle='-', marker='o', label='Connected Line')  # Line connecting points

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Scatter Plot Connected by Lines")
plt.legend()
plt.grid(True)

plt.show()






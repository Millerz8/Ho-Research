import os
import openai
from openai import OpenAI
import pandas as pd
from Ultimatum_Function import ultimatum_game
from LauryHolt import laurylottery
import matplotlib.pyplot as plt
from LauryHoltPlayground import laurylotteryplayground

import random
import numpy as np


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

niter = 100

# Names
names = pd.read_csv("Surnames.csv")
surnames = names[["Last Name"]]


# Ages
younger_ages = np.round(np.random.normal(loc = 31.9, scale = 4.7, size = niter))
older_ages = np.round(np.random.normal(loc = 71.2, scale = 8.4, size = niter))

player1 = random.sample(range(453), niter)
#player2s = random.sample(range(453), numprompts)


title1 = np.random.choice([0, 1], size = niter, replace=True)
#title2s = np.random.choice([0, 1], size=numprompts, replace=True)
titles = ["Mr.", "Ms."]

payouts = pd.read_csv("Laury-Holt-Payouts.csv")

# Probability Processing 
payouts['AProbability1'] = payouts['AProbability1'].apply(lambda x: f"{int(x*100)}%")
payouts['AProbability2'] = payouts['AProbability2'].apply(lambda x: f"{int(x*100)}%")
payouts['BProbability1'] = payouts['BProbability1'].apply(lambda x: f"{int(x*100)}%")
payouts['BProbability2'] = payouts['BProbability2'].apply(lambda x: f"{int(x*100)}%")
payouts['APayout1'] = "$" + (payouts['APayout1']).astype(str) + ".00"
payouts['APayout2'] = "$" + (payouts['APayout2']).astype(str) + ".00"
payouts['BPayout1'] = "$" + (payouts['BPayout1']).astype(str) + "0"
payouts['BPayout2'] = "$" + (payouts['BPayout2']).astype(str) + ".00"

# Switching "A" and "B" labels to confuse chat
formatted_df = pd.DataFrame()
formatted_df["Choice"] = payouts["Round"]
formatted_df["Option A"] = payouts["AProbability1"] + " chance of winning " + payouts["APayout1"] + ", " + payouts["AProbability2"] + " chance of winning " + payouts["APayout2"]
formatted_df["Option B"] = payouts["BProbability1"] + " chance of winning " + payouts["BPayout1"] + ", " + payouts["BProbability2"] + " chance of winning " + payouts["BPayout2"]

payouts = payouts.drop(columns=["ExpectedPayoutA", "ExpectedPayoutB", "RelativePayoutA"])


responses = []

for i in range(0, niter):

    response = laurylotteryplayground(client = client, player1 = surnames.loc[player1[i], "Last Name"], title1 = titles[title1[i]], 
                            payoutmatrix = formatted_df, age = younger_ages[i])
    print(response)
    responses.append(response)


numbers = list(map(int, responses))
numbers_array = np.array(numbers)
print(numbers)
rates = []

for i in range(1,11):

    rates.append(np.sum(numbers_array > i))

rates_array = np.array(rates)
rates_array = rates_array/niter*100
print(rates_array)
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

plt.scatter(x, rates_array, color='red')  # Scatter plot
plt.plot(x, rates_array, color='blue', linestyle='-', marker='o')  # Line connecting points

plt.xlabel("Round #")
plt.ylabel("Percentage of Responses Choosing A")
plt.title("Percentage of Responses Choosing A by Round, " + str(niter) + " Samples")
plt.grid(True)

plt.show()






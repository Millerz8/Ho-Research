import os
import openai
from openai import OpenAI
import pandas as pd
from Ultimatum_Function import ultimatum_game
from LauryHoltCorrect import laurylotterycorrect
import matplotlib.pyplot as plt

import random
import numpy as np

# This will just take ask the computer to complete the lottery without role playing 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
niter = 100

for i in range(0, niter):
    response = laurylotterycorrect(client = client, payoutmatrix = formatted_df)
    responses.append(response)


numbers = list(map(int, responses))
numbers_array = np.array(numbers)
print(numbers)
rates = []

for i in range(1,11):

    rates.append(np.sum(numbers_array > i))

rates_array = np.array(rates)
rates_array = rates_array/niter
print(rates_array)


x = [1,2,3,4,5,6,7,8,9,10]

plt.scatter(x, rates, color='red')  # Scatter plot
plt.plot(x, rates, color='blue', linestyle='-', marker='o')  # Line connecting points

plt.xlabel("Round #")
plt.ylabel("Percentage of Responses Choosing A")
plt.title("Percentage of Responses Choosing A by Round, 100 Samples")
plt.grid(True)

plt.show()








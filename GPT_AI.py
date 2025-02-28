import os
import openai
from openai import OpenAI
import pandas as pd
from Ultimatum_Function import ultimatum_game
import random
import numpy as np


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

names = pd.read_csv("Surnames.csv")
surnames = names[["Last Name"]]

numprompts = 60

player1s = random.sample(range(453), numprompts)
player2s = random.sample(range(453), numprompts)


title1s = np.random.choice([0, 1], size=numprompts, replace=True)
title2s = np.random.choice([0, 1], size=numprompts, replace=True)
titles = ["Mr.", "Ms."]

names =[]
yescount = 0
for i in range(0, len(player1s)):
    response = ultimatum_game(client, player1 = surnames.loc[player1s[i], "Last Name"], title1 = titles[title1s[i]], player2 = surnames.loc[player2s[i], "Last Name"], title2 = titles[title2s[i]])
    if response == "Yes.":
        yescount += 1

acceptrate = yescount/numprompts
print(acceptrate)





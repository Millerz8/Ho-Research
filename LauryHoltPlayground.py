import os
import openai
from openai import OpenAI
import pandas as pd


def laurylotteryplayground(client, player1, title1, payoutmatrix, age):
    age = int(age)
    player1 = title1 + " " + player1
    if title1 == "Mr.":
        pronoun = "man"
    else:
        pronoun = "woman"
    
    prompt1 = f"""
    Imagine a typical {age}-year-old American {pronoun} named {player1}.
    Think about how a person with this profile might approach risk and decision-making.

    You will now participate in a series of 10 independent lottery choices. For each round, you will be presented with two options: Option A and Option B. Each option has a potential payout and an associated probability of winning, shown as a percentage.

    Each lottery is independent, meaning your choice in one round should not affect your choices in others.

    Below are the details for each round:

    """

    prompt2_lines = "\n"
    prompt2_lines = [
        f"Round {round}: Option A: {payoutmatrix['Option A'][round-1]}. Option B: {payoutmatrix['Option B'][round-1]}."
        for round in payoutmatrix["Choice"]
    ]
    prompt2 = "\n".join(prompt2_lines) + "\n"

    prompt3 = f"""

    Now, imagine how a person like {player1} would behave:

    They can choose Option A in rounds 1 through <x1>, and then switch to Option B in rounds <x1 + 1> through 10.

    Based on the payoff structure above, what is the most likely value of <x1> that such a person would choose?

    Only reply with a single integer between 1 and 10. Do not include any explanation or other text.
    """

    prompt = prompt1 + prompt2 + prompt3
    print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
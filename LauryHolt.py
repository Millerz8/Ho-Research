import os
import openai
from openai import OpenAI
import pandas as pd


def laurylottery(client, player1, title1, payoutmatrix, age):
    age = int(age)
    player1 = title1 + " " + player1
    if title1 == "Mr.":
        pronoun = "man"
    else:
        pronoun = "woman"
    
    prompt1 = f"""

    Imagine a typical {age} year-old American {pronoun} named {player1}. 
    Consider the risk preferences and decision-making processes of a person with these characteristics.
  
    We will show you two options for each lottery round, and you will choose which option you want.
    For each lottery, each option will have different potential earnings, with a chance to earn, showing as a percentage under each option.
    Each of the selections will be independent, that is, for each lottery, your choice should be independent of the previous and following lotteries.
    Here are lotteries with options A and B.
    You can choose to play A or B and get the payment following the rules below.
    You can choose option A from round <1> to round <x1>,
    choose option B from round <x+1> to row 10.

    """

    prompt2_lines = "\n"
    prompt2_lines = [
        f"Round {round}: Option A: {payoutmatrix['Option A'][round-1]}. Option B: {payoutmatrix['Option B'][round-1]}."
        for round in payoutmatrix["Choice"]
    ]
    prompt2 = "\n".join(prompt2_lines) + "\n"

    prompt3 = f"""

    Answer me with the value of <x1> only, please remember <x1>should be larger and equal to 1, less and equal to 10, do not explain.

    """
    prompt = prompt1 + prompt2 + prompt3
    print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
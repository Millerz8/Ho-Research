import os
import openai
from openai import OpenAI
import pandas as pd


def laurylotterycorrect(client, payoutmatrix, title1, player1):
    player1 = title1 + " " + player1
    if title1 == "Mr.":
        pronoun = "man"
    else:
        pronoun = "woman"
    prompt1 = f"""

    Imagine a typical American {pronoun} named {player1}. 
    Consider the risk preferences and decision-making processes of a person with these characteristics.
  
    We will show you two options for each lottery round, and you will choose which option you want.
    For each lottery, each option will have different potential earnings, with a chance to earn, showing as a percentage under each option.
    Each of the selections will be independent, that is, for each lottery, your choice should be independent of the previous and following lotteries.
    Here are lotteries with options A and B.
    You can choose to play A or B and get the payment following the rules below.
    You can choose option A from round 1 to round x,
    choose option B from round x+1 to round 10.
    If you want to choose B for all rounds, respond with 0. 
    """
    prompt2_lines = "\n"
    prompt2_lines = [
        f"Round {round}: Option A: {payoutmatrix['Option A'][round-1]}. Option B: {payoutmatrix['Option B'][round-1]}."
        for round in payoutmatrix["Choice"]
    ]
    prompt2 = "\n".join(prompt2_lines) + "\n"

    prompt3 = f"""

    Answer me with the value of x only, please remember x should be larger and equal to 0, less and equal to 10. 
    Remember x is the LAST round that the person chooses A, after selecting A for round x, they will select B for round x + 1 and Everything after that.
    Only answer with you value for x, don't explain your answer. 

    """
    prompt = prompt1 + prompt2 + prompt3
 

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
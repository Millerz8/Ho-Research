import os
import openai
from openai import OpenAI
import pandas as pd


def laurylotterysingle(client, player1, title1, payoutmatrix, age, round):
    age = int(age)
    player1 = title1 + " " + player1
    if title1 == "Mr.":
        pronoun = "man"
    else:
        pronoun = "woman"

    prompt1 = f"""

    You are {player1}, a {age} year-old American {pronoun}. 

    You have been asked to participate in a survey in which you can choose between an Option A, and Option B.  

    """
    prompt2 = f"""
    - **Option A:** {payoutmatrix['Option A'][round-1]}  
    - **Option B:** {payoutmatrix['Option B'][round-1]}
    """

    prompt3 = f"""

    Indicate your choice of either 'A' or 'B'. Your answer should have a length of one character. 

    """
    prompt = prompt1 + prompt2 + prompt3
    #print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
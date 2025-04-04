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

    You are {player1}, a {age} year-old American {pronoun}. 

    You have been asked to participate in a survey with 10 rounds. For each round, you can choose either option A or option B. You will receive real money with the stated probabilities shown below.

    """
    prompt2_lines = "\n"
    prompt2_lines = [
        f"Round {round}: Option A: {payoutmatrix['Option A'][round-1]}. Option B: {payoutmatrix['Option B'][round-1]}."
        for round in payoutmatrix["Choice"]
    ]
    prompt2 = "\n".join(prompt2_lines) + "\n"

    prompt3 = f"""
    Indicate your choice A or B for each round.
    Write your choices (A or B) in order from Round 1 to Round 10, no commas or spaces, don't explain yourself. Think carefully, and remember that a logical response should not switch between A and B or B and A more than once. Your response should only be 10 characters"""

    prompt = prompt1 + prompt2 + prompt3
    print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
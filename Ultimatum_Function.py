import os
import openai
from openai import OpenAI
import pandas as pd

#api_key = os.getenv("OPENAI_API_KEY")
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#client = OpenAI()

def ultimatum_game(client, player1, title1, player2, title2):
    player1 = title1 + " " + player1
    player2 = title2 + " " + player2
    if title1 == "Mr.":
        pronoun = "himself"
    else:
        pronoun = "herself"

    prompt = f"""In the following scenario, {player2} had to decide whether to accept or reject the proposal.

    Scenario: {player1} is given $10. {player1} will propose how to split the money between {pronoun} and {player2}. 
    Then {player2} will decide whether to accept or reject {player1}'s proposal. If {player2} accepts,
    then {player1} and {player2} get the money as they agreed to split. If {player2} rejects, then both receive nothing.

    {player1} takes $6 for {pronoun} and offers {player2} $4.

    With a simple 'yes' or 'no' answer, does {player2} accept the proposal?"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content





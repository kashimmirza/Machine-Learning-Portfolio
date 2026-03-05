import openai
import re
import httpx
from dotenv import load_dotenv
import os

_ = load_dotenv()
from openai import OpenAI
#openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)
chat_completion.choices[0].message.content

class Agent:
    def __init__(self, system="", model="gpt_4-0125-preview", temperature=0):
        self.system = system
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content": system})
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    def execute(self):
        completion = client.chat.completions.create(
                     model=self.model,
                     temperature=self.temperature,
                     messages=self.messages)
        return completion.choices[0].message.content


        prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()
def calculate(what):
    return eval(what)

def average_dog_weight(name):
    if name in "Scottish Terrier": 
        return("Scottish Terriers average 20 lbs")
    elif name in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif name in "Toy Poodle":
        return("a toy poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}

abot = Agent(prompt)

result = abot("How much does a toy poodle weigh?")
print(result)

result = average_dog_weight("Toy Poodle")

result
    

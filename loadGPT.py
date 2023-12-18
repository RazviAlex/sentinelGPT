from openai import OpenAI
import argparse, requests, json, sys, signal, argparse, os

current_directory = os.getcwd()
absolute_path = os.path.join(current_directory, 'outputS1.txt')

#
#https://arxiv.org/pdf/2309.03409.pdf
#
#Observe that:
#• The styles of instructions found by different optimizer LLMs vary a lot: PaLM 2-L-IT and
#text-bison ones are concise, while GPT ones are long and detailed.
#• Although some top instructions contain the “step-by-step” phrase, most others achieve a comparable or better accuracy with different semantic meanings
#• GPT3.5 Turbo optimize prompt: A little bit of arithmetic and a logical approach will help us quickly arrive at the solution to this problem
#• GPT4 Turbo optimize prompt: Let’s combine our numerical command and clear thinking to quickly and accurately decipher the answer.
#• Information about models: https://platform.openai.com/docs/models/overview

def callGPT(event, args):
  modelArguments = args.model

  client = OpenAI()

  if modelArguments == "GPT-3.5T":    
    print("\n\nChatGPT-3.5 Turbo analysis...")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      temperature=0.3,
      messages=[
        {"role": "system", "content": "Given the following set of cybersecurity events which are structed as follows: EventType -> endpoint -> SourceParentProcess -> SourceProcess, etc, your job is to analyse step by step and understand what type of activity has been carried out. These are the events: "+str(event)},
        {"role": "user", "content": "A little bit of arithmetic and a logical approach will help us quickly arrive at the solution to this problem. Analyse each event (one by one and then together) for any observed patterns or anomalies. Answer must be structured as follows: A single paragraph that contains a final conclusion. The conclusion starts with a verdict (malicious (100% sure is a malicious behaviour), suspicious (you are not sure) or benign(you are 100% sure is not a malicious behaviour) ), followed by a short explanation of why this verdict. Finalize with an 'Extra part' where focus on the two most interesting data extracted from events (write the value of those events) that may be anomalous or suspicious."}
      ]
    )
  elif modelArguments == "GPT-4":
    print("\n\nChatGPT-4 analysis...")
    completion = client.chat.completions.create(
      model="gpt-4",
      temperature=0.3,
      messages=[
        {"role": "system", "content": "Given the following set of cybersecurity events which are structed as follows: EventType -> endpoint -> SourceParentProcess -> SourceProcess, etc, your job is to analyse step by step and understand what type of activity has been carried out. These are the events: "+str(event)},
        {"role": "user", "content": "Let’s combine our numerical command and clear thinking to quickly and accurately decipher the answer. Answer must be structured as follows: A single paragraph that contains a final conclusion. The conclusion starts with a verdict (malicious (100% sure is a malicious behaviour), suspicious (you are not sure) or benign(you are 100% sure is not a malicious behaviour) ), followed by an explanation of why this verdict. Finalize with an 'Extra part' where focus on the two most interesting data extracted from events (write the value of those events) that may be anomalous or suspicious."}
      ]
    )

  print(completion.choices[0].message.content)
  #print(completion.choices[1].message.content)


def exportS1Data(args):
  event = []

  with open(absolute_path, 'r') as readfile:
  # Iterate for each row in the file
    for line in readfile:
      event.append(line)

  if args.verbose:
    print(event)

  callGPT(event, args)

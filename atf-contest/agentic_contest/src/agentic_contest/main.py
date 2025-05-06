#!/usr/bin/env python
import sys
import warnings
import os
from crew import AtfContest
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run_contest_agent(question: str):
    # question = input("Enter your question: ")
    inputs = {
        'question': question,
        "HOST": os.getenv("HOSTDB"), 
        "TOKEN": os.getenv("TOKENDB"), 
        "WAREHOUSEID": os.getenv("WAREHOUSEIDDB")
    }
    res = AtfContest(inputs).crew().kickoff(inputs=inputs)
    return res
# run()
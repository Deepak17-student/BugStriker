from fastapi import FastAPI
from fastapi.responses import FileResponse
import json
from runner import run_tests
from evaluator import generate_diagnostic_question, final_evaluation

# 1. Create the app FIRST
app = FastAPI()

# 2. Store state
state = {"code": ""}

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/submit")
async def submit(submission: dict):
    state["code"] = submission["code"]
    with open("rubric.json") as f: rubric = json.load(f)
    results = run_tests(state["code"], rubric["test_cases"])
    
    # Call AI
    question = generate_diagnostic_question(state["code"], results)
    return {"status": "WAITING_FOR_STUDENT", "question": question}

@app.post("/respond")
async def respond(response: dict):
    with open("rubric.json") as f: rubric = json.load(f)
    new_results = run_tests(response["revised_code"], rubric["test_cases"])
    
    # Call AI
    verdict = final_evaluation(state["code"], response["explanation"], response["revised_code"], new_results)
    return {"status": "FINISHED", "verdict": verdict}
from fastapi import FastAPI
from fastapi.responses import FileResponse
import json
from runner import run_tests
from evaluator import generate_diagnostic_question, final_evaluation

app = FastAPI()

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.post("/submit")
async def submit(submission: dict):
    with open("rubric.json") as f: rubric = json.load(f)
    results = run_tests(submission["code"], rubric["test_cases"])
    question = generate_diagnostic_question(submission["code"], results)
    return {"status": "WAITING_FOR_STUDENT", "question": question}

@app.post("/respond")
async def respond(response: dict):
    verdict = final_evaluation("", response["explanation"], response["revised_code"], [])
    return {"status": "FINISHED", "verdict": verdict}
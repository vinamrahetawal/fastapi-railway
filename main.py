from fastapi import FastAPI, Query
from pydantic import BaseModel, EmailStr
import random

app = FastAPI()

Y = [1, 9, 80, 50, 120, 30]
email_data_store = {}

class College(BaseModel):
    Mean: float
    Median: float
    Mode: float
    Count: int
    Min: int
    Max: int
    secret_key: int

@app.get("/input")
def college_data(email: EmailStr = Query(...)):
    secret_key = random.randint(1000000000, 9999999999)
    email_data_store[email] = {
        "secret": secret_key,
        "data": Y
    }
    return {
        "Data": Y,
        "Secret": secret_key
    }

@app.post("/submit")
def submit_data(payload: College, email: EmailStr = Query(...)):
    if email not in email_data_store:
        return {"message": "Email not found. Please call /input first."}
    
    stored = email_data_store[email]
    if payload.secret_key != stored["secret"]:
        return {"message": "Invalid secret key"}

    stats = {
        "Size": payload.Count,
        "Mean": round(payload.Mean, 2),
        "Median": payload.Median,
        "Mode": payload.Mode,
        "Min": payload.Min,
        "Max": payload.Max,
    }

    return {
        "message": "Your response has been submitted successfully",
        "data": stats
    }
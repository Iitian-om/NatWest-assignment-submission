from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from typing import List
import pandas as pd
import os
import json
from .services import generate_report, upload_files
from .auth import authenticate_user

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/upload/")
async def upload_files(input_file: UploadFile = File(...), reference_file: UploadFile = File(...)):
    return await upload_files(input_file, reference_file)

@app.post("/generate_report/")
async def create_report(token: str = Depends(oauth2_scheme)):
    authenticate_user(token)
    report_path = await generate_report()
    return {"report_path": report_path}

@app.get("/download_report/")
async def download_report(report_path: str):
    return FileResponse(report_path)

@app.post("/configure_rules/")
async def configure_rules(rules: dict):
    with open("app/rules.json", "w") as f:
        json.dump(rules, f)
    return {"message": "Rules updated successfully"}
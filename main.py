#!/usr/bin/python3.9
from loguru import logger
import os

import sys, os

from fastapi import FastAPI, HTTPException, UploadFile, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pathlib import Path
from splitcopy import split_by_grupo
from enum import Enum

logger.remove()
logger.add(sys.stderr, level="DEBUG")

app = FastAPI()

async def validate_environment(environment: str = Path()):
    valid_environments = {"pre", "pro"}
    if environment not in valid_environments:
        raise HTTPException(status_code=400, detail="Invalid environment. Allowed values are 'pre' and 'pro'")
    return environment

async def validate_extensions(filename: str):
    if not (filename.endswith(".csv") or filename.endswith(".csv.gz")):
        raise HTTPException(status_code=400, detail="Invalid file extension. Allowed extensions are .csv and .csv.gz")   

@app.get("/", response_class=HTMLResponse)
async def redirect_to_index():
    return RedirectResponse(url="/index")


@app.get("/index", response_class=HTMLResponse)
async def index():
    html_content = """
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    </head>
        <body>
            <h1>para k kieres saber eso jaja saludos!</h1>
            <p>Creo que lo que quieres ver es <a href="/docs">el swagger</a>.</p>
        </body>
    </html>
    """    
    return HTMLResponse(content=html_content)

@app.post("/splitcsv/{environment}", response_class=JSONResponse)
async def splitcsvpre(uploaded_file: UploadFile, environment: str = Depends(validate_environment)):
    validate_extensions(filename=uploaded_file.filename)
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    file_location = os.path.join("uploads", uploaded_file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    splitfiles = split_by_grupo(file_location, environment=environment)
    return splitfiles



from loguru import logger
import os

import sys, os

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pathlib import Path
from splitcopy import split_by_grupo

logger.remove()
logger.add(sys.stderr, level="DEBUG")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def redirect_to_index():
    return RedirectResponse(url="/index")


@app.get("/index", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content="<html><body><h1>Index!</h1></body></html>")

@app.post("/splitcsv", response_class=JSONResponse)
async def splitcsv(uploaded_file: UploadFile):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    file_location = os.path.join("uploads", uploaded_file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    splitfiles = split_by_grupo(file_location)
    return splitfiles

import os
import random
import logging 
from typing import List 

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse 
 
app = FastAPI()

PORT = 8000

if not os.path.exists("../logs"):
    os.mkdir("../logs")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.StreamHandler()
file_handler = logging.FileHandler("../logs/api.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 

@app.post("/create_dummy")
async def image_detect(request: Request):

    if request.method == "POST":
        json_result: List = []
        try:
            json_results: List = [random.randint(1, 100) for _ in range(10)]

            logger.info(["results", json_result])

            return JSONResponse(
                {
                    "data": json_results,
                    "message": "object detected successfully",
                    "errors": None,
                    "status": 200,
                },
                status_code=200,
            )
        except Exception as error:
            logger.error(["process failed", error])
            return JSONResponse(
                {
                    "message": "failed",
                    "errors": "error",
                    "status": 400,
                },
                status_code=400,
            )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
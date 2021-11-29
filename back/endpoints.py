from fastapi import FastAPI
import json
import numpy as np
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request, UploadFile, File
import cv2
import uvicorn
from functionality import Model

# This part of code is needed to make connection of backend and frontend parts
app = FastAPI()
templates = Jinja2Templates(directory="../templates")
app.mount("/front", StaticFiles(directory="../front"), name="front")

# Change the path to your folders
model = Model(model_path="C:/Users/julia/PycharmProjects/anime_classifier/back/resnet_model",
              classes_path="C:/Users/julia/PycharmProjects/anime_classifier/back/class_names.txt")


@app.post("/classify")
async def classify(image: UploadFile = File(...)):

    print("Reading input pic")
    contents = await image.read()
    nparr = np.fromstring(contents, np.uint8)
    input_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    print("Classifying input pic")
    res = cv2.resize(input_img, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
    label = model.predict(res)

    print("Classifying done")
    return {"label": label}


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


if __name__ == "__main__":
    uvicorn.run("endpoints:app", host="127.0.0.1", port=5000, log_level="info")

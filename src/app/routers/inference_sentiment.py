import logging
from typing import List

import numpy as np
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import pipeline

# Set up the router
router = APIRouter()

# Set up logging
LOGGER = logging.getLogger("SentimentAnalysisAPI.inference")

# Load the model
classifier = pipeline("sentiment-analysis", model="stevhliu/my_awesome_model")

# Define the label mapping
LABEL_MAPPING = {
    "LABEL_1": "Positive",
    "LABEL_0": "Negative"
}

class TextInput(BaseModel):
    text: str

class TextOutput(BaseModel):
    label: str
    score: float

@router.post("/inference/get_label", response_model=TextOutput)
async def predict_fakeness(text: TextInput):
    """Make a prediction on the fakeness of a statement."""
    LOGGER.info(f"Received text for analysis: {text.text}")
    try:
        output = classifier(text.text)
        label = LABEL_MAPPING.get(output[0]["label"], "unknown")
        score = output[0]["score"]
        output_model = TextOutput(label=label, score=score)
        LOGGER.info(f"Generated output: {output_model}")
        return output_model
    except Exception as e:
        LOGGER.error(f"Error during prediction: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

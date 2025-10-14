from fastapi import FastAPI

from api.sentiment_analysis import SentimentAnalysisRequest, SentimentAnalysisResponse

from .prediction import load_models, predict

app = FastAPI()
sentence_transformer, classifier = load_models()


@app.post("/inference")
def inference(request: SentimentAnalysisRequest) -> SentimentAnalysisResponse:
    predicton = predict(sentence_transformer, classifier, request.text)
    return SentimentAnalysisResponse(prediction=predicton)

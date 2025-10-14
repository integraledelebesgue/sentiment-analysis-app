import importlib.resources

import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

import models


def load_models() -> tuple[SentenceTransformer, LogisticRegression]:
    with importlib.resources.path(
        models,
        "sentiment-analysis-model",
    ) as models_directory:
        sentence_transformer = SentenceTransformer(
            str(models_directory / "sentence_transformer.model")
        )

        classifier = joblib.load(models_directory / "classifier.joblib")
        assert isinstance(classifier, LogisticRegression)

    return sentence_transformer, classifier


def predict(
    sentence_transformer: SentenceTransformer,
    classifier: LogisticRegression,
    text: str,
) -> str:
    embedding = sentence_transformer.encode(text).reshape(1, -1)
    prediction = classifier.predict(embedding)
    return "positive" if prediction == 1 else "negative"

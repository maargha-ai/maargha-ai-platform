from typing import Dict, List

from gliner import GLiNER

_model = None


def get_gliner_model():
    global _model
    if _model is None:
        _model = GLiNER.from_pretrained("urchade/gliner_small")
    return _model


LABELS = [
    "SKILL",
    "PROGRAMMING_LANGUAGE",
    "FRAMEWORK",
    "TOOL",
    "DATABASE",
    "CLOUD",
    "DEGREE",
    "ROLE",
]


def extract_resume_entities(text: str) -> Dict[str, List[str]]:
    model = get_gliner_model()
    entities = model.predict_entities(text, labels=LABELS, threshold=0.35)

    result: Dict[str, List[str]] = {}
    for ent in entities:
        label = ent["label"]
        value = ent["text"]

        result.setdefault(label, set()).add(value)

    # convert sets → lists
    return {k: sorted(list(v)) for k, v in result.items()}

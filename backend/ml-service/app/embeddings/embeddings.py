from transformers import AutoTokenizer, AutoModel
import torch

print("Loading embedding model...")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

print("Embedding model ready")


# 🔥 Mean Pooling (IMPORTANT — replaces SentenceTransformer magic)
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # last hidden states
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


def embed_texts(texts):
    # 🔥 Flatten input properly
    if isinstance(texts[0], list):
        texts = [" ".join(t) for t in texts]

    encoded_input = tokenizer(
        texts,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        model_output = model(**encoded_input)

    embeddings = mean_pooling(model_output, encoded_input["attention_mask"])

    return embeddings.tolist()


def embed_single(text):
    return embed_texts([text])[0]
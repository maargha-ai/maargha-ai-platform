from datetime import timedelta
from typing import Optional

from google.cloud import storage

_client: Optional[storage.Client] = None


def get_storage_client() -> storage.Client:
    """Get or create storage client lazily"""
    global _client
    if _client is None:
        _client = storage.Client()
    return _client


def generate_signed_url(bucket_name: str, object_path: str) -> str:
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_path)

    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=30),
        method="GET",
    )

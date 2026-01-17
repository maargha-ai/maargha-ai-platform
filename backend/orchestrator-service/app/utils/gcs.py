from google.cloud import storage
from datetime import timedelta
import os

client = storage.Client()

def generate_signed_url(bucket_name: str, object_path: str) -> str:
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_path)

    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=30),
        method="GET",
    )

def upload_to_gcs(
    local_path: str,
    bucket_name: str,
    destination_blob: str,
) -> str:
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    blob.upload_from_filename(local_path)

    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=30),
        method="GET",
    )
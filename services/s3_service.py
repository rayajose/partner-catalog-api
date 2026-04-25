import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
S3_RAW_BUCKET = os.getenv("S3_RAW_BUCKET")


def upload_raw_feed(file_bytes: bytes, object_key: str, content_type: str = "text/csv") -> str:
    """
    Uploads a raw partner feed file to S3.

    Args:
        file_bytes: Raw file contents.
        object_key: Destination path/key in S3.
        content_type: MIME type of the uploaded file.

    Returns:
        The S3 object key.
    """
    if not S3_RAW_BUCKET:
        raise RuntimeError("S3_RAW_BUCKET environment variable is not set.")

    s3_client = boto3.client("s3", region_name=AWS_REGION)

    try:
        s3_client.put_object(
            Bucket=S3_RAW_BUCKET,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type,
        )
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to upload raw feed to S3: {exc}") from exc

    return object_key
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import boto3
from .util import settings, logger

@dataclass
class S3ObjectInfo:
    bucket: str
    key: str
    url: Optional[str] = None


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=settings.get("AWS_SECRET_ACCESS_KEY"),
        region_name=settings.get("AWS_REGION", "us-east-1"),
    )


def generate_presigned_put(key: str, expires: int = 900) -> S3ObjectInfo:
    bucket = settings.get("AWS_BUCKET")
    client = get_s3_client()
    url = client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires,
    )
    logger.debug(f"Presigned PUT gerado para {key}")
    return S3ObjectInfo(bucket=bucket, key=key, url=url)


def generate_presigned_get(key: str, expires: int = 900) -> S3ObjectInfo:
    bucket = settings.get("AWS_BUCKET")
    client = get_s3_client()
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires,
    )
    logger.debug(f"Presigned GET gerado para {key}")
    return S3ObjectInfo(bucket=bucket, key=key, url=url)


def put_bytes(key: str, data: bytes, content_type: str = "application/octet-stream"):
    client = get_s3_client()
    bucket = settings.get("AWS_BUCKET")
    client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    logger.info(f"Upload concluído: s3://{bucket}/{key}")


def get_bytes(key: str) -> bytes:
    client = get_s3_client()
    bucket = settings.get("AWS_BUCKET")
    obj = client.get_object(Bucket=bucket, Key=key)
    return obj["Body"].read()


# Helper key builders using default prefix
def _s3_base_prefix() -> str:
    # default path inside bucket where all app files live
    return settings.get("AWS_S3_BASE_PATH", "yavix-dev/data_integration")


def upload_key_for(arquivo_id: str, filename: str) -> str:
    base = _s3_base_prefix().strip("/")
    return f"{base}/uploads/{arquivo_id}/{filename}"


def normalized_key_for(arquivo_id: str, filename: str | None = None) -> str:
    base = _s3_base_prefix().strip("/")
    name = (filename or arquivo_id) + ".xlsx"
    return f"{base}/normalized/{arquivo_id}/{name}"


def report_key_for(arquivo_id: str, filename: str | None = None) -> str:
    base = _s3_base_prefix().strip("/")
    name = (filename or f"erros_{arquivo_id}")
    return f"{base}/reports/{arquivo_id}/{name}"

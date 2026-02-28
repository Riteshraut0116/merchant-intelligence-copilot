import os

def env(key, default=None):
    return os.getenv(key, default)

AWS_REGION = env("AWS_REGION","ap-south-1")
BEDROCK_MODEL_PRIMARY = env("BEDROCK_MODEL_PRIMARY","amazon.nova-pro-v1:0")
BEDROCK_MODEL_FAST = env("BEDROCK_MODEL_FAST","amazon.nova-lite-v1:0")
BEDROCK_MODEL_BASELINE = env("BEDROCK_MODEL_BASELINE","amazon.nova-micro-v1:0")

TEMPERATURE = float(env("TEMPERATURE","0.2"))
MAX_TOKENS = int(env("MAX_TOKENS","1200"))
TOP_P = float(env("TOP_P","0.9"))

S3_BUCKET_NAME = env("S3_BUCKET_NAME")
DYNAMODB_TABLE_NAME = env("DYNAMODB_TABLE_NAME")

APP_ENV = env("APP_ENV","development")
LOG_LEVEL = env("LOG_LEVEL","INFO")

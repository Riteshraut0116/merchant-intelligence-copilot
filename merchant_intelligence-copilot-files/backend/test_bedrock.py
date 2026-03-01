#!/usr/bin/env python3
"""
Test script to verify Bedrock API connectivity and Nova model access
"""

import os
import sys
import json
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('src/.env')

# Configuration
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
MODEL_ID = os.getenv("BEDROCK_MODEL_FAST", "amazon.nova-lite-v1:0")

print("=" * 60)
print("Bedrock API Connection Test")
print("=" * 60)
print(f"Region: {AWS_REGION}")
print(f"Model: {MODEL_ID}")
print(f"Access Key: {AWS_ACCESS_KEY_ID[:10]}..." if AWS_ACCESS_KEY_ID else "Access Key: NOT SET")
print("=" * 60)

# Initialize Bedrock client
try:
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    print("✓ Bedrock client initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize Bedrock client: {e}")
    sys.exit(1)

# Test 1: Simple invoke_model call
print("\n" + "=" * 60)
print("Test 1: Simple invoke_model API call")
print("=" * 60)

request_body = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "Say 'Hello, I am working!' in one sentence."
                }
            ]
        }
    ],
    "inferenceConfig": {
        "temperature": 0.2,
        "topP": 0.9,
        "maxTokens": 100
    }
}

try:
    print(f"Sending request to {MODEL_ID}...")
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(request_body),
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response['body'].read())
    print("✓ API call successful!")
    print(f"\nResponse structure: {json.dumps(response_body, indent=2)[:500]}...")
    
    # Extract text
    output = response_body.get("output", {})
    message = output.get("message", {})
    content = message.get("content", [])
    text_parts = [part.get("text", "") for part in content if "text" in part]
    result = " ".join(text_parts).strip()
    
    print(f"\n✓ Extracted text: {result}")
    
except Exception as e:
    print(f"✗ API call failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Business advisor query
print("\n" + "=" * 60)
print("Test 2: Business advisor query with system prompt")
print("=" * 60)

request_body = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "What are 3 tips for managing inventory in a small grocery store?"
                }
            ]
        }
    ],
    "system": [
        {
            "text": "You are a helpful business advisor for small merchants in India. Provide practical, actionable advice."
        }
    ],
    "inferenceConfig": {
        "temperature": 0.2,
        "topP": 0.9,
        "maxTokens": 300
    }
}

try:
    print(f"Sending business query to {MODEL_ID}...")
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(request_body),
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response['body'].read())
    
    # Extract text
    output = response_body.get("output", {})
    message = output.get("message", {})
    content = message.get("content", [])
    text_parts = [part.get("text", "") for part in content if "text" in part]
    result = " ".join(text_parts).strip()
    
    print(f"\n✓ Business advice response:\n{result}")
    
except Exception as e:
    print(f"✗ Business query failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed! Bedrock API is working correctly.")
print("=" * 60)

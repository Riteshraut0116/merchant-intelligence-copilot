#!/usr/bin/env python3
"""
Diagnostic script to check Bedrock access and model availability
"""

import os
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv('src/.env')

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

print("=" * 70)
print("AWS BEDROCK ACCESS DIAGNOSTIC")
print("=" * 70)
print(f"\n📍 Region: {AWS_REGION}")
print(f"🔑 Access Key: {AWS_ACCESS_KEY_ID[:10]}...{AWS_ACCESS_KEY_ID[-4:]}" if AWS_ACCESS_KEY_ID else "❌ Access Key: NOT SET")
print(f"🔐 Secret Key: {'*' * 20}...{AWS_SECRET_ACCESS_KEY[-4:]}" if AWS_SECRET_ACCESS_KEY else "❌ Secret Key: NOT SET")

# Initialize clients
try:
    bedrock = boto3.client(
        "bedrock",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    print("\n✅ Bedrock clients initialized successfully")
except Exception as e:
    print(f"\n❌ Failed to initialize Bedrock clients: {e}")
    exit(1)

# Check available foundation models
print("\n" + "=" * 70)
print("CHECKING AVAILABLE MODELS IN YOUR REGION")
print("=" * 70)

try:
    response = bedrock.list_foundation_models()
    models = response.get('modelSummaries', [])
    
    nova_models = [m for m in models if 'nova' in m.get('modelId', '').lower()]
    
    if nova_models:
        print(f"\n✅ Found {len(nova_models)} Nova models available:")
        for model in nova_models:
            model_id = model.get('modelId', 'Unknown')
            status = model.get('modelLifecycle', {}).get('status', 'Unknown')
            print(f"   • {model_id} - Status: {status}")
    else:
        print(f"\n⚠️  No Nova models found in region {AWS_REGION}")
        print("\n💡 Nova models may not be available in this region.")
        print("   Try these regions instead:")
        print("   • us-east-1 (US East - N. Virginia)")
        print("   • us-west-2 (US West - Oregon)")
        print("   • eu-west-1 (Europe - Ireland)")
        
except Exception as e:
    print(f"\n❌ Failed to list models: {e}")
    print("\n💡 This might mean:")
    print("   1. Your IAM user doesn't have bedrock:ListFoundationModels permission")
    print("   2. Bedrock is not available in your region")

# Test model access
print("\n" + "=" * 70)
print("TESTING MODEL ACCESS")
print("=" * 70)

test_models = [
    "amazon.nova-micro-v1:0",
    "amazon.nova-lite-v1:0",
    "amazon.nova-pro-v1:0"
]

for model_id in test_models:
    print(f"\n🧪 Testing {model_id}...")
    try:
        import json
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": "Say 'test' in one word."}]
                }
            ],
            "inferenceConfig": {
                "temperature": 0.2,
                "topP": 0.9,
                "maxTokens": 10
            }
        }
        
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )
        
        response_body = json.loads(response['body'].read())
        print(f"   ✅ {model_id} - WORKING!")
        
    except Exception as e:
        error_msg = str(e)
        if "AccessDeniedException" in error_msg:
            print(f"   ❌ {model_id} - ACCESS DENIED")
            print(f"      💡 You need to enable model access in Bedrock console")
        elif "ValidationException" in error_msg or "model" in error_msg.lower():
            print(f"   ❌ {model_id} - NOT AVAILABLE in {AWS_REGION}")
        else:
            print(f"   ❌ {model_id} - ERROR: {error_msg[:100]}")

print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)

print("""
📋 To fix Bedrock access issues:

1. Enable Model Access:
   • Go to AWS Console → Bedrock
   • Click "Model access" in left sidebar
   • Click "Manage model access"
   • Enable: Amazon Nova Micro, Lite, and Pro
   • Click "Save changes"
   • Wait 1-2 minutes for access to be granted

2. Check IAM Permissions:
   Your IAM user/role needs these permissions:
   • bedrock:InvokeModel
   • bedrock:InvokeModelWithResponseStream
   • bedrock:ListFoundationModels (optional, for diagnostics)

3. Try Different Region:
   If Nova models aren't available in ap-south-1, update .env:
   AWS_REGION=us-east-1

4. Verify Credentials:
   Make sure your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are correct
""")

print("=" * 70)

import json, boto3, os
from .config import AWS_REGION, TEMPERATURE, TOP_P, MAX_TOKENS

# Initialize Bedrock client with credentials from environment
br = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def nova_converse(model_id: str, system: str, user: str):
    """
    Call AWS Bedrock Converse API for Nova models.
    Returns the text response from the model.
    """
    import logging
    logger = logging.getLogger()
    
    try:
        logger.info(f"Calling Bedrock with model: {model_id}")
        logger.info(f"System prompt length: {len(system)}, User prompt length: {len(user)}")
        
        response = br.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": user}]
                }
            ],
            system=[{"text": system}],
            inferenceConfig={
                "temperature": TEMPERATURE,
                "topP": TOP_P,
                "maxTokens": MAX_TOKENS
            }
        )
        
        logger.info(f"Bedrock response received: {response.get('ResponseMetadata', {}).get('HTTPStatusCode')}")
        
        # Extract text from response
        output = response.get("output", {})
        message = output.get("message", {})
        content = message.get("content", [])
        
        # Combine all text parts
        text_parts = [part.get("text", "") for part in content if "text" in part]
        result = " ".join(text_parts).strip()
        
        logger.info(f"Extracted text length: {len(result)}")
        return result
        
    except Exception as e:
        logger.error(f"Bedrock API call failed: {str(e)}", exc_info=True)
        raise Exception(f"Bedrock API call failed: {str(e)}")

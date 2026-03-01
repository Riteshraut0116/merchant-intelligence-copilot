import json, boto3, logging
from .config import AWS_REGION, TEMPERATURE, TOP_P, MAX_TOKENS

logger = logging.getLogger()

try:
    br = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    logger.info(f"Bedrock client initialized for region: {AWS_REGION}")
except Exception as e:
    logger.error(f"Failed to initialize Bedrock client: {str(e)}")
    br = None

def nova_converse(model_id: str, system: str, user: str):
    """
    Call AWS Bedrock Nova models using invoke_model API.
    Returns the generated text or raises an exception.
    """
    if br is None:
        raise Exception("Bedrock client not initialized. Check AWS credentials.")
    
    try:
        logger.info(f"Calling Bedrock model: {model_id}")
        
        # Prepare request body for Nova models
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": f"{system}\n\n{user}"}]
                }
            ],
            "inferenceConfig": {
                "temperature": TEMPERATURE,
                "topP": TOP_P,
                "maxTokens": MAX_TOKENS
            }
        }
        
        # Call Bedrock using invoke_model
        response = br.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        
        # Extract text from response
        output = response_body.get("output", {})
        message = output.get("message", {})
        content = message.get("content", [])
        
        # Combine all text parts
        text_parts = [part.get("text", "") for part in content if "text" in part]
        result = " ".join(text_parts).strip()
        
        if not result:
            logger.warning(f"Empty response from Bedrock. Full response: {response_body}")
            raise Exception("Empty response from Bedrock")
        
        logger.info(f"Bedrock response received: {len(result)} characters")
        return result
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Bedrock API error: {error_msg}")
        
        # Provide helpful error messages
        if "AccessDeniedException" in error_msg:
            raise Exception("AWS Bedrock access denied. Please enable Bedrock in your AWS account and request access to Nova models.")
        elif "ValidationException" in error_msg:
            raise Exception(f"Invalid Bedrock request: {error_msg}")
        elif "ResourceNotFoundException" in error_msg:
            raise Exception(f"Model not found: {model_id}. Ensure Nova models are available in {AWS_REGION}")
        elif "ThrottlingException" in error_msg:
            raise Exception("Bedrock API rate limit exceeded. Please try again later.")
        else:
            raise Exception(f"Bedrock error: {error_msg}")

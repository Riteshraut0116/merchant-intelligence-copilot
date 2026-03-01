"""
Test LLM Handler - Simple endpoint to test Bedrock connectivity
"""

import json
import logging
from common.responses import ok, bad
from common.config import BEDROCK_MODEL_FAST
from common.bedrock_nova import nova_converse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    Test endpoint to verify Bedrock LLM is working.
    GET /test-llm
    """
    try:
        logger.info("Testing Bedrock LLM connection...")
        
        # Simple test query
        system = "You are a helpful assistant. Respond in one short sentence."
        user = "Say 'Hello, I am working correctly!'"
        
        logger.info(f"Calling Bedrock with model: {BEDROCK_MODEL_FAST}")
        response = nova_converse(BEDROCK_MODEL_FAST, system, user)
        
        logger.info(f"LLM Response: {response}")
        
        return ok({
            "status": "success",
            "message": "Bedrock LLM is working!",
            "model": BEDROCK_MODEL_FAST,
            "test_response": response
        })
        
    except Exception as e:
        logger.error(f"LLM test failed: {str(e)}", exc_info=True)
        return bad(f"LLM test failed: {str(e)}")

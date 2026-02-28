"""
Chat Handler - Mock Implementation for Demo
This is a simple mock implementation that provides demo responses.
Replace with actual Bedrock integration for production.
"""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle chat requests with mock responses for demo purposes.
    
    Expected request body:
    {
        "message": "Which products should I order?",
        "language": "en"  # Optional: "en", "hi", "mr"
    }
    """
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', '').lower()
        language = body.get('language', 'en')
        
        logger.info(f"Chat request - Message: {message}, Language: {language}")
        
        # Mock responses based on common questions
        response_text = get_mock_response(message, language)
        
        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Merchant-Id',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({
                'response': response_text,
                'confidence': 75,  # Mock confidence score
                'language': language,
                'disclaimer': 'This is a demo response. AI suggestions are probabilistic.'
            })
        }
        
    except Exception as e:
        logger.error(f"Error in chat handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': f'Error processing chat request: {str(e)}'
            })
        }


def get_mock_response(message: str, language: str) -> str:
    """
    Generate mock responses based on the message content.
    """
    
    # English responses
    if language == 'en':
        if 'order' in message or 'reorder' in message or 'stock' in message:
            return """Based on your recent sales data, I recommend ordering:

📦 High Priority:
• Atta 1kg - Order 50 units (High urgency)
• Rice 5kg - Order 30 units (Medium urgency)
• Cooking Oil 1L - Order 40 units (High urgency)

These products show strong demand trends and low current stock levels. Order within the next 2-3 days to avoid stockouts."""

        elif 'top' in message or 'best' in message or 'selling' in message:
            return """Your top selling products this month are:

🔝 Top 5 Products:
1. Atta 1kg - 450 units sold
2. Rice 5kg - 380 units sold
3. Cooking Oil 1L - 320 units sold
4. Sugar 1kg - 290 units sold
5. Tea Powder 250g - 275 units sold

These products account for 65% of your total revenue. Consider maintaining higher stock levels for these items."""

        elif 'spike' in message or 'alert' in message or 'anomaly' in message:
            return """⚠️ Demand Alerts:

📈 Spikes Detected:
• Cold Drinks - 45% increase (likely due to weather)
• Ice Cream - 38% increase (seasonal trend)

📉 Drops Detected:
• Hot Beverages - 22% decrease (seasonal)

💡 Recommendation: Adjust inventory levels accordingly and consider promotional pricing for slow-moving items."""

        elif 'forecast' in message or 'predict' in message or 'future' in message:
            return """📊 7-Day Forecast Summary:

Based on historical patterns and current trends:

• Overall sales expected to increase by 12%
• Weekend sales typically 30% higher
• Festival season approaching - expect 25% surge
• Weather forecast shows hot days - cold beverages will spike

Confidence: 82% (based on 90 days of historical data)"""

        else:
            return """I can help you with:

💬 Product recommendations and reorder suggestions
📊 Sales trends and forecasts
⚠️ Demand alerts and anomalies
📈 Top performing products
💡 Business insights and optimization tips

What would you like to know about your business?"""
    
    # Hindi responses
    elif language == 'hi':
        if 'order' in message or 'reorder' in message:
            return """आपके हाल के बिक्री डेटा के आधार पर, मैं ऑर्डर करने की सलाह देता हूं:

📦 उच्च प्राथमिकता:
• आटा 1kg - 50 यूनिट ऑर्डर करें (उच्च तात्कालिकता)
• चावल 5kg - 30 यूनिट ऑर्डर करें (मध्यम तात्कालिकता)
• खाना पकाने का तेल 1L - 40 यूनिट ऑर्डर करें (उच्च तात्कालिकता)

ये उत्पाद मजबूत मांग रुझान और कम वर्तमान स्टॉक स्तर दिखाते हैं।"""

        else:
            return """मैं आपकी मदद कर सकता हूं:

💬 उत्पाद सिफारिशें और पुनः ऑर्डर सुझाव
📊 बिक्री रुझान और पूर्वानुमान
⚠️ मांग अलर्ट और विसंगतियां
📈 शीर्ष प्रदर्शन करने वाले उत्पाद

आप अपने व्यवसाय के बारे में क्या जानना चाहेंगे?"""
    
    # Marathi responses
    elif language == 'mr':
        if 'order' in message or 'reorder' in message:
            return """तुमच्या अलीकडील विक्री डेटावर आधारित, मी ऑर्डर करण्याची शिफारस करतो:

📦 उच्च प्राधान्य:
• पीठ 1kg - 50 युनिट ऑर्डर करा (उच्च तातडीचे)
• तांदूळ 5kg - 30 युनिट ऑर्डर करा (मध्यम तातडीचे)
• स्वयंपाक तेल 1L - 40 युनिट ऑर्डर करा (उच्च तातडीचे)

ही उत्पादने मजबूत मागणी ट्रेंड आणि कमी वर्तमान स्टॉक पातळी दर्शवतात।"""

        else:
            return """मी तुम्हाला मदत करू शकतो:

💬 उत्पादन शिफारसी आणि पुन्हा ऑर्डर सूचना
📊 विक्री ट्रेंड आणि अंदाज
⚠️ मागणी अलर्ट आणि विसंगती
📈 शीर्ष कामगिरी करणारी उत्पादने

तुम्हाला तुमच्या व्यवसायाबद्दल काय जाणून घ्यायचे आहे?"""
    
    # Default fallback
    return """I'm here to help with your business insights! 

You can ask me about:
• Product recommendations
• Sales forecasts
• Inventory alerts
• Top selling items

What would you like to know?"""

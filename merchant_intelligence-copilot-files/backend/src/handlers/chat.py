"""
Chat Handler - LLM-powered conversational interface
Uses Bedrock Nova for intelligent responses based on insights data
"""

import json
import logging
from typing import Dict, Any
from common.responses import ok, bad
from common.config import BEDROCK_MODEL_FAST
from common.bedrock_nova import nova_converse
from common.validators import validate_prompt_injection

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle chat requests with LLM-powered responses.
    
    Expected request body:
    {
        "message": "Which products should I order?",
        "language": "en",  # Optional: "en", "hi", "mr"
        "insights": {...}  # Optional: current insights data for context
    }
    """
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', '').strip()
        language = body.get('language', 'en')
        insights = body.get('insights')
        
        if not message:
            return bad("Message is required")
        
        # Validate for prompt injection
        if not validate_prompt_injection(message):
            return bad("Invalid message content")
        
        logger.info(f"Chat request - Message: {message[:100]}, Language: {language}")
        
        # Log insights data structure for debugging
        if insights:
            if 'insights' in insights and isinstance(insights['insights'], dict):
                products_count = len(insights['insights'].get('products', []))
                logger.info(f"Insights structure: nested, products count: {products_count}")
            elif 'products' in insights:
                products_count = len(insights.get('products', []))
                logger.info(f"Insights structure: flat, products count: {products_count}")
            else:
                logger.warning(f"Insights structure unknown: {list(insights.keys())}")
        else:
            logger.info("No insights data provided")
        
        # Generate LLM response with context
        response_text = generate_llm_response(message, language, insights)
        
        return ok({
            'response': response_text,
            'language': language,
            'disclaimer': 'AI-assisted insights. Review with your business knowledge.'
        })
        
    except Exception as e:
        logger.error(f"Error in chat handler: {str(e)}", exc_info=True)
        return bad(f"Error processing chat request: {str(e)}")


def generate_llm_response(message: str, language: str, insights: Dict = None) -> str:
    """
    Generate LLM-powered responses with business context.
    """
    import time
    start_time = time.time()
    
    message_lower = message.lower()
    logger.info(f"Processing message: '{message_lower}'")
    
    # Check if insights data is available and extract products
    products = []
    if insights:
        # Handle nested structure: insights.insights.products or insights.products
        if 'insights' in insights and isinstance(insights['insights'], dict):
            products = insights['insights'].get('products', [])
        elif 'products' in insights:
            products = insights.get('products', [])
    
    if not products:
        logger.info(f"No products found, using LLM for general business advice (took {time.time() - start_time:.3f}s)")
        return get_no_data_response(language, message)
    
    logger.info(f"Found {len(products)} products")
    
    high_urgency = [p for p in products if p.get('reorder', {}).get('urgency') == 'high']
    medium_urgency = [p for p in products if p.get('reorder', {}).get('urgency') == 'medium']
    anomalies = [p for p in products if p.get('anomalies') and len(p['anomalies']) > 0]
    low_confidence = [p for p in products if p.get('confidence_score', 100) < 60]
    
    # Use LLM for all queries with business context
    logger.info(f"Using LLM for response (took {time.time() - start_time:.3f}s so far)")
    return generate_llm_complex_response(message, language, products, high_urgency, anomalies)


def generate_reorder_response(high_urgency: list, medium_urgency: list, language: str) -> str:
    """Fast response for reorder questions"""
    if language == 'en':
        if not high_urgency and not medium_urgency:
            return "✅ Good news! All products have sufficient stock levels. No urgent reorders needed right now."
        
        response = "📦 Reorder Recommendations:\n\n"
        if high_urgency:
            response += "🔴 HIGH PRIORITY (Order immediately):\n"
            for p in high_urgency[:5]:
                response += f"• {p['product_name']} - Order {p['reorder']['quantity']} units\n"
        if medium_urgency:
            response += f"\n🟡 MEDIUM PRIORITY (Order within 3-5 days):\n"
            for p in medium_urgency[:3]:
                response += f"• {p['product_name']} - Order {p['reorder']['quantity']} units\n"
        return response
    
    elif language == 'hi':
        if not high_urgency and not medium_urgency:
            return "✅ अच्छी खबर! सभी उत्पादों में पर्याप्त स्टॉक है। अभी कोई तत्काल पुनः ऑर्डर की आवश्यकता नहीं।"
        
        response = "📦 पुनः ऑर्डर सिफारिशें:\n\n"
        if high_urgency:
            response += "🔴 उच्च प्राथमिकता (तुरंत ऑर्डर करें):\n"
            for p in high_urgency[:5]:
                response += f"• {p['product_name']} - {p['reorder']['quantity']} यूनिट ऑर्डर करें\n"
        if medium_urgency:
            response += f"\n🟡 मध्यम प्राथमिकता (3-5 दिनों में ऑर्डर करें):\n"
            for p in medium_urgency[:3]:
                response += f"• {p['product_name']} - {p['reorder']['quantity']} यूनिट ऑर्डर करें\n"
        return response
    
    else:  # Marathi
        if not high_urgency and not medium_urgency:
            return "✅ चांगली बातमी! सर्व उत्पादनांमध्ये पुरेसा स्टॉक आहे। आत्ता कोणत्याही तातडीच्या पुन्हा ऑर्डरची गरज नाही."
        
        response = "📦 पुन्हा ऑर्डर शिफारसी:\n\n"
        if high_urgency:
            response += "🔴 उच्च प्राधान्य (लगेच ऑर्डर करा):\n"
            for p in high_urgency[:5]:
                response += f"• {p['product_name']} - {p['reorder']['quantity']} युनिट ऑर्डर करा\n"
        if medium_urgency:
            response += f"\n🟡 मध्यम प्राधान्य (3-5 दिवसांत ऑर्डर करा):\n"
            for p in medium_urgency[:3]:
                response += f"• {p['product_name']} - {p['reorder']['quantity']} युनिट ऑर्डर करा\n"
        return response


def generate_top_products_response(products: list, language: str) -> str:
    """Fast response for top products questions"""
    sorted_products = sorted(products, key=lambda p: sum([f.get('yhat', 0) for f in p.get('forecast', [])]), reverse=True)[:5]
    
    if language == 'en':
        response = "🔝 Top Selling Products:\n\n"
        for i, p in enumerate(sorted_products, 1):
            forecast_sum = sum([f.get('yhat', 0) for f in p.get('forecast', [])])
            response += f"{i}. {p['product_name']} - {forecast_sum:.0f} units (7-day forecast)\n"
        response += "\n💡 Tip: Keep higher stock levels for these products to avoid stockouts."
        return response
    
    elif language == 'hi':
        response = "🔝 सबसे ज़्यादा बिकने वाले उत्पाद:\n\n"
        for i, p in enumerate(sorted_products, 1):
            forecast_sum = sum([f.get('yhat', 0) for f in p.get('forecast', [])])
            response += f"{i}. {p['product_name']} - {forecast_sum:.0f} यूनिट (7-दिन का पूर्वानुमान)\n"
        response += "\n💡 सुझाव: स्टॉकआउट से बचने के लिए इन उत्पादों का अधिक स्टॉक रखें।"
        return response
    
    else:  # Marathi
        response = "🔝 सर्वाधिक विक्री होणारी उत्पादने:\n\n"
        for i, p in enumerate(sorted_products, 1):
            forecast_sum = sum([f.get('yhat', 0) for f in p.get('forecast', [])])
            response += f"{i}. {p['product_name']} - {forecast_sum:.0f} युनिट (7-दिवसांचा अंदाज)\n"
        response += "\n💡 टीप: स्टॉकआउट टाळण्यासाठी या उत्पादनांचा जास्त स्टॉक ठेवा."
        return response


def generate_alerts_response(anomalies: list, language: str) -> str:
    """Fast response for alerts/anomalies questions"""
    if language == 'en':
        if not anomalies:
            return "✅ No unusual patterns detected. All products showing normal demand trends."
        
        response = "⚠️ Demand Alerts:\n\n"
        for p in anomalies[:5]:
            response += f"• {p['product_name']}:\n"
            for anomaly in p['anomalies'][:2]:
                response += f"  - {anomaly}\n"
        response += "\n💡 Review these products and adjust inventory/pricing accordingly."
        return response
    
    elif language == 'hi':
        if not anomalies:
            return "✅ कोई असामान्य पैटर्न नहीं मिला। सभी उत्पाद सामान्य मांग रुझान दिखा रहे हैं।"
        
        response = "⚠️ मांग अलर्ट:\n\n"
        for p in anomalies[:5]:
            response += f"• {p['product_name']}:\n"
            for anomaly in p['anomalies'][:2]:
                response += f"  - {anomaly}\n"
        response += "\n💡 इन उत्पादों की समीक्षा करें और तदनुसार इन्वेंटरी/मूल्य निर्धारण समायोजित करें।"
        return response
    
    else:  # Marathi
        if not anomalies:
            return "✅ कोणतेही असामान्य पॅटर्न आढळले नाहीत. सर्व उत्पादने सामान्य मागणी ट्रेंड दर्शवत आहेत."
        
        response = "⚠️ मागणी अलर्ट:\n\n"
        for p in anomalies[:5]:
            response += f"• {p['product_name']}:\n"
            for anomaly in p['anomalies'][:2]:
                response += f"  - {anomaly}\n"
        response += "\n💡 या उत्पादनांचे पुनरावलोकन करा आणि त्यानुसार इन्व्हेंटरी/किंमत समायोजित करा."
        return response


def generate_forecast_response(products: list, language: str) -> str:
    """Fast response for forecast questions"""
    total_forecast = sum([sum([f.get('yhat', 0) for f in p.get('forecast', [])]) for p in products])
    avg_confidence = sum([p.get('confidence_score', 0) for p in products]) / len(products) if products else 0
    
    if language == 'en':
        response = f"📊 7-Day Forecast Summary:\n\n"
        response += f"• Total expected sales: {total_forecast:.0f} units\n"
        response += f"• Average confidence: {avg_confidence:.0f}%\n"
        response += f"• Products analyzed: {len(products)}\n\n"
        response += "Top 3 products by forecast:\n"
        sorted_products = sorted(products, key=lambda p: sum([f.get('yhat', 0) for f in p.get('forecast', [])]), reverse=True)[:3]
        for i, p in enumerate(sorted_products, 1):
            forecast_sum = sum([f.get('yhat', 0) for f in p.get('forecast', [])])
            response += f"{i}. {p['product_name']} - {forecast_sum:.0f} units\n"
        return response
    
    elif language == 'hi':
        response = f"📊 7-दिन का पूर्वानुमान सारांश:\n\n"
        response += f"• कुल अपेक्षित बिक्री: {total_forecast:.0f} यूनिट\n"
        response += f"• औसत विश्वास: {avg_confidence:.0f}%\n"
        response += f"• विश्लेषित उत्पाद: {len(products)}\n\n"
        response += "पूर्वानुमान के अनुसार शीर्ष 3 उत्पाद:\n"
        sorted_products = sorted(products, key=lambda p: sum([f.get('yhat', 0) for f in p.get('forecast', [])]), reverse=True)[:3]
        for i, p in enumerate(sorted_products, 1):
            forecast_sum = sum([f.get('yhat', 0) for f in p.get('forecast', [])])
            response += f"{i}. {p['product_name']} - {forecast_sum:.0f} यूनिट\n"
        return response
    
    else:  # Marathi
        response = f"📊 7-दिवसांचा अंदाज सारांश:\n\n"
        response += f"• एकूण अपेक्षित विक्री: {total_forecast:.0f} युनिट\n"
        response += f"• सरासरी आत्मविश्वास: {avg_confidence:.0f}%\n"
        response += f"• विश्लेषित उत्पादने: {len(products)}\n\n"
        response += "अंदाजानुसार शीर्ष 3 उत्पादने:\n"
        sorted_products = sorted(products, key=lambda p: sum([f.get('yhat', 0) for f in p.get('forecast', [])]), reverse=True)[:3]
        for i, p in enumerate(sorted_products, 1):
            forecast_sum = sum([f.get('yhat', 0) for f in p.get('forecast', [])])
            response += f"{i}. {p['product_name']} - {forecast_sum:.0f} युनिट\n"
        return response


def generate_confidence_response(low_confidence: list, all_products: list, language: str) -> str:
    """Fast response for confidence/accuracy questions"""
    avg_confidence = sum([p.get('confidence_score', 0) for p in all_products]) / len(all_products) if all_products else 0
    
    if language == 'en':
        response = f"📈 Forecast Confidence Report:\n\n"
        response += f"• Average confidence: {avg_confidence:.0f}%\n"
        response += f"• Products analyzed: {len(all_products)}\n"
        response += f"• Low confidence items: {len(low_confidence)}\n\n"
        
        if low_confidence:
            response += "⚠️ Products with low confidence (<60%):\n"
            for p in low_confidence[:3]:
                response += f"• {p['product_name']} - {p['confidence_score']:.0f}%\n"
            response += "\n💡 Low confidence may indicate insufficient data or irregular patterns."
        else:
            response += "✅ All forecasts have good confidence levels!"
        return response
    
    elif language == 'hi':
        response = f"📈 पूर्वानुमान विश्वास रिपोर्ट:\n\n"
        response += f"• औसत विश्वास: {avg_confidence:.0f}%\n"
        response += f"• विश्लेषित उत्पाद: {len(all_products)}\n"
        response += f"• कम विश्वास वाले आइटम: {len(low_confidence)}\n\n"
        
        if low_confidence:
            response += "⚠️ कम विश्वास वाले उत्पाद (<60%):\n"
            for p in low_confidence[:3]:
                response += f"• {p['product_name']} - {p['confidence_score']:.0f}%\n"
            response += "\n💡 कम विश्वास अपर्याप्त डेटा या अनियमित पैटर्न का संकेत हो सकता है।"
        else:
            response += "✅ सभी पूर्वानुमानों में अच्छा विश्वास स्तर है!"
        return response
    
    else:  # Marathi
        response = f"📈 अंदाज आत्मविश्वास अहवाल:\n\n"
        response += f"• सरासरी आत्मविश्वास: {avg_confidence:.0f}%\n"
        response += f"• विश्लेषित उत्पादने: {len(all_products)}\n"
        response += f"• कमी आत्मविश्वास असलेले आयटम: {len(low_confidence)}\n\n"
        
        if low_confidence:
            response += "⚠️ कमी आत्मविश्वास असलेली उत्पादने (<60%):\n"
            for p in low_confidence[:3]:
                response += f"• {p['product_name']} - {p['confidence_score']:.0f}%\n"
            response += "\n💡 कमी आत्मविश्वास अपुरा डेटा किंवा अनियमित पॅटर्नचे संकेत असू शकते."
        else:
            response += "✅ सर्व अंदाजांमध्ये चांगला आत्मविश्वास पातळी आहे!"
        return response


def generate_llm_complex_response(message: str, language: str, products: list, high_urgency: list, anomalies: list) -> str:
    """Use LLM with rich business context for intelligent responses"""
    
    logger.info("Generating LLM response with business context")
    
    lang_instruction = {
        'en': 'Respond in English',
        'hi': 'Respond in Hindi (हिंदी)',
        'mr': 'Respond in Marathi (मराठी)'
    }.get(language, 'Respond in English')
    
    # Build rich context with product details
    top_products = sorted(products, key=lambda p: sum([f.get('yhat', 0) for f in p.get('forecast', [])]), reverse=True)[:5]
    
    context_parts = [
        f"Total products analyzed: {len(products)}",
        f"High urgency reorders: {len(high_urgency)}",
        f"Products with anomalies: {len(anomalies)}"
    ]
    
    if high_urgency:
        context_parts.append(f"\nHigh priority reorders: {', '.join([p['product_name'] + f' ({p['reorder']['quantity']} units)' for p in high_urgency[:3]])}")
    
    if anomalies:
        context_parts.append(f"\nProducts with alerts: {', '.join([p['product_name'] for p in anomalies[:3]])}")
    
    context_parts.append(f"\nTop selling products (7-day forecast): {', '.join([p['product_name'] + f' ({sum([f.get('yhat', 0) for f in p.get('forecast', [])]):.0f} units)' for p in top_products[:3]])}")
    
    context = "\n".join(context_parts)
    
    system = f"""You are an AI business advisor for Indian MSME merchants, specializing in inventory management and demand forecasting.

{lang_instruction}. Be conversational, helpful, and provide actionable insights.

Guidelines:
- Give specific, actionable recommendations
- Use emojis appropriately (📦 for orders, 🔝 for top products, ⚠️ for alerts, 📊 for forecasts)
- Keep responses concise but informative (3-5 sentences)
- Focus on business impact and next steps
- Use simple language suitable for small business owners"""
    
    user = f"""Business Context:
{context}

Merchant Question: {message}

Provide a helpful, actionable response based on the data."""
    
    try:
        response = nova_converse(BEDROCK_MODEL_FAST, system, user)
        return response
    except Exception as e:
        logger.error(f"LLM generation failed: {str(e)}")
        # Fallback to helpful menu
        if language == 'en':
            return f"""I can help you with:

📦 Reorder recommendations - Ask "Which products should I order?"
🔝 Top products - Ask "What are my top selling products?"
⚠️ Alerts - Ask "Are there any demand spikes?"
📊 Forecasts - Ask "What's the forecast for next week?"

You have {len(products)} products analyzed with {len(high_urgency)} high priority reorders and {len(anomalies)} alerts."""
        
        elif language == 'hi':
            return f"""मैं आपकी मदद कर सकता हूं:

📦 पुनः ऑर्डर सिफारिशें - पूछें "मुझे कौन से उत्पाद ऑर्डर करने चाहिए?"
🔝 शीर्ष उत्पाद - पूछें "मेरे सबसे ज़्यादा बिकने वाले उत्पाद कौन से हैं?"
⚠️ अलर्ट - पूछें "क्या कोई मांग में वृद्धि है?"
📊 पूर्वानुमान - पूछें "अगले सप्ताह का पूर्वानुमान क्या है?"

आपके पास {len(products)} उत्पाद विश्लेषित हैं जिनमें {len(high_urgency)} उच्च प्राथमिकता पुनः ऑर्डर और {len(anomalies)} अलर्ट हैं।"""
        
        else:  # Marathi
            return f"""मी तुम्हाला मदत करू शकतो:

📦 पुन्हा ऑर्डर शिफारसी - विचारा "मला कोणती उत्पादने मागवावी?"
🔝 शीर्ष उत्पादने - विचारा "माझी सर्वाधिक विक्री होणारी उत्पादने कोणती आहेत?"
⚠️ अलर्ट - विचारा "मागणीत काही वाढ आहे का?"
📊 अंदाज - विचारा "पुढील आठवड्याचा अंदाज काय आहे?"

तुमच्याकडे {len(products)} उत्पादने विश्लेषित आहेत ज्यात {len(high_urgency)} उच्च प्राधान्य पुन्हा ऑर्डर आणि {len(anomalies)} अलर्ट आहेत।"""


def get_no_data_response(language: str, message: str) -> str:
    """
    Response when no insights data is available.
    Uses LLM to answer general business questions.
    """
    logger.info("No insights data available, using LLM for general business advice")
    
    lang_instruction = {
        'en': 'Respond in English',
        'hi': 'Respond in Hindi (हिंदी)',
        'mr': 'Respond in Marathi (मराठी)'
    }.get(language, 'Respond in English')
    
    system = f"""You are an AI business advisor for Indian MSME (Micro, Small, and Medium Enterprises) merchants.

{lang_instruction}. Be conversational, helpful, and provide practical business advice.

Guidelines:
- Provide general business advice for small merchants in India
- Focus on inventory management, sales strategies, customer service, and business growth
- Use simple language suitable for small business owners
- Keep responses concise (3-5 sentences)
- Use emojis appropriately to make responses friendly
- If asked about specific product data, remind them to upload their sales data for personalized insights

Topics you can help with:
- Inventory management best practices
- Pricing strategies
- Customer retention
- Business growth tips
- Marketing for small businesses
- Cash flow management
- Seasonal planning"""
    
    user = f"""The merchant hasn't uploaded their sales data yet, so I don't have specific product information.

Merchant Question: {message}

Provide helpful general business advice. If the question requires specific data analysis, politely suggest they upload their sales data."""
    
    try:
        response = nova_converse(BEDROCK_MODEL_FAST, system, user)
        
        # Add a gentle reminder about uploading data for personalized insights
        if language == 'en':
            response += "\n\n💡 Tip: Upload your sales data to get personalized insights and forecasts for your specific products!"
        elif language == 'hi':
            response += "\n\n💡 सुझाव: अपने विशिष्ट उत्पादों के लिए व्यक्तिगत अंतर्दृष्टि और पूर्वानुमान प्राप्त करने के लिए अपना बिक्री डेटा अपलोड करें!"
        else:  # Marathi
            response += "\n\n💡 टीप: तुमच्या विशिष्ट उत्पादनांसाठी वैयक्तिक अंतर्दृष्टी आणि अंदाज मिळविण्यासाठी तुमचा विक्री डेटा अपलोड करा!"
        
        return response
        
    except Exception as e:
        logger.error(f"LLM generation failed for general query: {str(e)}")
        # Fallback response
        if language == 'en':
            return """👋 Hello! I'm your AI business advisor for inventory management and demand forecasting.

📊 To get started, please upload your sales data (CSV format with date, product_name, quantity_sold, price, revenue columns).

I can help you with:
• Demand forecasting and inventory planning
• Reorder recommendations
• Sales trend analysis
• Price optimization suggestions

Once you upload your data, I'll provide personalized insights for your business!"""
        
        elif language == 'hi':
            return """👋 नमस्ते! मैं इन्वेंटरी प्रबंधन और मांग पूर्वानुमान के लिए आपका AI व्यवसाय सलाहकार हूं।

📊 शुरू करने के लिए, कृपया अपना बिक्री डेटा अपलोड करें (CSV प्रारूप में date, product_name, quantity_sold, price, revenue कॉलम के साथ)।

मैं आपकी मदद कर सकता हूं:
• मांग पूर्वानुमान और इन्वेंटरी योजना
• पुनः ऑर्डर सिफारिशें
• बिक्री रुझान विश्लेषण
• मूल्य अनुकूलन सुझाव

एक बार जब आप अपना डेटा अपलोड कर देंगे, तो मैं आपके व्यवसाय के लिए व्यक्तिगत अंतर्दृष्टि प्रदान करूंगा!"""
        
        else:  # Marathi
            return """👋 नमस्कार! मी इन्व्हेंटरी व्यवस्थापन आणि मागणी अंदाजासाठी तुमचा AI व्यवसाय सल्लागार आहे।

📊 सुरुवात करण्यासाठी, कृपया तुमचा विक्री डेटा अपलोड करा (CSV स्वरूपात date, product_name, quantity_sold, price, revenue स्तंभांसह)।

मी तुम्हाला मदत करू शकतो:
• मागणी अंदाज आणि इन्व्हेंटरी नियोजन
• पुन्हा ऑर्डर शिफारसी
• विक्री ट्रेंड विश्लेषण
• किंमत ऑप्टिमायझेशन सूचना

एकदा तुम्ही तुमचा डेटा अपलोड केल्यावर, मी तुमच्या व्यवसायासाठी वैयक्तिक अंतर्दृष्टी प्रदान करेन!"""

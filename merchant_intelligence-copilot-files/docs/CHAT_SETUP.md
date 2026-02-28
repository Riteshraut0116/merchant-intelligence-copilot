# Chat Feature Setup Guide

## Issue: Chat Not Responding

The chat feature was showing "Sorry, I encountered an error" because the `/chat` endpoint didn't exist in the backend.

## ✅ Solution Implemented

### 1. Created Mock Chat Handler
**File**: `backend/src/handlers/chat.py`

This is a demo implementation that provides intelligent mock responses based on common questions:
- Product recommendations
- Top selling products
- Demand alerts
- Sales forecasts
- Multilingual support (English, Hindi, Marathi)

### 2. Updated Backend Template
**File**: `backend/template.yaml`

Added the ChatFunction to expose the `/chat` endpoint:
```yaml
ChatFunction:
  Type: AWS::Serverless::Function
  Properties:
    CodeUri: src/
    Handler: handlers.chat.lambda_handler
    Path: /chat
    Method: POST
```

### 3. Enhanced Frontend Error Handling
**File**: `frontend/src/pages/Chat.tsx`

Improved error messages to show:
- 🚧 Endpoint not found (404)
- ❌ Backend not running (network error)
- ⚠️ Other errors with details

## 🚀 How to Enable Chat

### Step 1: Rebuild Backend
```powershell
cd backend
sam build
```

### Step 2: Restart SAM Local
```powershell
# Stop the current SAM process (Ctrl+C)
# Then restart:
sam local start-api --port 3000
```

You should see:
```
Mounting ChatFunction at http://127.0.0.1:3000/chat [POST]
```

### Step 3: Test Chat
1. Open frontend: http://localhost:5173
2. Navigate to "Copilot Chat"
3. Try asking:
   - "Which products should I order this week?"
   - "What are my top selling products?"
   - "Are there any demand spikes?"

## 💬 Sample Questions

The mock chat handler responds intelligently to:

### Product Orders
- "Which products should I order?"
- "What should I reorder?"
- "Show me stock recommendations"

### Sales Analysis
- "What are my top selling products?"
- "Show me best sellers"
- "Which products sell the most?"

### Alerts & Anomalies
- "Are there any demand spikes?"
- "Show me alerts"
- "Any anomalies detected?"

### Forecasts
- "What's the forecast for next week?"
- "Predict future sales"
- "Show me demand predictions"

### General Help
- "What can you help me with?"
- "How do I use this?"

## 🌐 Multilingual Support

The chat works in three languages:

### English
```
User: "Which products should I order?"
Bot: "Based on your recent sales data, I recommend ordering..."
```

### Hindi (हिंदी)
```
User: "कौन से उत्पाद ऑर्डर करें?"
Bot: "आपके हाल के बिक्री डेटा के आधार पर..."
```

### Marathi (मराठी)
```
User: "कोणती उत्पादने ऑर्डर करावीत?"
Bot: "तुमच्या अलीकडील विक्री डेटावर आधारित..."
```

## 🔧 Troubleshooting

### Problem: Still getting "Chat backend not connected"

**Solution 1**: Verify endpoint is mounted
```powershell
# Check SAM Local output for:
Mounting ChatFunction at http://127.0.0.1:3000/chat [POST]
```

**Solution 2**: Test endpoint directly
```powershell
curl -X POST http://127.0.0.1:3000/chat `
  -H "Content-Type: application/json" `
  -d '{"message":"hello","language":"en"}'
```

Expected response:
```json
{
  "response": "I'm here to help...",
  "confidence": 75,
  "language": "en"
}
```

**Solution 3**: Check frontend .env
```
VITE_API_BASE_URL=http://127.0.0.1:3000
```

**Solution 4**: Clear browser cache
- Press Ctrl+Shift+R to hard refresh
- Or clear browser cache and reload

### Problem: Chat responds but in wrong language

**Solution**: Select language from dropdown at top of chat page

### Problem: Responses are generic

**Note**: This is a mock implementation for demo purposes. The responses are pre-written based on common patterns. For production, integrate with Amazon Bedrock for dynamic AI responses.

## 🎯 For Production

To replace mock responses with real AI:

1. **Update chat.py** to call Amazon Bedrock:
```python
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='ap-south-1')

response = bedrock.invoke_model(
    modelId='amazon.nova-lite-v1:0',
    body=json.dumps({
        'messages': [{'role': 'user', 'content': message}],
        'max_tokens': 500
    })
)
```

2. **Add Bedrock permissions** to template.yaml:
```yaml
Policies:
  - Statement:
    - Effect: Allow
      Action:
        - bedrock:InvokeModel
      Resource: "*"
```

3. **Retrieve merchant context** from localStorage insights:
```python
# Get insights from DynamoDB or pass from frontend
# Use insights as context for better responses
```

## ✅ Verification Checklist

- [ ] Backend rebuilt with `sam build`
- [ ] SAM Local restarted
- [ ] Chat endpoint visible in SAM output
- [ ] Frontend can send messages
- [ ] Responses appear in chat
- [ ] Language selector works
- [ ] Error messages are helpful
- [ ] Mobile responsive

## 📝 Notes

- This is a **demo implementation** for hackathon purposes
- Responses are **pre-written** and don't use actual sales data
- For production, integrate with **Amazon Bedrock** for real AI
- The mock handler provides **realistic responses** for demo purposes
- All responses include **confidence scores** and **disclaimers**

---

**Status**: ✅ Chat feature now working with mock responses  
**Next Step**: Integrate with Amazon Bedrock for production AI

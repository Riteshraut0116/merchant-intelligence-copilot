# Setup and Run Guide

## Quick Start Guide for Merchant Intelligence Copilot

This guide will help you set up and run the Merchant Intelligence Copilot with all the newly implemented features.

---

## Prerequisites

### Required Software
- **Python 3.12** or higher
- **Node.js 18** or higher
- **AWS SAM CLI** (for local backend testing)
- **AWS Account** (for Bedrock access)

### AWS Configuration
You need AWS credentials configured with access to:
- Amazon Bedrock (Nova models)
- S3 (optional, for production)
- DynamoDB (optional, for production)

---

## Backend Setup

### Step 1: Install Python Dependencies

```bash
cd merchant-intelligence-copilot/merchant_intelligence-copilot-files/backend

# Install dependencies
pip install -r src/requirements.txt
```

**Note**: Prophet installation may take a few minutes as it compiles C++ extensions.

### Step 2: Configure Environment Variables

Create a `.env` file in the `backend/src` directory:

```bash
cp src/.env.example src/.env
```

Edit `src/.env` with your AWS credentials:

```env
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BEDROCK_MODEL_PRIMARY=amazon.nova-pro-v1:0
BEDROCK_MODEL_FAST=amazon.nova-lite-v1:0
BEDROCK_MODEL_BASELINE=amazon.nova-micro-v1:0
```

### Step 3: Build and Run Backend

```bash
# Build SAM application
sam build

# Start local API (runs on http://localhost:3000)
sam local start-api --port 3000
```

**Alternative**: If SAM CLI is not installed, you can test individual Lambda functions:

```bash
# Test generate insights handler
python -c "from handlers.generate_insights import lambda_handler; print(lambda_handler({'body': '{}'}, {}))"
```

---

## Frontend Setup

### Step 1: Install Node Dependencies

```bash
cd merchant-intelligence-copilot/merchant_intelligence-copilot-files/frontend

# Install dependencies
npm install
```

### Step 2: Configure API Endpoint

Edit `frontend/src/lib/api.ts` to point to your backend:

```typescript
const API_BASE_URL = 'http://localhost:3000';  // For local development
// const API_BASE_URL = 'https://your-api-gateway-url';  // For production
```

### Step 3: Run Frontend

```bash
# Start development server (runs on http://localhost:5173)
npm run dev
```

The application will open in your browser at `http://localhost:5173`

---

## Testing the Application

### 1. Upload Sample Data

Create a sample CSV file (`sample_sales.csv`):

```csv
date,product_name,quantity_sold,price,revenue
2026-01-01,Atta 1kg,50,40,2000
2026-01-02,Atta 1kg,55,40,2200
2026-01-03,Atta 1kg,48,40,1920
2026-01-04,Atta 1kg,52,40,2080
2026-01-05,Atta 1kg,60,40,2400
2026-01-06,Atta 1kg,58,40,2320
2026-01-07,Atta 1kg,62,40,2480
2026-01-08,Atta 1kg,55,40,2200
2026-01-09,Atta 1kg,53,40,2120
2026-01-10,Atta 1kg,57,40,2280
2026-01-11,Atta 1kg,61,40,2440
2026-01-12,Atta 1kg,59,40,2360
2026-01-13,Atta 1kg,63,40,2520
2026-01-14,Atta 1kg,56,40,2240
2026-01-15,Atta 1kg,54,40,2160
2026-01-16,Atta 1kg,58,40,2320
2026-01-17,Atta 1kg,62,40,2480
2026-01-18,Atta 1kg,60,40,2400
2026-01-19,Atta 1kg,64,40,2560
2026-01-20,Atta 1kg,57,40,2280
2026-01-21,Atta 1kg,55,40,2200
2026-01-22,Atta 1kg,59,40,2360
2026-01-23,Atta 1kg,63,40,2520
2026-01-24,Atta 1kg,61,40,2440
2026-01-25,Atta 1kg,65,40,2600
2026-01-26,Atta 1kg,58,40,2320
2026-01-27,Atta 1kg,56,40,2240
2026-01-28,Atta 1kg,60,40,2400
2026-01-29,Atta 1kg,64,40,2560
2026-01-30,Atta 1kg,62,40,2480
2026-01-31,Atta 1kg,66,40,2640
2026-02-01,Rice 5kg,30,200,6000
2026-02-02,Rice 5kg,32,200,6400
2026-02-03,Rice 5kg,28,200,5600
2026-02-04,Rice 5kg,31,200,6200
2026-02-05,Rice 5kg,35,200,7000
```

### 2. Test Upload Flow

1. Navigate to **Upload Data** page
2. Select language (English/Hindi/Marathi)
3. Upload the CSV file
4. Click **Analyze Data**
5. Wait for processing (should take 10-30 seconds)

### 3. Test Dashboard

1. Navigate to **Dashboard**
2. View KPI cards (Products Analyzed, Alerts, Confidence)
3. Select a product from dropdown
4. View 7-day forecast chart
5. Click "Why?" button on any product to see explanations

### 4. Test Copilot Chat

1. Navigate to **Copilot Chat**
2. Try sample questions:
   - "What are my top selling products?"
   - "Which products should I order this week?"
   - "Are there any demand spikes?"
3. Verify responses are in selected language

### 5. Test Weekly Report

1. Navigate to **Weekly Report**
2. View AI-generated action plan
3. Check Top 3 Priorities
4. Review Risks & Alerts
5. See Quick Wins
6. Click **Export** to copy as Markdown

### 6. Test Themes and Languages

1. Navigate to **Settings**
2. Try all 5 themes:
   - Light Mode
   - Dark Mode
   - Gradient Dark
   - Glassmorphism
   - Minimal White
3. Switch between languages (EN/HI/MR)
4. Verify all pages update correctly

---

## New Features to Test

### Prophet Forecasting
- Upload data with 30+ days to see Prophet in action
- Compare forecast accuracy with previous moving average
- Check confidence scores (should be higher with more data)

### Enhanced Anomaly Detection
- Upload data with significant week-over-week changes
- Look for "spike", "drop", or "outlier" anomalies
- Check severity classification (high/medium)

### LLM Explainability
- Products with low confidence (<70%) get LLM explanations
- Products with anomalies get detailed reasoning
- High urgency reorders get action recommendations

### Weekly Report Generation
- Backend generates comprehensive action plan
- Analyzes all insights to prioritize actions
- Provides business impact estimates
- Multilingual support

---

## Troubleshooting

### Backend Issues

**Problem**: `sam build` fails
```bash
# Solution: Install AWS SAM CLI
pip install aws-sam-cli
```

**Problem**: Prophet installation fails
```bash
# Solution: Install build tools
# On Ubuntu/Debian:
sudo apt-get install python3-dev build-essential

# On macOS:
xcode-select --install

# On Windows:
# Install Visual Studio Build Tools
```

**Problem**: Bedrock access denied
```bash
# Solution: Ensure your AWS credentials have Bedrock permissions
# Add this policy to your IAM user/role:
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:InvokeModelWithResponseStream"
  ],
  "Resource": "*"
}
```

### Frontend Issues

**Problem**: API connection fails
```bash
# Solution: Check backend is running on port 3000
curl http://localhost:3000/health

# Update API_BASE_URL in frontend/src/lib/api.ts
```

**Problem**: Translations not working
```bash
# Solution: Clear browser cache and reload
# Or check browser console for errors
```

**Problem**: Charts not rendering
```bash
# Solution: Ensure recharts is installed
npm install recharts
```

---

## Production Deployment

### Backend Deployment

```bash
# Build for production
sam build

# Deploy to AWS
sam deploy --guided

# Follow prompts to configure:
# - Stack name
# - AWS Region (ap-south-1 recommended)
# - Confirm changes
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Deploy to S3 + CloudFront
aws s3 sync dist/ s3://your-bucket-name/
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## Performance Optimization

### Backend
- Prophet forecasting: ~2-5 seconds per product
- LLM calls: ~1-3 seconds per explanation
- Total processing: ~10-30 seconds for 10-20 products

### Frontend
- Initial load: <2 seconds
- Page transitions: <500ms
- Chart rendering: <1 second

### Cost Optimization
- Use Nova Lite for most LLM calls (~$0.0006 per 1K tokens)
- Cache frequent queries in localStorage
- Batch process multiple products together

---

## Support

### Documentation
- `docs/requirements.md` - Full requirements specification
- `docs/tasks.md` - Implementation task breakdown
- `docs/PENDING_TASKS_IMPLEMENTED.md` - What was implemented
- `docs/IMPLEMENTATION_COMPLETE.md` - UI enhancements summary

### Common Issues
- Check AWS credentials are configured
- Ensure Bedrock is enabled in your region
- Verify Python 3.12+ and Node 18+ are installed
- Check firewall allows localhost:3000 and localhost:5173

---

## Next Steps

1. ✅ Test all features with sample data
2. ✅ Verify multilingual support works
3. ✅ Check all themes render correctly
4. ⏳ Add authentication (Cognito)
5. ⏳ Deploy to production AWS
6. ⏳ Collect user feedback
7. ⏳ Iterate and improve

---

**Happy Testing! 🚀**

For questions or issues, refer to the documentation in the `docs/` folder.

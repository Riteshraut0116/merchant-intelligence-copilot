# Merchant Intelligence Copilot for Indian MSMEs

**AWS AI for Bharat Hackathon Submission**  
**Team:** Bharat Brain Wave |  **Lead:** Ritesh Raut  

**Theme:** AI for Retail, Commerce & Market Intelligence  

**Problem Statement:**  
Build an AI-powered solution that helps people learn faster, work smarter, or become more productive while building or understanding technology.

---

## 📘 Project Overview

### The Problem

Indian Micro, Small, and Medium Enterprises (MSMEs) represent 30% of India's GDP and employ over 110 million people. However, 80% of these businesses operate with minimal digital infrastructure, leading to:

- **30-40% inventory wastage** due to overstocking or stockouts
- **15-20% revenue loss** from suboptimal pricing decisions
- **Limited market intelligence** leading to missed demand opportunities
- **High operational friction** in understanding sales patterns and trends

Traditional business intelligence tools are too expensive (₹10,000-50,000/month), require technical expertise, and lack vernacular language support—making them inaccessible to most MSMEs.

### Why This Matters for Bharat MSMEs

MSMEs are the backbone of India's economy, yet they make critical business decisions based on intuition rather than data. A kirana store owner in Mumbai doesn't know which products to reorder, a retail shop in Pune loses money on expired stock, and merchants across India miss festival demand spikes because they lack affordable, accessible intelligence tools.

### Our Solution

Merchant Intelligence Copilot is an AI-powered decision assistant that transforms simple CSV/POS sales data into actionable business intelligence. Merchants upload their sales history, and the system generates demand forecasts, inventory recommendations, pricing insights, anomaly alerts, and multilingual action plans—all powered by AWS AI services (Amazon Bedrock, Prophet forecasting). The system is designed Bharat-first: low-cost (₹37/merchant/month), multilingual (English, Hindi, Marathi), and accessible via conversational chat interface.

---

## ✨ Key Features

- **Demand Forecasting**: 7-day and 30-day demand predictions using Prophet time-series models with confidence intervals
- **Inventory Recommendations**: Automated reorder quantity suggestions with urgency indicators to prevent stockouts
- **Anomaly Detection**: Real-time alerts for demand spikes, drops, and slow-moving products
- **Price Optimization**: Data-driven pricing suggestions based on demand elasticity and margin thresholds
- **Conversational Copilot**: Natural language Q&A interface powered by Amazon Bedrock (Claude 3) for merchant queries
- **Multilingual Support**: English, Hindi, and Marathi outputs for low-tech merchant onboarding
- **Weekly Action Plans**: Automated LLM-generated reports with top 3 priorities and expected business impact
- **Explainability**: Every recommendation includes "why" reasoning and confidence scores (0-100%)
- **Responsible AI**: Confidence scoring, disclaimers, prompt safety, and human-in-the-loop feedback

---

## 🧠 Why AI?

### Why Traditional Tools Fail for MSMEs

Rule-based systems and spreadsheets cannot:
- Capture non-linear demand patterns (festivals, weather, local events)
- Learn from historical data automatically
- Provide plain-language explanations for non-technical users
- Scale affordably for thousands of small merchants

### Role of Forecasting Models (Prophet/ARIMA)

Machine learning is essential for demand forecasting because:
- **Prophet (Meta)** automatically detects seasonality, trends, and holidays from messy business data
- **Confidence intervals** quantify prediction uncertainty, critical for inventory decisions
- **Adaptive learning** improves accuracy as more data is collected
- Without ML, merchants rely on guesswork, leading to 30-40% inventory wastage

### Role of LLM Reasoning (Amazon Bedrock)

Large Language Models transform raw forecasts into actionable intelligence:
- **Natural Language Generation**: Convert numbers into merchant-friendly recommendations ("Order 50 kg Atta by Friday")
- **Contextual Reasoning**: Explain "why" demand is changing (seasonality, trends, anomalies)
- **Multilingual Support**: Claude 3 natively supports Hindi and Marathi for Bharat-first design
- **Conversational AI**: Enable low-tech merchants to ask questions in natural language, not dashboards
- **Automated Reports**: Generate weekly action plans without manual analysis

### Why AI is Essential, Not Optional

Without AI, this system would be a basic data visualization tool. AI enables:
1. **Proactive intelligence** (predict stockouts before they happen)
2. **Explainable insights** (merchants understand "why," not just "what")
3. **Low-tech accessibility** (chat interface vs complex dashboards)
4. **Scalability** (serve 10,000+ merchants at ₹37/month each)

---

## 🏗️ Architecture Overview

### High-Level System Design

The Merchant Intelligence Copilot follows a serverless, AI-native architecture built entirely on AWS services:

**Stage 1: Data Ingestion & Validation**
- Merchants upload CSV files via React web UI (hosted on S3 + CloudFront)
- API Gateway routes requests to Lambda functions with Cognito authentication
- UploadHandler Lambda stores raw CSV in S3 and triggers DataValidator Lambda
- DataValidator cleans data (normalize, handle missing values, detect outliers) and generates quality report

**Stage 2: AI-Powered Analysis**
- ForecastGenerator Lambda trains Prophet models per product and generates 7-day/30-day forecasts
- AnomalyDetector Lambda identifies demand spikes, drops, and slow-moving products
- All forecasts and anomalies stored in DynamoDB with TTL for cost optimization

**Stage 3: LLM-Powered Reasoning & Presentation**
- ChatHandler Lambda processes merchant queries using Amazon Bedrock (Claude 3 Haiku)
- Retrieves merchant context (forecasts, anomalies) from DynamoDB and builds RAG prompts
- ReportGenerator Lambda creates weekly action plans using Claude 3 Sonnet
- All LLM outputs include confidence scores and disclaimers

**Data Storage**
- S3: Raw and cleaned CSV files with lifecycle policies (move to Glacier after 30 days)
- DynamoDB: User metadata, forecasts, chat history, weekly reports (on-demand pricing)
- ElastiCache (optional): LLM response caching for cost optimization

**Monitoring & Security**
- CloudWatch: Logs, metrics, and alarms for Lambda execution and errors
- Cognito: User authentication with JWT token validation
- IAM: Least-privilege roles for each Lambda function
- Encryption: SSE-S3 for data at rest, HTTPS/TLS 1.2+ for data in transit

### Major Components and Responsibilities

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| Frontend | React 18 + TypeScript | CSV upload, forecast dashboard, chat interface, action plan view |
| API Gateway | AWS API Gateway | REST API with Cognito authorizer, request validation, throttling |
| Upload Handler | Lambda (Python 3.11) | Process CSV uploads, store in S3, trigger validation |
| Data Validator | Lambda (Python 3.11) | Clean data, detect outliers, generate quality report |
| Forecast Generator | Lambda (Python 3.11) | Train Prophet models, generate forecasts with confidence intervals |
| Anomaly Detector | Lambda (Python 3.11) | Detect spikes, drops, slow-moving products |
| Chat Handler | Lambda (Python 3.11) | Process merchant queries, call Bedrock, return responses |
| Report Generator | Lambda (Python 3.11) | Generate weekly action plans using LLM |
| Amazon Bedrock | Claude 3 Haiku/Sonnet | LLM reasoning, explanations, multilingual support |
| DynamoDB | NoSQL Database | Store forecasts, chat history, reports (with TTL) |
| S3 | Object Storage | Store CSV files with lifecycle policies |
| Cognito | Authentication | User authentication with JWT tokens |

---

## ⚙️ Tech Stack

### Frontend
- React 18 with TypeScript
- Recharts (forecast visualizations)
- Tailwind CSS (mobile-responsive UI)
- Axios (API client)
- AWS Amplify (Cognito authentication)
- react-i18next (multilingual UI)

### Backend
- AWS Lambda (Python 3.11)
- AWS API Gateway (REST API)
- AWS Cognito (authentication)
- AWS S3 (CSV storage)
- AWS DynamoDB (metadata, forecasts, chat history)
- AWS ElastiCache Redis (optional LLM caching)

### AI / ML
- Amazon Bedrock (Claude 3 Haiku for chat, Claude 3 Sonnet for reports)
- Prophet (Meta) for time-series forecasting
- ARIMA (optional fallback for short-term predictions)
- NumPy, Pandas (data processing)

### Storage
- S3 with lifecycle policies (Glacier after 30 days)
- DynamoDB with TTL (auto-delete old forecasts after 7 days)
- On-demand capacity mode for cost optimization

### CI/CD
- AWS SAM (Infrastructure as Code)
- GitHub Actions (automated deployment)
- CloudFormation (resource provisioning)

### Responsible AI Components
- Confidence scoring (forecast + data availability)
- Prompt safety validation (injection prevention)
- Output filtering (hallucination detection)
- Human-in-the-loop feedback (thumbs up/down)
- Disclaimers on all AI-generated content

---

## 🔄 How It Works (End-to-End Flow)

### Step 1: Merchant Uploads Sales Data
1. Merchant logs in via AWS Cognito (email/password or phone OTP)
2. Uploads CSV file with columns: `date`, `product_name`, `quantity_sold`, `price`, `revenue`
3. Frontend sends file to API Gateway → UploadHandler Lambda
4. Lambda stores raw CSV in S3: `uploads/{user_id}/{timestamp}.csv`
5. Lambda triggers DataValidator Lambda asynchronously

### Step 2: Data Validation & Cleaning
1. DataValidator downloads CSV from S3 and validates required columns
2. Cleans data: normalize product names, convert dates, handle missing values
3. Detects outliers using Z-score method (threshold > 3)
4. Generates data quality report: completeness score, outliers detected, date range
5. Saves cleaned CSV to S3: `cleaned/{user_id}/{timestamp}_cleaned.csv`
6. Stores quality report in DynamoDB and triggers ForecastGenerator Lambda

### Step 3: Demand Forecasting
1. ForecastGenerator loads cleaned data and groups by product and date
2. For each product with ≥30 days of data:
   - Trains Prophet model with daily and weekly seasonality
   - Generates 7-day and 30-day forecasts with confidence intervals
   - Calculates confidence score based on prediction interval width
3. Stores forecasts in DynamoDB with TTL (auto-delete after 7 days)
4. Triggers AnomalyDetector and ReportGenerator Lambdas

### Step 4: Anomaly Detection
1. AnomalyDetector retrieves forecasts and historical data
2. Calculates week-over-week change for each product
3. Detects spikes (>30% increase), drops (>30% decrease), slow-moving (<50% average velocity)
4. Stores anomalies in DynamoDB with severity indicators (high/medium)

### Step 5: Dashboard Display
1. Frontend fetches forecasts, anomalies, and quality report from API Gateway
2. Displays forecast charts with historical data + prediction + confidence bands
3. Shows reorder recommendations with urgency indicators
4. Displays anomaly alerts with severity badges

### Step 6: Conversational Copilot (Chat)
1. Merchant types question: "Which products should I order this week?"
2. Frontend sends query to ChatHandler Lambda via API Gateway
3. Lambda retrieves merchant context (forecasts, anomalies) from DynamoDB
4. Builds RAG prompt with system instructions and merchant data
5. Calls Amazon Bedrock (Claude 3 Haiku) with temperature=0.3 for factual responses
6. Calculates confidence score based on data availability
7. Returns response with explanation, confidence score, and disclaimer
8. Frontend displays response in chat interface

### Step 7: Weekly Action Plan
1. EventBridge rule triggers ReportGenerator Lambda every Monday 8 AM
2. Lambda retrieves forecasts, anomalies, and inventory recommendations
3. Builds comprehensive prompt for Bedrock (Claude 3 Sonnet)
4. Generates structured action plan with top 3 priorities and expected impact
5. Stores report in DynamoDB and displays on dashboard

---

## 🖥️ Demo Walkthrough (For Judges)

### Suggested 3-Minute Demo Flow

**Minute 1: Problem & Solution (30 seconds)**
- Explain MSME pain points (inventory wastage, revenue loss, no intelligence tools)
- Introduce Merchant Intelligence Copilot as AI-powered decision assistant
- Highlight Bharat-first design (low-cost, multilingual, conversational)

**Minute 2: Live Demo (2 minutes)**

1. **CSV Upload (20 seconds)**
   - Show sample CSV with 90 days of sales data for 15 products
   - Upload file and display data quality report (completeness score, outliers)

2. **Demand Forecasts (30 seconds)**
   - Navigate to forecast dashboard
   - Show 7-day forecast chart with confidence bands for "Atta 1kg"
   - Click "Why?" button to expand LLM explanation
   - Highlight confidence score (85%) and color-coded badge

3. **Inventory Recommendations (20 seconds)**
   - Show reorder recommendations with quantities and urgency
   - Example: "Order 50 kg Atta by Friday (High urgency)"
   - Explain calculation: Forecasted demand + 20% safety stock

4. **Anomaly Alerts (20 seconds)**
   - Display anomaly card: "Spike in Cold Drinks (+45% this week)"
   - Show LLM-generated explanation: "Likely due to recent heatwave"

5. **Conversational Copilot (30 seconds)**
   - Type query in Hindi: "इस हफ्ते कौन से उत्पाद ऑर्डर करें?"
   - Show LLM response in Hindi with product recommendations
   - Highlight confidence score and disclaimer

6. **Weekly Action Plan (20 seconds)**
   - Navigate to weekly report
   - Show top 3 priorities with explanations and expected impact
   - Emphasize automated generation (saves 5+ hours/week)

**Minute 3: Responsible AI & Impact (30 seconds)**
- Highlight confidence scoring, explainability, and disclaimers
- Show cost efficiency: ₹37/merchant/month (100x cheaper than traditional tools)
- Mention scalability: Designed for 10,000+ MSMEs across India

---

## 🚀 Getting Started (Prototype Setup)

### Prerequisites

- AWS Account with access to:
  - Lambda, API Gateway, S3, DynamoDB, Cognito
  - Amazon Bedrock (Claude 3 models enabled in ap-south-1 region)
- AWS CLI configured with credentials
- AWS SAM CLI installed
- Node.js 18+ and npm
- Python 3.11+
- Git

### High-Level Setup Steps

**1. Clone Repository**
```bash
git clone https://github.com/your-team/merchant-intelligence-copilot.git
cd merchant-intelligence-copilot
```

**2. Deploy Backend Infrastructure**
```bash
# Install Python dependencies for Lambda Layer
pip install -r layers/ml_dependencies/requirements.txt -t layers/ml_dependencies/python

# Build and deploy SAM application
sam build
sam deploy --guided --region ap-south-1

# Note: Follow prompts to configure stack name, S3 bucket, and Cognito settings
```

**3. Configure Frontend**
```bash
cd frontend

# Install dependencies
npm install

# Create .env file with API Gateway and Cognito endpoints
# (Outputs from SAM deployment)
echo "REACT_APP_API_ENDPOINT=<API_GATEWAY_URL>" > .env
echo "REACT_APP_COGNITO_USER_POOL_ID=<USER_POOL_ID>" >> .env
echo "REACT_APP_COGNITO_CLIENT_ID=<CLIENT_ID>" >> .env

# Build and deploy frontend to S3
npm run build
aws s3 sync build/ s3://merchant-copilot-frontend/
```

**4. Create Demo User**
```bash
# Create test user in Cognito
aws cognito-idp admin-create-user \
  --user-pool-id <USER_POOL_ID> \
  --username demo@example.com \
  --temporary-password TempPass123! \
  --region ap-south-1
```

**5. Upload Sample Data**
- Navigate to frontend URL (CloudFront distribution or S3 static website)
- Login with demo credentials
- Upload sample CSV from `sample-data/msme_sales_90days.csv`
- Wait 60 seconds for forecasts to generate

### Environment Assumptions

- Single-region deployment (ap-south-1 Mumbai) for data localization
- Bedrock models (Claude 3 Haiku, Claude 3 Sonnet) enabled in AWS account
- Budget: ~$50/month for 100 merchants (MVP phase)
- Demo data: 90 days of sales history for 15 products

---

## 🛡️ Responsible AI & Ethics

### Explainability

Every AI recommendation includes transparent reasoning:
- **Forecast Explanations**: LLM generates plain-language explanations for demand trends ("Demand increasing due to weekly seasonality and upcoming festival")
- **Anomaly Explanations**: System explains possible causes for spikes/drops ("Spike in Cold Drinks likely due to heatwave")
- **Inventory Recommendations**: Shows calculation logic (Forecasted demand + 20% safety stock)
- **UI Design**: Every recommendation card has "Why?" button to expand full explanation

### Confidence Scoring

All AI outputs include quantified uncertainty:
- **Forecast Confidence**: Based on prediction interval width (narrow = high confidence)
- **Data Availability Confidence**: Based on historical data quantity (90+ days = 90% confidence)
- **Combined Score**: Weighted average (70% forecast, 30% data availability)
- **Display Strategy**: Color-coded badges (Green >80%, Yellow 60-80%, Red <60%)
- **Low Confidence Warning**: Recommendations <60% flagged with "Verify manually" disclaimer

### Disclaimers

Displayed prominently throughout the system:
- **Dashboard Header**: "AI‑assisted insights to support smarter business decisions."
- **Chat Interface**: "This is an AI assistant. Always use your business judgment."
- **Weekly Reports**: "Automated insights. Review with your business knowledge."
- **API Responses**: Every response includes disclaimer field

### Bias & Hallucination Control

**Input Validation**:
- Reject prompt injection patterns ("ignore previous instructions", SQL injection)
- Limit message length (max 500 characters)
- Validate queries are business-related (not off-topic)

**Output Filtering**:
- Check if LLM hallucinated product names not in merchant's data
- Remove hallucinated products from responses
- Use Bedrock Guardrails for unsafe content filtering

**Grounding in Data (RAG)**:
- Always include merchant's actual data in prompts
- Instruct LLM: "Only use data provided. Never make up product names or numbers."
- Validate JSON schema for structured outputs

**Bias Mitigation**:
- Test models across diverse product categories, regions, and merchant sizes
- Monitor for systematic over/under-forecasting by category
- Use fairness metrics (forecast accuracy parity across categories)

### Human-in-the-Loop Approach

**Merchant Feedback**:
- Every recommendation has thumbs up/down button
- Feedback stored in DynamoDB for review
- Low-rated responses flagged for admin investigation

**Admin Oversight**:
- Dashboard to view low-confidence outputs (<60%)
- Review user feedback (thumbs down ratings)
- Monitor anomaly detection false positives
- Adjust prompt templates based on feedback

**Escalation Path**:
- Merchant reports incorrect recommendation → Admin investigates
- Root cause analysis: data quality, model error, or prompt issue
- Corrective action: update prompt, retrain model, or improve validation

---

## 🌐 Bharat-First Design

### Low-Data Onboarding

- **CSV Upload**: No API integrations or POS system required—merchants export sales data manually
- **Minimal Data Requirements**: Works with just 30 days of history (though 90+ days recommended)
- **Automatic Data Cleaning**: Handles missing values, inconsistent product names, and outliers
- **Data Quality Report**: Transparent feedback on completeness and issues detected

### Multilingual Support

- **Languages**: English, Hindi, Marathi (expandable to Tamil, Telugu, Bengali)
- **Native LLM Support**: Claude 3 natively generates Hindi/Marathi responses (no translation API needed)
- **UI Localization**: react-i18next for static text translation
- **Language Selection**: Dropdown in UI, preference stored in localStorage
- **Fallback Logic**: Defaults to English if requested language fails

### Accessibility for Non-Technical Users

- **Conversational Interface**: Merchants ask questions in natural language, not SQL queries
- **Plain-Language Outputs**: "Order 50 kg Atta by Friday" instead of "Forecasted demand: 395 units"
- **Mobile-Responsive**: Tailwind CSS ensures usability on basic smartphones
- **Visual Indicators**: Color-coded confidence badges, urgency icons, severity alerts
- **No Jargon**: LLM instructed to avoid technical terms (e.g., "confidence interval" → "how sure we are")

### Cost Efficiency

- **Target Cost**: ₹37/merchant/month (~$0.45)
- **100x Cheaper**: Traditional BI tools cost ₹10,000-50,000/month
- **Serverless Architecture**: Pay-per-use (no always-on servers)
- **Optimization**: LLM caching, token limits, on-demand DynamoDB, S3 lifecycle policies

---

## 📊 Success Metrics

### Business Impact KPIs

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Inventory Wastage Reduction | 20% | Compare stockouts and overstocking before/after adoption |
| Revenue Increase | 10-15% | Track sales growth from optimized pricing and stockout prevention |
| Time Saved per Merchant | 5+ hours/week | Survey merchants on manual analysis time eliminated |
| Merchant Adoption | 10,000+ MSMEs | User signups within 12 months post-launch |

### AI Effectiveness Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Demand Forecast Accuracy (MAPE) | <20% | Mean Absolute Percentage Error on test data |
| LLM Response Relevance | >85% | Human evaluation of 100 sample responses |
| Confidence Score Calibration | >80% | Alignment between predicted confidence and actual accuracy |
| Multilingual Output Quality | >90% | Native speaker evaluation (Hindi, Marathi) |
| Anomaly Detection Precision | >75% | True positives / (True positives + False positives) |

### User Engagement Metrics

- Weekly Active Users (WAU): >70% of registered merchants
- Chat Queries per Merchant: 10-15/week
- CSV Upload Frequency: 1-2/week (weekly data refresh)
- Feedback Submission Rate: >30% of recommendations rated

---

## 💰 Cost Considerations

### Estimated AWS Costs (Per Merchant/Month)

| Service | Usage | Cost |
|---------|-------|------|
| Amazon Bedrock | 50 chat queries + 4 reports | $0.017 (~₹1.40) |
| AWS Lambda | 6 functions, 200 invocations | $0.026 (~₹2.15) |
| DynamoDB | 1500 reads, 150 writes, 2 MB storage | $0.41 (~₹34) |
| S3 | 20 MB storage, lifecycle policies | $0.0004 (~₹0.03) |
| **Total per Merchant** | | **$0.45/month (~₹37)** |

### Shared Costs (100 Merchants)

| Service | Cost |
|---------|------|
| API Gateway | $1/month |
| CloudFront | $2/month |
| Cognito | Free tier (50,000 MAUs) |
| **Grand Total (100 merchants)** | **~$50/month** |

### Optimization Strategies

**Bedrock Cost Control**:
- Use Claude 3 Haiku (cheapest) for chat, Claude 3 Sonnet only for complex reports
- Limit context window to top 5 products (reduce tokens)
- Set max_tokens=500 for chat, 1000 for reports
- Cache frequent queries in ElastiCache (optional)

**Lambda Optimization**:
- Right-size memory (512 MB for simple tasks, 2048 MB only for ML inference)
- Use async invocations for non-blocking tasks
- Package dependencies in Lambda Layer (reduce cold starts)

**DynamoDB Optimization**:
- Use on-demand pricing (pay-per-request)
- Enable TTL to auto-delete old forecasts after 7 days
- Avoid over-indexing (only create GSIs for frequent queries)

**S3 Optimization**:
- Lifecycle policies: Move uploads to Glacier after 30 days, delete cleaned data after 90 days
- Compress CSV files with gzip (70-80% size reduction)

---

## 🔮 Future Enhancements

### WhatsApp Integration

- Merchants interact with Copilot via WhatsApp Business API (no app required)
- Weekly reports delivered as WhatsApp messages
- Alerts sent as WhatsApp notifications
- Architecture: WhatsApp webhook → API Gateway → Lambda → Bedrock → WhatsApp response

### Voice Assistant

- Merchants ask questions via voice in Hindi/Marathi
- AWS Transcribe (speech-to-text) → ChatHandler → Bedrock → AWS Polly (text-to-speech)
- Enables hands-free interaction for busy shop owners

### Market Intelligence Retrieval

- Integrate external data sources (weather, festivals, local events)
- Enrich forecasts with macro trends ("Heatwave → Cold Drinks demand spike")
- Use web scraping or APIs for competitor price monitoring

### Multi-Store Management

- Merchants manage inventory across multiple locations
- Consolidated dashboard with store-level drill-down
- Transfer recommendations (move stock from Store A to Store B)

### Supplier Integration

- Auto-generate purchase orders based on reorder recommendations
- Send POs to suppliers via email/API
- Track order status and delivery timelines

### Financial Insights

- Profit/loss analysis per product
- Cash flow forecasting
- Working capital optimization

### Advanced ML Models

- Deep learning (LSTM, Transformer) for complex demand patterns
- Reinforcement learning for dynamic pricing
- Causal inference to understand "why" demand changed

---

## 🏆 Hackathon Submission Checklist

### MVP Readiness

- [x] CSV upload and data validation pipeline functional
- [x] Demand forecasting with Prophet (7-day and 30-day)
- [x] Anomaly detection (spikes, drops, slow-moving products)
- [x] Conversational Copilot chat with Amazon Bedrock
- [x] Multilingual support (English, Hindi, Marathi)
- [x] Confidence scoring on all AI outputs
- [x] Explainability ("Why?" for every recommendation)
- [x] Disclaimers on dashboard, chat, and reports
- [x] Weekly action plan generation
- [x] Mobile-responsive React frontend

### Demo Readiness

- [x] Sample CSV data (90 days, 15 products) prepared
- [x] Demo user account created in Cognito
- [x] 3-minute demo script finalized
- [x] Backup demo video recorded (5 minutes)
- [x] All Lambda functions tested end-to-end
- [x] Frontend deployed to S3 + CloudFront
- [x] API Gateway endpoints tested with Postman

### Documentation Completeness

- [x] README.md with architecture, setup, and demo walkthrough
- [x] Requirements document (problem, features, acceptance criteria)
- [x] Design document (architecture, AI design, cost optimization)
- [x] Implementation tasks document (22 tasks with sub-tasks)
- [x] SAM template (Infrastructure as Code)
- [x] API documentation (endpoints, request/response formats)

### Responsible AI Compliance

- [x] Confidence scores displayed on all AI outputs
- [x] Disclaimers on dashboard, chat, and reports
- [x] Prompt safety validation (injection prevention)
- [x] Output filtering (hallucination detection)
- [x] Human-in-the-loop feedback (thumbs up/down)
- [x] Bias mitigation testing across product categories

### Bharat-First Validation

- [x] CSV upload (no API integrations required)
- [x] Multilingual UI and LLM outputs (Hindi, Marathi)
- [x] Mobile-responsive design (tested on basic smartphones)
- [x] Cost efficiency (₹37/merchant/month)
- [x] Plain-language outputs (no technical jargon)

---

## 👥 Team

**Team Name:** Bharat Brain Wave  
**Team Lead:** Ritesh Raut  
**Hackathon:** AWS AI for Bharat Hackathon  
**Theme:** AI for Retail, Commerce & Market Intelligence

---

## 📄 License

This project is submitted for the AWS AI for Bharat Hackathon. All rights reserved by Team Bharat Brain Wave.

---

## 🙏 Acknowledgments

- AWS for hosting the AI for Bharat Hackathon
- Meta for the Prophet forecasting library
- Anthropic for Claude 3 models via Amazon Bedrock
- Indian MSME community for inspiring this solution

---

## 👤 Author

**Ritesh Raut**  
*Programmer Analyst, Cognizant*

AI-powered decision copilot for Bharat’s MSME sellers 📊🤖

---

### 🌐 Connect with me:
<p align="left">
<a href="https://github.com/Riteshraut0116" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg" alt="Riteshraut0116" height="30" width="40" /></a>
<a href="https://linkedin.com/in/ritesh-raut-9aa4b71ba" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="ritesh-raut-9aa4b71ba" height="30" width="40" /></a>
<a href="https://www.instagram.com/riteshraut1601/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="riteshraut1601" height="30" width="40" /></a>
<a href="https://www.facebook.com/ritesh.raut.649321/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/facebook.svg" alt="ritesh.raut.649321" height="30" width="40" /></a>
</p>

---


**Built with ❤️ for Bharat MSMEs**







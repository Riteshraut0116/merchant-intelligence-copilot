# Requirements Document: Merchant Intelligence Copilot for Indian MSMEs

## 📘 1. Project Overview

### 1.1 Problem Statement

Indian Micro, Small, and Medium Enterprises (MSMEs) represent 30% of India's GDP and employ over 110 million people. However, 80% of these businesses operate with minimal digital infrastructure, relying on manual record-keeping, intuition-based inventory decisions, and reactive pricing strategies. This results in:

- **30-40% inventory wastage** due to overstocking or stockouts
- **15-20% revenue loss** from suboptimal pricing decisions
- **Limited market intelligence** leading to missed demand opportunities
- **High operational friction** in understanding sales patterns and trends

Traditional business intelligence tools are:
- Too expensive for MSMEs (₹10,000-50,000/month)
- Require technical expertise to operate
- Not designed for low-data, high-variability MSME contexts
- Lack vernacular language support

### 1.2 Why AI is Required

**AI is not optional—it is essential** for solving this problem:

1. **Demand Forecasting (Time-Series ML)**
   - MSMEs have irregular, seasonal, and event-driven demand patterns
   - Traditional rule-based systems cannot capture non-linear relationships
   - ML models (ARIMA, Prophet, LSTM) can learn from limited historical data and predict future demand with confidence intervals

2. **Natural Language Reasoning (LLM)**
   - MSME owners need **actionable insights, not raw numbers**
   - LLMs (via Amazon Bedrock) can:
     - Convert forecasts into plain-language recommendations
     - Explain "why" a product is trending or declining
     - Generate multilingual action plans (Hindi, Marathi, English)
     - Answer merchant questions in conversational format
   - Enables **low-tech onboarding**: merchants interact via chat, not dashboards

3. **Intelligent Automation**
   - AI-driven anomaly detection identifies sudden demand spikes or drops
   - Price optimization considers competitor data, margins, and demand elasticity
   - Automated weekly reports reduce manual analysis time from hours to seconds

### 1.3 Why This Solution is Relevant for Bharat MSMEs

This solution is **Bharat-first** by design:

- **Low-Tech Onboarding**: CSV upload (no API integrations required)
- **Vernacular Support**: Hindi, Marathi, English outputs
- **Explainability**: Every recommendation includes "why" and confidence scores
- **Cost-Effective**: AWS Bedrock pay-per-use model (₹500-2000/month estimated)
- **Mobile-First**: Lightweight web interface accessible on basic smartphones
- **Trust-Building**: Confidence scores and disclaimers ensure merchants retain decision control
- **Scalable**: Designed for 10,000+ MSME merchants across India

---

## 🎯 2. Goals & Success Metrics

### 2.1 Business Goals

1. **Reduce inventory wastage by 20%** through accurate demand forecasting
2. **Increase revenue by 10-15%** via optimized pricing and stockout prevention
3. **Save 5+ hours/week** per merchant on manual data analysis
4. **Enable data-driven decisions** for 10,000+ MSMEs within 12 months post-launch

### 2.2 AI Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Demand Forecast Accuracy (MAPE) | <20% | Mean Absolute Percentage Error on test data |
| LLM Response Relevance | >85% | Human evaluation of 100 sample responses |
| Confidence Score Calibration | >80% | Alignment between predicted confidence and actual accuracy |
| Multilingual Output Quality | >90% | Native speaker evaluation (Hindi, Marathi) |
| Anomaly Detection Precision | >75% | True positives / (True positives + False positives) |

### 2.3 Hackathon-Aligned KPIs

- **Meaningful AI Use**: Forecasting + LLM reasoning + anomaly detection
- **Bharat-First**: CSV upload, multilingual, explainable, low-cost
- **Responsible AI**: Confidence scores, disclaimers, bias controls
- **Feasibility**: MVP deployable on AWS in 48 hours
- **Impact**: Clear problem-solution mapping with measurable outcomes

---

## 👤 3. User Personas

### 3.1 MSME Merchant (Primary User)

**Profile**: Rajesh Kumar, 42, Kirana Store Owner, Mumbai

- **Tech Literacy**: Basic smartphone usage, WhatsApp proficient
- **Pain Points**: 
  - Doesn't know which products to reorder
  - Loses money on expired/unsold stock
  - Competitors undercut prices without warning
- **Goals**: 
  - Understand what to stock next week
  - Avoid stockouts during festivals
  - Get simple, actionable advice in Hindi
- **Success Criteria**: Can upload sales CSV and get recommendations in <5 minutes

### 3.2 Store Manager (Secondary User)

**Profile**: Priya Sharma, 28, Managing 3 retail outlets, Pune

- **Tech Literacy**: Moderate (uses Excel, Google Sheets)
- **Pain Points**:
  - Managing inventory across multiple stores
  - Identifying slow-moving products
  - Tracking weekly performance trends
- **Goals**:
  - Weekly automated reports
  - Alerts for stockouts or anomalies
  - Price optimization suggestions
- **Success Criteria**: Receives actionable weekly insights without manual analysis

### 3.3 Admin (System User)

**Profile**: System Administrator / Hackathon Team

- **Responsibilities**:
  - Monitor system health
  - Review AI output quality
  - Manage user onboarding
  - Optimize AWS costs
- **Goals**:
  - Ensure 99% uptime
  - Keep Bedrock costs under budget
  - Track user engagement metrics

---

## ⚙️ 4. Functional Requirements

### 4.1 Data Ingestion & Validation

**FR-1.1: CSV/POS Data Upload**
- **Description**: Merchants upload sales data via CSV file
- **Acceptance Criteria**:
  - Supports CSV files up to 10MB
  - Required columns: `date`, `product_name`, `quantity_sold`, `price`, `revenue`
  - Optional columns: `category`, `cost_price`, `supplier`
  - Validates file format and column headers
  - Provides clear error messages for invalid files
- **AI Justification**: Clean data is essential for accurate ML forecasting

**FR-1.2: Data Cleaning & Preprocessing**
- **Description**: Automatically clean and normalize uploaded data
- **Acceptance Criteria**:
  - Handle missing values (forward-fill for dates, median for prices)
  - Detect and flag outliers (Z-score > 3)
  - Normalize product names (case-insensitive, trim whitespace)
  - Convert dates to standard format (YYYY-MM-DD)
  - Generate data quality report (% completeness, outliers detected)
- **AI Justification**: ML models require clean, structured data for reliable predictions

### 4.2 Demand Forecasting

**FR-2.1: Daily/Weekly Demand Forecasts**
- **Description**: Predict future demand for each product
- **Acceptance Criteria**:
  - Generate 7-day and 30-day demand forecasts
  - Use time-series ML models (Prophet, ARIMA, or AWS Forecast)
  - Provide confidence intervals (lower bound, upper bound)
  - Display forecasts in tabular and chart formats
  - Update forecasts weekly as new data is uploaded
- **AI Justification**: ML captures seasonality, trends, and non-linear patterns that rule-based systems cannot

**FR-2.2: Forecast Explainability**
- **Description**: Explain why demand is predicted to increase/decrease
- **Acceptance Criteria**:
  - Identify key drivers (seasonality, trend, recent spikes)
  - Use LLM to generate plain-language explanations
  - Example: "Demand for 'Atta' is expected to rise 20% next week due to upcoming festival season"
  - Confidence score displayed (0-100%)
- **AI Justification**: LLMs convert ML outputs into actionable merchant insights

### 4.3 Inventory Recommendations

**FR-3.1: Reorder Quantity Suggestions**
- **Description**: Recommend optimal reorder quantities per product
- **Acceptance Criteria**:
  - Calculate reorder quantity based on forecasted demand + safety stock
  - Consider lead time (default: 3 days, user-configurable)
  - Flag products at risk of stockout (current stock < 7-day forecast)
  - Provide "order now" vs "wait" recommendations
  - Display in merchant-friendly format: "Order 50 kg Atta by Friday"
- **AI Justification**: ML forecasts enable proactive inventory planning vs reactive ordering

**FR-3.2: Slow-Moving Product Alerts**
- **Description**: Identify products with declining demand
- **Acceptance Criteria**:
  - Detect products with <50% of average sales velocity
  - Suggest discount pricing or bundling strategies
  - LLM generates action plan: "Consider 10% discount on Product X to clear stock"
  - Confidence score for recommendation
- **AI Justification**: Anomaly detection + LLM reasoning automate inventory optimization

### 4.4 Price Intelligence

**FR-4.1: Price Optimization Suggestions**
- **Description**: Recommend optimal pricing based on demand and margins
- **Acceptance Criteria**:
  - Calculate price elasticity from historical data
  - Suggest price adjustments (+/- 5-15%) to maximize revenue
  - Ensure minimum margin threshold (user-configurable, default: 20%)
  - Display expected revenue impact: "Increase price by ₹5 → +8% revenue"
  - LLM explains reasoning: "Demand is inelastic; customers will pay more"
- **AI Justification**: ML models optimize pricing dynamically based on demand patterns

**FR-4.2: Competitor Price Monitoring (Future)**
- **Description**: Track competitor prices and suggest adjustments
- **Acceptance Criteria**:
  - (Out of scope for MVP, listed for future enhancement)

### 4.5 Trend Detection & Anomaly Alerts

**FR-5.1: Demand Spike/Drop Detection**
- **Description**: Automatically detect unusual demand patterns
- **Acceptance Criteria**:
  - Flag products with >30% demand change week-over-week
  - Classify as "spike" (positive) or "drop" (negative)
  - Send real-time alerts via dashboard
  - LLM explains possible causes: "Spike in 'Cold Drinks' likely due to heatwave"
- **AI Justification**: ML-based anomaly detection identifies opportunities and risks faster than manual analysis

**FR-5.2: Seasonal Trend Insights**
- **Description**: Identify recurring seasonal patterns
- **Acceptance Criteria**:
  - Detect monthly/quarterly seasonality in sales data
  - Highlight upcoming high-demand periods (festivals, holidays)
  - LLM generates proactive recommendations: "Stock up on 'Sweets' 2 weeks before Diwali"
- **AI Justification**: Time-series ML captures complex seasonal patterns

### 4.6 Merchant Copilot Chat (Q&A)

**FR-6.1: Conversational AI Assistant**
- **Description**: Merchants ask questions in natural language
- **Acceptance Criteria**:
  - Support queries like:
    - "Which products should I order this week?"
    - "Why is Product X selling less?"
    - "What is my best-selling category?"
  - LLM (Bedrock) generates context-aware responses using merchant's data
  - Responses include confidence scores
  - Multilingual support (English, Hindi, Marathi)
  - Chat history persisted per user session
- **AI Justification**: LLMs enable low-tech merchants to interact with data via conversation, not dashboards

**FR-6.2: Prompt Safety & Input Validation**
- **Description**: Prevent prompt injection and malicious inputs
- **Acceptance Criteria**:
  - Validate user inputs for SQL injection, XSS, prompt injection patterns
  - Reject queries unrelated to merchant data (e.g., "Write me a poem")
  - Log suspicious queries for review
  - Display disclaimer: "AI-generated advice. Verify before acting."
- **AI Justification**: Responsible AI requires input validation to prevent misuse

### 4.7 Multilingual Outputs

**FR-7.1: Language Selection**
- **Description**: Merchants choose preferred language
- **Acceptance Criteria**:
  - Support English, Hindi, Marathi
  - Language selection persisted per user
  - All LLM-generated text (recommendations, explanations, chat) translated
  - Use Bedrock's multilingual capabilities or AWS Translate
- **AI Justification**: Bharat-first design requires vernacular support for MSME adoption

### 4.8 Auto-Generated Weekly Action Plans

**FR-8.1: Weekly Merchant Report**
- **Description**: Automated summary of key insights and actions
- **Acceptance Criteria**:
  - Generated every Monday morning
  - Includes:
    - Top 5 products to reorder
    - Slow-moving products to discount
    - Demand trends (up/down)
    - Price optimization suggestions
    - Anomalies detected
  - Delivered via email or dashboard
  - LLM generates executive summary in merchant's language
- **AI Justification**: LLMs automate report generation, saving merchants hours of manual analysis

### 4.9 Explainability & Confidence Scoring

**FR-9.1: Confidence Scores for All AI Outputs**
- **Description**: Every AI recommendation includes confidence level
- **Acceptance Criteria**:
  - Confidence score (0-100%) displayed for:
    - Demand forecasts
    - Inventory recommendations
    - Price suggestions
    - Anomaly alerts
    - Chat responses
  - Color-coded: Green (>80%), Yellow (60-80%), Red (<60%)
  - Low-confidence outputs include disclaimer: "Low confidence. Verify manually."
- **AI Justification**: Responsible AI requires transparency about prediction uncertainty

**FR-9.2: Explainability ("Why" Behind Recommendations)**
- **Description**: LLM explains reasoning for each recommendation
- **Acceptance Criteria**:
  - Every recommendation includes "Why?" section
  - Example: "Reorder 100 units of Product X because demand is forecasted to increase 25% next week due to festival season"
  - Explanations generated by LLM using forecast data + context
  - Merchant can expand/collapse explanations
- **AI Justification**: Explainability builds merchant trust and enables informed decision-making

### 4.10 Alerts & Notifications

**FR-10.1: Stockout Risk Alerts**
- **Description**: Notify merchants when products are at risk of stockout
- **Acceptance Criteria**:
  - Alert triggered when current stock < 7-day forecasted demand
  - Displayed on dashboard with urgency indicator (High/Medium/Low)
  - Includes recommended reorder quantity
  - Optional: Email/SMS notifications (future enhancement)
- **AI Justification**: ML forecasts enable proactive stockout prevention

**FR-10.2: Slow-Moving Product Alerts**
- **Description**: Notify merchants of products with declining sales
- **Acceptance Criteria**:
  - Alert triggered when sales velocity drops >30% over 2 weeks
  - Suggests action: discount, bundle, or discontinue
  - LLM explains possible causes
- **AI Justification**: Anomaly detection + LLM reasoning automate inventory optimization

---

## 🧩 5. Non-Functional Requirements

### 5.1 Scalability

**NFR-1.1: Support 10,000+ Concurrent Users**
- Use AWS Lambda for serverless compute (auto-scaling)
- DynamoDB for user data (scales automatically)
- S3 for CSV storage (unlimited capacity)

**NFR-1.2: Handle 100,000+ Products per Merchant**
- Optimize ML inference for large datasets
- Use batch processing for forecasts (AWS Batch or Step Functions)

### 5.2 Performance

**NFR-2.1: Response Times**
- CSV upload processing: <30 seconds for 10MB file
- Demand forecast generation: <60 seconds for 100 products
- Chat response: <5 seconds per query
- Dashboard load time: <3 seconds

**NFR-2.2: Forecast Accuracy**
- Mean Absolute Percentage Error (MAPE) <20% for 7-day forecasts
- Continuously improve models with user feedback

### 5.3 Security

**NFR-3.1: Data Encryption**
- Encrypt data at rest (S3, DynamoDB) using AWS KMS
- Encrypt data in transit (HTTPS/TLS 1.2+)

**NFR-3.2: Access Control**
- User authentication via AWS Cognito
- Role-based access control (Merchant, Admin)
- Merchants can only access their own data

**NFR-3.3: Input Validation**
- Sanitize all user inputs (CSV, chat queries)
- Prevent SQL injection, XSS, prompt injection

### 5.4 Cost Efficiency

**NFR-4.1: Optimize AWS Bedrock Usage**
- Cache frequent LLM queries (Redis/ElastiCache)
- Use smaller models for simple tasks (Claude Haiku vs Sonnet)
- Batch LLM requests where possible
- Target cost: ₹500-2000/month per merchant

**NFR-4.2: Serverless Architecture**
- Use Lambda (pay-per-invocation) vs EC2 (always-on)
- DynamoDB on-demand pricing (pay-per-request)

### 5.5 Availability

**NFR-5.1: Uptime**
- Target: 99% uptime (allows ~7 hours downtime/month)
- Use AWS multi-AZ deployments for resilience

**NFR-5.2: Disaster Recovery**
- Daily backups of user data (S3 versioning, DynamoDB backups)
- Recovery Time Objective (RTO): <4 hours

### 5.6 Data Privacy

**NFR-6.1: MSME Data Safety**
- Merchant data isolated per user (no cross-contamination)
- No data sharing with third parties
- Compliance with India's Digital Personal Data Protection Act (DPDPA) 2023
- Data retention policy: 2 years (user-configurable)

**NFR-6.2: Anonymization**
- Aggregate analytics use anonymized data only
- No PII in logs or error messages

---

## 🛡️ 6. Responsible AI Requirements (MANDATORY)

### 6.1 Confidence Scores

**RAI-1.1: Display Confidence for All AI Outputs**
- Every forecast, recommendation, and chat response includes confidence score (0-100%)
- Low-confidence outputs (<60%) flagged with warning icon
- Merchants can filter recommendations by confidence threshold

**RAI-1.2: Confidence Calibration**
- Regularly validate that confidence scores align with actual accuracy
- Example: 80% confidence predictions should be correct 80% of the time
- Use calibration plots to monitor and adjust

### 6.2 Disclaimers

**RAI-2.1: AI-Generated Content Disclaimer**
- Display on every page: "AI-generated recommendations. Verify before acting."
- Chat responses include: "This is AI-generated advice. Use your judgment."
- Weekly reports include: "Automated insights. Review with your business knowledge."

**RAI-2.2: Liability Disclaimer**
- Terms of Service: "Merchant Intelligence Copilot provides decision support, not guarantees. Final decisions are the merchant's responsibility."

### 6.3 Bias & Hallucination Control

**RAI-3.1: Bias Mitigation**
- Test ML models across diverse product categories, regions, and merchant sizes
- Monitor for systematic over/under-forecasting by category
- Use fairness metrics (e.g., forecast accuracy parity across categories)

**RAI-3.2: Hallucination Prevention**
- LLM responses grounded in merchant's actual data (RAG pattern)
- Reject queries outside merchant data scope
- Log and review LLM outputs for factual errors
- Use Bedrock Guardrails to filter unsafe/irrelevant outputs

**RAI-3.3: Human-in-the-Loop**
- Merchants can provide feedback on recommendations (thumbs up/down)
- Feedback used to retrain models and improve LLM prompts
- Admin reviews flagged outputs weekly

### 6.4 Input Validation & Prompt Safety

**RAI-4.1: Prompt Injection Prevention**
- Validate chat inputs for malicious patterns
- Reject queries like: "Ignore previous instructions and..."
- Use Bedrock's built-in prompt safety features

**RAI-4.2: Data Validation**
- Reject CSV files with suspicious content (SQL commands, scripts)
- Sanitize product names and text fields

### 6.5 Explainability

**RAI-5.1: Transparent AI Reasoning**
- Every recommendation includes "Why?" explanation
- Forecast charts show historical data + prediction + confidence interval
- Merchants can drill down into model inputs (seasonality, trend components)

**RAI-5.2: Model Documentation**
- Publicly document ML models used (Prophet, ARIMA, etc.)
- Explain how forecasts are generated (training data, features, algorithms)

---

## 🏗️ 7. Technical Constraints

### 7.1 AWS-Only Stack

**TC-1.1: Mandatory AWS Services**
- Compute: AWS Lambda
- Storage: S3, DynamoDB
- AI/ML: Amazon Bedrock (Claude 3), AWS Forecast (optional)
- Auth: AWS Cognito
- API: API Gateway
- Monitoring: CloudWatch

**TC-1.2: No Third-Party AI APIs**
- Cannot use OpenAI, Google Gemini, etc.
- Must use Amazon Bedrock for LLM capabilities

### 7.2 Low-Cost MVP

**TC-2.1: Budget Constraints**
- Target AWS cost: <$500/month for 100 merchants (MVP phase)
- Optimize Bedrock token usage (cache, batch, smaller models)
- Use serverless architecture (no EC2 instances)

### 7.3 Lightweight Deployment

**TC-3.1: Hackathon Deployment**
- Deployable via AWS SAM or CDK in <2 hours
- Infrastructure-as-Code (IaC) for reproducibility
- Single-region deployment (ap-south-1 Mumbai)

**TC-3.2: Frontend**
- Simple web UI (React or Next.js)
- Mobile-responsive (Bootstrap or Tailwind CSS)
- Hosted on S3 + CloudFront (static site)

---

## ⚠️ 8. Assumptions & Limitations

### 8.1 Assumptions

**A-1**: Merchants have at least 3 months of historical sales data for accurate forecasting

**A-2**: Merchants can export sales data as CSV from their POS system or maintain manual records

**A-3**: Merchants have basic smartphone/computer access and internet connectivity

**A-4**: Product names are reasonably consistent (e.g., "Atta 1kg" vs "Atta 1 kg" can be normalized)

**A-5**: Merchants trust AI recommendations if explainability and confidence scores are provided

### 8.2 Limitations

**L-1**: Forecast accuracy degrades for products with <30 days of sales history

**L-2**: Price optimization assumes no external competitor data (uses only merchant's historical data)

**L-3**: Multilingual support limited to English, Hindi, Marathi (MVP phase)

**L-4**: No real-time inventory sync (merchants manually upload CSV weekly)

**L-5**: LLM responses may occasionally be generic if data is insufficient

---

## 🚫 9. Out-of-Scope Items (MVP)

The following features are **not included in the hackathon MVP** but may be added post-launch:

**OS-1**: WhatsApp integration for alerts and chat

**OS-2**: Voice input for chat queries (speech-to-text)

**OS-3**: Real-time POS integration (API-based data sync)

**OS-4**: Multi-store management (consolidated view across locations)

**OS-5**: Competitor price scraping and monitoring

**OS-6**: Advanced analytics (customer segmentation, cohort analysis)

**OS-7**: Mobile app (native iOS/Android)

**OS-8**: Supplier integration (automated purchase orders)

**OS-9**: Financial insights (profit/loss, cash flow forecasting)

**OS-10**: Marketplace integration (Amazon, Flipkart seller analytics)

---

## 🚀 10. Future Enhancements

### 10.1 WhatsApp Integration

- Send weekly reports via WhatsApp Business API
- Merchants can query Copilot via WhatsApp chat
- Alerts delivered as WhatsApp messages

### 10.2 Voice Input

- Merchants ask questions via voice (Hindi, Marathi, English)
- Use AWS Transcribe for speech-to-text
- LLM processes voice queries and responds in text/voice

### 10.3 Market Trend Retrieval

- Integrate external data sources (weather, festivals, local events)
- Enrich forecasts with macro trends (e.g., "Heatwave → Cold Drinks demand spike")

### 10.4 Multi-Store Support

- Merchants manage inventory across multiple locations
- Consolidated dashboard with store-level drill-down
- Transfer recommendations (move stock from Store A to Store B)

### 10.5 Supplier Integration

- Auto-generate purchase orders based on reorder recommendations
- Send POs to suppliers via email/API
- Track order status and delivery timelines

### 10.6 Financial Insights

- Profit/loss analysis per product
- Cash flow forecasting
- Working capital optimization

### 10.7 Advanced ML Models

- Deep learning models (LSTM, Transformer) for complex demand patterns
- Reinforcement learning for dynamic pricing
- Causal inference to understand "why" demand changed

---

## Appendix: Acceptance Criteria Summary

| Requirement ID | Acceptance Criteria | Priority |
|----------------|---------------------|----------|
| FR-1.1 | CSV upload with validation | P0 (Must-Have) |
| FR-1.2 | Data cleaning and quality report | P0 |
| FR-2.1 | 7-day and 30-day demand forecasts | P0 |
| FR-2.2 | Forecast explainability with LLM | P0 |
| FR-3.1 | Reorder quantity recommendations | P0 |
| FR-3.2 | Slow-moving product alerts | P1 (Should-Have) |
| FR-4.1 | Price optimization suggestions | P1 |
| FR-5.1 | Demand spike/drop detection | P1 |
| FR-5.2 | Seasonal trend insights | P2 (Nice-to-Have) |
| FR-6.1 | Conversational AI chat | P0 |
| FR-6.2 | Prompt safety and input validation | P0 |
| FR-7.1 | Multilingual outputs (EN, HI, MR) | P0 |
| FR-8.1 | Auto-generated weekly reports | P1 |
| FR-9.1 | Confidence scores for all outputs | P0 |
| FR-9.2 | Explainability for recommendations | P0 |
| FR-10.1 | Stockout risk alerts | P1 |
| FR-10.2 | Slow-moving product alerts | P1 |

**Priority Definitions**:
- **P0 (Must-Have)**: Critical for MVP, hackathon demo
- **P1 (Should-Have)**: Important but can be deferred post-hackathon
- **P2 (Nice-to-Have)**: Future enhancement

---

## Document Metadata

- **Version**: 1.0
- **Last Updated**: 2026-02-08
- **Author**: Bharat Brain Wave Team (Ritesh Raut, Lead)
- **Hackathon**: AWS AI for Bharat Hackathon
- **Theme**: AI for Retail, Commerce & Market Intelligence
- **Status**: Draft for Review

---

**End of Requirements Document**

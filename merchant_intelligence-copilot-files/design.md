# Design Document: Merchant Intelligence Copilot for Indian MSMEs

## Document Metadata

- **Version**: 1.0
- **Last Updated**: 2026-02-08
- **Author**: Bharat Brain Wave Team (Ritesh Raut, Lead)
- **Hackathon**: AWS AI for Bharat Hackathon
- **Theme**: AI for Retail, Commerce & Market Intelligence
- **Status**: Design Review

---

## 🏛️ 1. High-Level Architecture Overview

### 1.1 System Purpose

The Merchant Intelligence Copilot is an AI-powered decision support system that transforms raw sales data from Indian MSME merchants into actionable business intelligence. The system operates in three core stages:

**Stage 1: Data Ingestion & Validation**
- Merchants upload CSV files containing sales history (date, product, quantity, price, revenue)
- System validates, cleanses, and stores data in S3 and DynamoDB
- Data quality report generated and displayed to merchant

**Stage 2: AI-Powered Analysis**
- Time-series ML models (Prophet/ARIMA) generate demand forecasts for each product
- Anomaly detection identifies demand spikes, drops, and seasonal patterns
- Inventory optimization engine calculates reorder quantities and stockout risks
- Price optimization engine suggests pricing adjustments based on demand elasticity

**Stage 3: LLM-Powered Reasoning & Presentation**
- Amazon Bedrock (Claude 3) converts ML outputs into plain-language explanations
- Generates multilingual action plans (English, Hindi, Marathi)
- Powers conversational Copilot chat for merchant Q&A
- Creates weekly automated reports with prioritized recommendations


### 1.2 End-to-End User Journey

```
Merchant Journey:
1. Login via AWS Cognito (email/phone authentication)
2. Upload CSV file via web UI (React frontend hosted on S3/CloudFront)
3. System validates and processes data (Lambda + S3)
4. Dashboard displays:
   - Demand forecasts (7-day, 30-day) with confidence intervals
   - Reorder recommendations with quantities and urgency
   - Price optimization suggestions with revenue impact
   - Anomaly alerts (spikes, drops, slow movers)
   - Weekly action plan (LLM-generated summary)
5. Merchant interacts with Copilot Chat:
   - "Which products should I order this week?"
   - "Why is Product X selling less?"
   - LLM responds using merchant's data + ML insights
6. Merchant receives weekly email report (automated)
```

### 1.3 Key Design Principles

1. **Serverless-First**: Use AWS Lambda, API Gateway, DynamoDB (no EC2 instances) for cost efficiency and auto-scaling
2. **AI-Native**: ML forecasting + LLM reasoning at the core (not bolt-on features)
3. **Bharat-First**: CSV upload (no API integrations), multilingual, mobile-responsive, low-cost
4. **Responsible AI**: Confidence scores, explainability, disclaimers, human-in-the-loop
5. **Hackathon-Feasible**: Deployable in 48 hours using AWS SAM/CDK, single-region (ap-south-1)

---

## 🧱 2. Architecture Diagram (Textual Explanation)

### 2.1 Layered Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        UI LAYER (Frontend)                       │
│  React SPA (S3 + CloudFront) - Mobile-Responsive Dashboard      │
│  - CSV Upload Interface                                          │
│  - Forecast Dashboard (Charts, Tables)                           │
│  - Copilot Chat Interface                                        │
│  - Weekly Action Plan View                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                       API LAYER (Gateway)                        │
│  AWS API Gateway (REST API)                                      │
│  - /upload (POST) - CSV file upload                              │
│  - /forecast (GET) - Retrieve forecasts                          │
│  - /chat (POST) - Copilot Q&A                                    │
│  - /report (GET) - Weekly action plan                            │
│  - AWS Cognito Authorizer (JWT validation)                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    COMPUTE LAYER (Lambda)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Upload       │  │ Forecast     │  │ Chat         │          │
│  │ Handler      │  │ Generator    │  │ Handler      │          │
│  │ (Python)     │  │ (Python)     │  │ (Python)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Data         │  │ Report       │  │ Anomaly      │          │
│  │ Validator    │  │ Generator    │  │ Detector     │          │
│  │ (Python)     │  │ (Python)     │  │ (Python)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      AI/ML LAYER                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Amazon Bedrock (Claude 3 Haiku/Sonnet)                   │   │
│  │ - Forecast explanations                                  │   │
│  │ - Action plan generation                                 │   │
│  │ - Copilot chat responses                                 │   │
│  │ - Multilingual translation                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Time-Series Forecasting Engine (Python)                  │   │
│  │ - Prophet (Meta) for seasonal forecasting                │   │
│  │ - ARIMA for short-term predictions                       │   │
│  │ - Confidence interval calculation                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Anomaly Detection (Python)                               │   │
│  │ - Z-score based outlier detection                        │   │
│  │ - Week-over-week change detection                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA & STORAGE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Amazon S3    │  │ DynamoDB     │  │ ElastiCache  │          │
│  │ - Raw CSV    │  │ - User       │  │ (Redis)      │          │
│  │ - Processed  │  │   metadata   │  │ - LLM cache  │          │
│  │   data       │  │ - Forecasts  │  │ - Session    │          │
│  │ - Reports    │  │ - Config     │  │   data       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   MONITORING & LOGGING                           │
│  CloudWatch Logs, CloudWatch Metrics, X-Ray Tracing             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow Summary

1. **User uploads CSV** → API Gateway → Upload Lambda → S3 (raw) + DynamoDB (metadata)
2. **Data validation** → Validator Lambda → S3 (cleaned) + DynamoDB (quality report)
3. **Forecast generation** → Forecast Lambda → Prophet/ARIMA → DynamoDB (forecasts)
4. **LLM reasoning** → Bedrock API → Explanations + Action Plans → DynamoDB
5. **Dashboard retrieval** → API Gateway → Lambda → DynamoDB/S3 → Frontend
6. **Chat interaction** → API Gateway → Chat Lambda → Bedrock (RAG) → Response

---

## 🧩 3. Component-Level Design

### 3.1 Frontend (React SPA)

**Technology Stack**:
- React 18 with TypeScript
- Recharts for forecast visualizations
- Tailwind CSS for mobile-responsive UI
- Axios for API calls
- AWS Amplify for Cognito authentication

**Key Components**:

```
src/
├── components/
│   ├── Dashboard.tsx          # Main dashboard with forecast cards
│   ├── UploadCSV.tsx          # CSV upload interface with drag-drop
│   ├── ForecastChart.tsx      # Time-series chart with confidence bands
│   ├── CopilotChat.tsx        # Chat interface with message history
│   ├── ActionPlan.tsx         # Weekly report display
│   ├── AlertsPanel.tsx        # Stockout/anomaly alerts
│   └── LanguageSelector.tsx   # EN/HI/MR language switcher
├── services/
│   ├── api.ts                 # API Gateway client
│   └── auth.ts                # Cognito authentication
└── utils/
    ├── formatters.ts          # Number/date formatting
    └── validators.ts          # Client-side CSV validation
```

**Hosting**:
- Static files hosted on S3 bucket (e.g., `merchant-copilot-frontend`)
- CloudFront distribution for HTTPS and global CDN
- Custom domain (optional): `app.merchantcopilot.in`

**Authentication Flow**:
1. User logs in via Cognito Hosted UI (email/password or phone OTP)
2. Cognito returns JWT access token
3. Frontend stores token in localStorage
4. All API calls include `Authorization: Bearer <token>` header


### 3.2 API Gateway

**Configuration**:
- REST API (not HTTP API) for full feature support
- Regional endpoint (ap-south-1 Mumbai)
- Cognito User Pool Authorizer for authentication
- CORS enabled for frontend domain
- Request validation enabled (JSON schema validation)
- Throttling: 1000 requests/second per user (burst: 2000)

**API Endpoints**:

| Method | Path | Lambda Function | Purpose |
|--------|------|-----------------|---------|
| POST | /upload | UploadHandler | Upload CSV file (multipart/form-data) |
| GET | /data/quality | DataValidator | Retrieve data quality report |
| POST | /forecast/generate | ForecastGenerator | Trigger forecast generation |
| GET | /forecast/{product_id} | ForecastRetriever | Get forecast for specific product |
| GET | /forecast/all | ForecastRetriever | Get all forecasts for merchant |
| POST | /chat | ChatHandler | Send chat message to Copilot |
| GET | /report/weekly | ReportGenerator | Get weekly action plan |
| GET | /alerts | AlertsRetriever | Get active alerts (stockouts, anomalies) |
| POST | /feedback | FeedbackHandler | Submit feedback on recommendations |

**Request/Response Format**:
- All requests/responses use JSON (except CSV upload)
- Standard error format:
```json
{
  "error": "InvalidCSVFormat",
  "message": "Missing required column: product_name",
  "details": { "missing_columns": ["product_name"] }
}
```

### 3.3 AWS Lambda Functions

**3.3.1 Upload Handler Lambda**

**Purpose**: Process CSV file uploads and store in S3

**Runtime**: Python 3.11
**Memory**: 512 MB
**Timeout**: 60 seconds

**Logic**:
```python
def lambda_handler(event, context):
    # 1. Extract file from API Gateway multipart/form-data
    file_content = extract_file(event['body'])
    user_id = event['requestContext']['authorizer']['claims']['sub']
    
    # 2. Validate file size (<10MB) and format (.csv)
    if len(file_content) > 10 * 1024 * 1024:
        return error_response(400, "File too large")
    
    # 3. Generate unique file key
    file_key = f"uploads/{user_id}/{timestamp()}.csv"
    
    # 4. Upload to S3
    s3.put_object(Bucket='merchant-data', Key=file_key, Body=file_content)
    
    # 5. Store metadata in DynamoDB
    dynamodb.put_item(
        TableName='Uploads',
        Item={
            'user_id': user_id,
            'upload_id': generate_uuid(),
            'file_key': file_key,
            'status': 'uploaded',
            'timestamp': timestamp()
        }
    )
    
    # 6. Trigger DataValidator Lambda asynchronously
    lambda_client.invoke(
        FunctionName='DataValidator',
        InvocationType='Event',  # Async
        Payload=json.dumps({'file_key': file_key, 'user_id': user_id})
    )
    
    return success_response({'upload_id': upload_id, 'status': 'processing'})
```

**IAM Permissions**:
- `s3:PutObject` on `merchant-data` bucket
- `dynamodb:PutItem` on `Uploads` table
- `lambda:InvokeFunction` on `DataValidator` function

---

**3.3.2 Data Validator Lambda**

**Purpose**: Validate, clean, and preprocess CSV data

**Runtime**: Python 3.11
**Memory**: 1024 MB
**Timeout**: 120 seconds

**Logic**:
```python
import pandas as pd
import numpy as np

def lambda_handler(event, context):
    file_key = event['file_key']
    user_id = event['user_id']
    
    # 1. Download CSV from S3
    csv_content = s3.get_object(Bucket='merchant-data', Key=file_key)['Body'].read()
    df = pd.read_csv(io.BytesIO(csv_content))
    
    # 2. Validate required columns
    required_cols = ['date', 'product_name', 'quantity_sold', 'price', 'revenue']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        update_status(user_id, 'validation_failed', {'missing_columns': missing_cols})
        return
    
    # 3. Data cleaning
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['product_name'] = df['product_name'].str.strip().str.lower()
    df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    
    # 4. Handle missing values
    df = df.dropna(subset=['date', 'product_name'])  # Drop if critical fields missing
    df['quantity_sold'].fillna(0, inplace=True)
    df['price'].fillna(df['price'].median(), inplace=True)
    
    # 5. Outlier detection (Z-score > 3)
    df['quantity_zscore'] = np.abs((df['quantity_sold'] - df['quantity_sold'].mean()) / df['quantity_sold'].std())
    outliers = df[df['quantity_zscore'] > 3]
    
    # 6. Generate data quality report
    quality_report = {
        'total_rows': len(df),
        'date_range': {'start': df['date'].min().isoformat(), 'end': df['date'].max().isoformat()},
        'unique_products': df['product_name'].nunique(),
        'missing_values': df.isnull().sum().to_dict(),
        'outliers_detected': len(outliers),
        'completeness_score': (1 - df.isnull().sum().sum() / df.size) * 100
    }
    
    # 7. Save cleaned data to S3
    cleaned_key = file_key.replace('uploads/', 'cleaned/')
    df.to_csv(f's3://merchant-data/{cleaned_key}', index=False)
    
    # 8. Store quality report in DynamoDB
    dynamodb.put_item(
        TableName='DataQuality',
        Item={'user_id': user_id, 'report': quality_report, 'timestamp': timestamp()}
    )
    
    # 9. Trigger ForecastGenerator Lambda
    lambda_client.invoke(
        FunctionName='ForecastGenerator',
        InvocationType='Event',
        Payload=json.dumps({'file_key': cleaned_key, 'user_id': user_id})
    )
    
    return success_response(quality_report)
```

**Dependencies**:
- pandas, numpy (packaged in Lambda Layer)

---

**3.3.3 Forecast Generator Lambda**

**Purpose**: Generate demand forecasts using time-series ML models

**Runtime**: Python 3.11
**Memory**: 2048 MB (ML models require more memory)
**Timeout**: 300 seconds (5 minutes)

**Logic**:
```python
from prophet import Prophet
import pandas as pd

def lambda_handler(event, context):
    file_key = event['file_key']
    user_id = event['user_id']
    
    # 1. Load cleaned data from S3
    df = pd.read_csv(f's3://merchant-data/{file_key}')
    
    # 2. Group by product and date (aggregate daily sales)
    df_grouped = df.groupby(['product_name', 'date']).agg({
        'quantity_sold': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    # 3. Generate forecasts for each product
    forecasts = []
    for product in df_grouped['product_name'].unique():
        product_data = df_grouped[df_grouped['product_name'] == product]
        
        # Skip if insufficient data (<30 days)
        if len(product_data) < 30:
            continue
        
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = product_data[['date', 'quantity_sold']].rename(columns={'date': 'ds', 'quantity_sold': 'y'})
        
        # Train Prophet model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,  # Not enough data for yearly
            interval_width=0.8  # 80% confidence interval
        )
        model.fit(prophet_df)
        
        # Generate 7-day and 30-day forecasts
        future = model.make_future_dataframe(periods=30, freq='D')
        forecast = model.predict(future)
        
        # Extract forecast for next 7 and 30 days
        forecast_7d = forecast.tail(7)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
        forecast_30d = forecast.tail(30)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
        
        # Calculate confidence score (based on prediction interval width)
        avg_interval_width = (forecast['yhat_upper'] - forecast['yhat_lower']).mean()
        avg_prediction = forecast['yhat'].mean()
        confidence_score = max(0, min(100, 100 - (avg_interval_width / avg_prediction * 100)))
        
        forecasts.append({
            'product_name': product,
            'forecast_7d': forecast_7d,
            'forecast_30d': forecast_30d,
            'confidence_score': round(confidence_score, 2),
            'model': 'Prophet'
        })
    
    # 4. Store forecasts in DynamoDB
    for forecast in forecasts:
        dynamodb.put_item(
            TableName='Forecasts',
            Item={
                'user_id': user_id,
                'product_name': forecast['product_name'],
                'forecast_data': forecast,
                'timestamp': timestamp(),
                'ttl': timestamp() + 7 * 24 * 3600  # Expire after 7 days
            }
        )
    
    # 5. Trigger AnomalyDetector and ReportGenerator Lambdas
    lambda_client.invoke(FunctionName='AnomalyDetector', InvocationType='Event', Payload=json.dumps({'user_id': user_id}))
    lambda_client.invoke(FunctionName='ReportGenerator', InvocationType='Event', Payload=json.dumps({'user_id': user_id}))
    
    return success_response({'forecasts_generated': len(forecasts)})
```

**Dependencies**:
- prophet, pandas, numpy (Lambda Layer)


**3.3.4 Anomaly Detector Lambda**

**Purpose**: Detect demand spikes, drops, and slow-moving products

**Runtime**: Python 3.11
**Memory**: 1024 MB
**Timeout**: 120 seconds

**Logic**:
```python
def lambda_handler(event, context):
    user_id = event['user_id']
    
    # 1. Retrieve forecasts from DynamoDB
    forecasts = dynamodb.query(TableName='Forecasts', KeyConditionExpression='user_id = :uid', ExpressionAttributeValues={':uid': user_id})
    
    # 2. Load historical data from S3
    df = load_cleaned_data(user_id)
    
    # 3. Detect anomalies for each product
    anomalies = []
    for forecast in forecasts:
        product = forecast['product_name']
        product_data = df[df['product_name'] == product]
        
        # Calculate week-over-week change
        last_week_sales = product_data.tail(7)['quantity_sold'].sum()
        prev_week_sales = product_data.iloc[-14:-7]['quantity_sold'].sum()
        wow_change = ((last_week_sales - prev_week_sales) / prev_week_sales * 100) if prev_week_sales > 0 else 0
        
        # Detect spike (>30% increase)
        if wow_change > 30:
            anomalies.append({
                'product_name': product,
                'type': 'spike',
                'change_percent': round(wow_change, 2),
                'severity': 'high' if wow_change > 50 else 'medium'
            })
        
        # Detect drop (>30% decrease)
        elif wow_change < -30:
            anomalies.append({
                'product_name': product,
                'type': 'drop',
                'change_percent': round(wow_change, 2),
                'severity': 'high' if wow_change < -50 else 'medium'
            })
        
        # Detect slow-moving (<50% of average velocity)
        avg_velocity = product_data['quantity_sold'].mean()
        if last_week_sales < 0.5 * avg_velocity * 7:
            anomalies.append({
                'product_name': product,
                'type': 'slow_moving',
                'current_velocity': round(last_week_sales / 7, 2),
                'avg_velocity': round(avg_velocity, 2),
                'severity': 'medium'
            })
    
    # 4. Store anomalies in DynamoDB
    dynamodb.put_item(
        TableName='Anomalies',
        Item={'user_id': user_id, 'anomalies': anomalies, 'timestamp': timestamp()}
    )
    
    return success_response({'anomalies_detected': len(anomalies)})
```

---

**3.3.5 Chat Handler Lambda**

**Purpose**: Process Copilot chat queries using Amazon Bedrock

**Runtime**: Python 3.11
**Memory**: 512 MB
**Timeout**: 30 seconds

**Logic**:
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='ap-south-1')

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['sub']
    user_message = json.loads(event['body'])['message']
    language = json.loads(event['body']).get('language', 'en')  # en, hi, mr
    
    # 1. Retrieve merchant context (forecasts, anomalies, recent data)
    context = build_merchant_context(user_id)
    
    # 2. Build prompt for Bedrock
    system_prompt = f"""You are a helpful business advisor for Indian MSME merchants. 
You have access to the merchant's sales data, demand forecasts, and inventory insights.
Respond in {language} language.
Be concise, actionable, and explain your reasoning.
Always include confidence levels when making recommendations.
If you don't have enough data, say so clearly."""

    user_prompt = f"""Merchant Context:
- Products: {context['products']}
- Recent Forecasts: {context['forecasts']}
- Anomalies: {context['anomalies']}

Merchant Question: {user_message}

Provide a helpful, data-driven answer."""

    # 3. Call Bedrock (Claude 3 Haiku for cost efficiency)
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 500,
            'system': system_prompt,
            'messages': [{'role': 'user', 'content': user_prompt}],
            'temperature': 0.3  # Lower temperature for factual responses
        })
    )
    
    # 4. Parse response
    response_body = json.loads(response['body'].read())
    assistant_message = response_body['content'][0]['text']
    
    # 5. Calculate confidence score (based on data availability)
    confidence_score = calculate_confidence(context, user_message)
    
    # 6. Store chat history in DynamoDB
    dynamodb.put_item(
        TableName='ChatHistory',
        Item={
            'user_id': user_id,
            'timestamp': timestamp(),
            'user_message': user_message,
            'assistant_message': assistant_message,
            'confidence_score': confidence_score
        }
    )
    
    # 7. Return response with disclaimer
    return success_response({
        'message': assistant_message,
        'confidence_score': confidence_score,
        'disclaimer': 'AI-generated advice. Verify before acting.'
    })

def build_merchant_context(user_id):
    # Retrieve forecasts, anomalies, and recent sales data
    forecasts = dynamodb.query(TableName='Forecasts', KeyConditionExpression='user_id = :uid', ExpressionAttributeValues={':uid': user_id})
    anomalies = dynamodb.get_item(TableName='Anomalies', Key={'user_id': user_id})
    
    return {
        'products': [f['product_name'] for f in forecasts],
        'forecasts': forecasts[:5],  # Top 5 for context window
        'anomalies': anomalies.get('anomalies', [])
    }

def calculate_confidence(context, query):
    # Simple heuristic: confidence based on data availability
    if len(context['forecasts']) > 10:
        return 85
    elif len(context['forecasts']) > 5:
        return 70
    else:
        return 50
```

**Cost Optimization**:
- Use Claude 3 Haiku (cheapest model) for chat
- Cache frequent queries in ElastiCache (Redis)
- Limit context window to top 5 products (reduce tokens)

---

**3.3.6 Report Generator Lambda**

**Purpose**: Generate weekly action plans using LLM

**Runtime**: Python 3.11
**Memory**: 512 MB
**Timeout**: 60 seconds

**Logic**:
```python
def lambda_handler(event, context):
    user_id = event['user_id']
    language = event.get('language', 'en')
    
    # 1. Retrieve all insights (forecasts, anomalies, inventory recommendations)
    forecasts = dynamodb.query(TableName='Forecasts', KeyConditionExpression='user_id = :uid', ExpressionAttributeValues={':uid': user_id})
    anomalies = dynamodb.get_item(TableName='Anomalies', Key={'user_id': user_id}).get('anomalies', [])
    
    # 2. Calculate inventory recommendations
    reorder_recommendations = []
    for forecast in forecasts:
        product = forecast['product_name']
        forecast_7d = forecast['forecast_data']['forecast_7d']
        predicted_demand = sum([day['yhat'] for day in forecast_7d])
        
        # Assume current stock = 0 (merchant needs to input this in future)
        # For MVP, recommend ordering forecasted demand + 20% safety stock
        reorder_qty = predicted_demand * 1.2
        
        reorder_recommendations.append({
            'product_name': product,
            'reorder_quantity': round(reorder_qty, 2),
            'urgency': 'high' if reorder_qty > 100 else 'medium'
        })
    
    # 3. Build prompt for LLM
    prompt = f"""Generate a weekly action plan for an MSME merchant in {language} language.

Data Summary:
- Total Products: {len(forecasts)}
- Anomalies Detected: {len(anomalies)}
- Reorder Recommendations: {len(reorder_recommendations)}

Top 5 Products to Reorder:
{json.dumps(reorder_recommendations[:5], indent=2)}

Anomalies:
{json.dumps(anomalies, indent=2)}

Generate a concise, actionable weekly plan with:
1. Top 3 priorities (reorder, pricing, alerts)
2. Explanation for each priority
3. Expected business impact

Format as a structured report."""

    # 4. Call Bedrock (Claude 3 Sonnet for better reasoning)
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 1000,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.5
        })
    )
    
    report = json.loads(response['body'].read())['content'][0]['text']
    
    # 5. Store report in DynamoDB
    dynamodb.put_item(
        TableName='WeeklyReports',
        Item={
            'user_id': user_id,
            'report': report,
            'timestamp': timestamp(),
            'language': language
        }
    )
    
    # 6. Send email via SES (optional)
    # ses.send_email(...)
    
    return success_response({'report': report})
```


### 3.4 Amazon S3 (Storage)

**Bucket Structure**:

```
merchant-data/
├── uploads/
│   └── {user_id}/
│       └── {timestamp}.csv          # Raw uploaded CSV files
├── cleaned/
│   └── {user_id}/
│       └── {timestamp}_cleaned.csv  # Validated and cleaned data
├── reports/
│   └── {user_id}/
│       └── weekly_{date}.pdf        # Generated reports (future)
└── models/
    └── {user_id}/
        └── {product_name}_model.pkl # Trained Prophet models (optional caching)
```

**Bucket Configuration**:
- **Encryption**: SSE-S3 (server-side encryption)
- **Versioning**: Enabled (for data recovery)
- **Lifecycle Policy**: 
  - Move `uploads/` to Glacier after 30 days
  - Delete `cleaned/` after 90 days
- **Access Control**: Private (IAM-based access only)
- **CORS**: Enabled for frontend domain

**Cost Optimization**:
- Use S3 Intelligent-Tiering for automatic cost optimization
- Compress CSV files before storage (gzip)

---

### 3.5 DynamoDB (Metadata & Configurations)

**Table Design**:

**Table 1: Users**
- **Partition Key**: `user_id` (String)
- **Attributes**: `email`, `phone`, `language_preference`, `created_at`, `subscription_tier`
- **Purpose**: Store user profile and preferences

**Table 2: Uploads**
- **Partition Key**: `user_id` (String)
- **Sort Key**: `upload_id` (String)
- **Attributes**: `file_key`, `status`, `timestamp`, `data_quality_score`
- **Purpose**: Track CSV upload history and processing status

**Table 3: Forecasts**
- **Partition Key**: `user_id` (String)
- **Sort Key**: `product_name` (String)
- **Attributes**: `forecast_data` (Map), `confidence_score`, `timestamp`, `ttl`
- **Purpose**: Store demand forecasts per product
- **TTL**: Enabled (auto-delete after 7 days)

**Table 4: Anomalies**
- **Partition Key**: `user_id` (String)
- **Attributes**: `anomalies` (List), `timestamp`
- **Purpose**: Store detected anomalies (spikes, drops, slow movers)

**Table 5: ChatHistory**
- **Partition Key**: `user_id` (String)
- **Sort Key**: `timestamp` (Number)
- **Attributes**: `user_message`, `assistant_message`, `confidence_score`
- **Purpose**: Store chat conversation history

**Table 6: WeeklyReports**
- **Partition Key**: `user_id` (String)
- **Sort Key**: `timestamp` (Number)
- **Attributes**: `report` (String), `language`
- **Purpose**: Store generated weekly action plans

**Table 7: Feedback**
- **Partition Key**: `user_id` (String)
- **Sort Key**: `feedback_id` (String)
- **Attributes**: `recommendation_type`, `rating`, `comment`, `timestamp`
- **Purpose**: Collect user feedback for model improvement

**Capacity Mode**: On-Demand (pay-per-request, auto-scaling)

**Cost Optimization**:
- Use TTL to auto-delete old forecasts
- Use sparse indexes for infrequent queries
- Batch write operations where possible

---

### 3.6 Amazon Bedrock (LLM Reasoning)

**Model Selection**:

| Use Case | Model | Justification |
|----------|-------|---------------|
| Chat responses | Claude 3 Haiku | Fastest, cheapest, sufficient for Q&A |
| Weekly reports | Claude 3 Sonnet | Better reasoning for complex summaries |
| Multilingual translation | Claude 3 Haiku | Supports Hindi, Marathi natively |
| Forecast explanations | Claude 3 Haiku | Simple explanations, low token count |

**Prompt Engineering Strategy**:

**1. System Prompt Template**:
```
You are a business advisor for Indian MSME merchants.
You have access to their sales data, demand forecasts, and inventory insights.
Your role is to provide actionable, data-driven recommendations.

Guidelines:
- Be concise and specific
- Always explain your reasoning
- Include confidence levels (High/Medium/Low)
- Use simple language (avoid jargon)
- Respond in {language} language
- If data is insufficient, say so clearly
- Never make up numbers or facts
```

**2. User Prompt Template (RAG Pattern)**:
```
Merchant Context:
- Business Type: {business_type}
- Products: {product_list}
- Recent Sales Trends: {trends_summary}
- Demand Forecasts: {forecast_summary}
- Anomalies: {anomaly_summary}

Merchant Question: {user_query}

Provide a helpful answer based on the data above.
```

**3. Guardrails**:
- **Input Validation**: Reject queries unrelated to merchant data
- **Output Filtering**: Remove any hallucinated product names not in merchant's data
- **Confidence Scoring**: Append confidence score based on data availability

**Cost Optimization**:
- **Caching**: Cache frequent queries (e.g., "What should I order this week?") in Redis
- **Token Limits**: Set max_tokens=500 for chat, 1000 for reports
- **Model Selection**: Use Haiku (cheapest) by default, Sonnet only for complex tasks
- **Batch Processing**: Generate all weekly reports in a single Lambda invocation

**Estimated Bedrock Costs** (per merchant/month):
- Chat queries: 50 queries × 1000 tokens × $0.00025/1K tokens = $0.0125
- Weekly reports: 4 reports × 2000 tokens × $0.00025/1K tokens = $0.002
- **Total**: ~$0.015/merchant/month (~₹1.25)

---

### 3.7 ElastiCache (Redis) - Optional for MVP

**Purpose**: Cache LLM responses and session data

**Configuration**:
- **Node Type**: cache.t3.micro (0.5 GB memory)
- **Cluster Mode**: Disabled (single node for MVP)
- **Encryption**: In-transit and at-rest

**Caching Strategy**:
- **LLM Responses**: Cache by query hash (TTL: 1 hour)
- **Forecasts**: Cache frequently accessed forecasts (TTL: 24 hours)
- **Session Data**: Store user session tokens (TTL: 30 minutes)

**Cost**: ~$15/month (can be skipped for MVP if budget is tight)

---

## 🔄 4. Data Flow (Step-by-Step)

### 4.1 CSV Upload Flow

```
1. Merchant uploads CSV via React UI
   ↓
2. Frontend sends POST /upload to API Gateway (multipart/form-data)
   ↓
3. API Gateway validates JWT token (Cognito Authorizer)
   ↓
4. UploadHandler Lambda receives file
   ↓
5. Lambda uploads file to S3: uploads/{user_id}/{timestamp}.csv
   ↓
6. Lambda stores metadata in DynamoDB: Uploads table
   ↓
7. Lambda triggers DataValidator Lambda (async)
   ↓
8. Frontend receives response: {"upload_id": "...", "status": "processing"}
   ↓
9. Frontend polls GET /data/quality every 5 seconds to check status
```

### 4.2 Data Validation Flow

```
1. DataValidator Lambda triggered by UploadHandler
   ↓
2. Lambda downloads CSV from S3
   ↓
3. Validates columns (date, product_name, quantity_sold, price, revenue)
   ↓
4. Cleans data:
   - Convert dates to standard format
   - Normalize product names (lowercase, trim)
   - Handle missing values (forward-fill, median)
   - Detect outliers (Z-score > 3)
   ↓
5. Generates data quality report:
   - Total rows, date range, unique products
   - Missing values, outliers detected
   - Completeness score (0-100%)
   ↓
6. Saves cleaned data to S3: cleaned/{user_id}/{timestamp}_cleaned.csv
   ↓
7. Stores quality report in DynamoDB: DataQuality table
   ↓
8. Updates upload status in DynamoDB: Uploads table (status = "validated")
   ↓
9. Triggers ForecastGenerator Lambda (async)
```

### 4.3 Forecast Generation Flow

```
1. ForecastGenerator Lambda triggered by DataValidator
   ↓
2. Lambda loads cleaned data from S3
   ↓
3. Groups data by product and date (daily aggregation)
   ↓
4. For each product:
   a. Check if sufficient data (≥30 days)
   b. Prepare data for Prophet (ds, y columns)
   c. Train Prophet model (daily + weekly seasonality)
   d. Generate 7-day and 30-day forecasts
   e. Calculate confidence score (based on prediction interval width)
   ↓
5. Stores forecasts in DynamoDB: Forecasts table
   - Partition Key: user_id
   - Sort Key: product_name
   - Attributes: forecast_7d, forecast_30d, confidence_score
   ↓
6. Triggers AnomalyDetector Lambda (async)
   ↓
7. Triggers ReportGenerator Lambda (async)
```

### 4.4 Anomaly Detection Flow

```
1. AnomalyDetector Lambda triggered by ForecastGenerator
   ↓
2. Lambda retrieves forecasts from DynamoDB
   ↓
3. Lambda loads historical data from S3
   ↓
4. For each product:
   a. Calculate week-over-week change
   b. Detect spike (>30% increase)
   c. Detect drop (>30% decrease)
   d. Detect slow-moving (<50% of average velocity)
   ↓
5. Stores anomalies in DynamoDB: Anomalies table
   ↓
6. Frontend displays alerts on dashboard
```

### 4.5 LLM Reasoning Flow (Chat)

```
1. Merchant types question in Copilot Chat: "Which products should I order?"
   ↓
2. Frontend sends POST /chat to API Gateway
   ↓
3. ChatHandler Lambda receives query
   ↓
4. Lambda retrieves merchant context from DynamoDB:
   - Forecasts (top 5 products)
   - Anomalies (recent alerts)
   - Recent sales data
   ↓
5. Lambda builds prompt for Bedrock:
   - System prompt: "You are a business advisor..."
   - User prompt: "Merchant Context: ... Question: ..."
   ↓
6. Lambda calls Bedrock (Claude 3 Haiku)
   ↓
7. Bedrock generates response (max 500 tokens)
   ↓
8. Lambda calculates confidence score (based on data availability)
   ↓
9. Lambda stores chat history in DynamoDB: ChatHistory table
   ↓
10. Lambda returns response to frontend:
    {
      "message": "Based on your forecasts, order 50 kg Atta...",
      "confidence_score": 85,
      "disclaimer": "AI-generated advice. Verify before acting."
    }
   ↓
11. Frontend displays response in chat interface
```

### 4.6 Weekly Report Generation Flow

```
1. EventBridge rule triggers ReportGenerator Lambda every Monday 8 AM
   ↓
2. Lambda retrieves all users from DynamoDB: Users table
   ↓
3. For each user:
   a. Retrieve forecasts, anomalies, inventory recommendations
   b. Build prompt for Bedrock (Claude 3 Sonnet)
   c. Generate weekly action plan (top 3 priorities)
   d. Store report in DynamoDB: WeeklyReports table
   e. Send email via SES (optional)
   ↓
4. Merchant logs in and sees new report on dashboard
```

---

## 🤖 5. AI Design Details (VERY IMPORTANT)

### 5.1 Why Forecasting is Required

**Problem**: MSME merchants face unpredictable demand patterns due to:
- Seasonal variations (festivals, weather, holidays)
- Event-driven spikes (local events, promotions)
- Supply chain disruptions
- Competitor actions

**Why Rule-Based Systems Fail**:
- Cannot capture non-linear relationships (e.g., temperature → cold drinks demand)
- Cannot learn from historical patterns
- Require manual tuning for each product

**Why ML Forecasting is Essential**:
- **Prophet (Meta)**: Designed for business time-series with seasonality, holidays, and missing data
- **ARIMA**: Captures short-term trends and autocorrelation
- **Confidence Intervals**: Quantify prediction uncertainty (critical for inventory decisions)
- **Automatic Seasonality Detection**: Learns weekly/monthly patterns without manual input

**Hackathon Justification**:
- Forecasting is the **core AI capability** that enables all downstream recommendations
- Without forecasts, the system is just a data visualization tool (not AI-powered)


### 5.2 Why LLM Reasoning is Required

**Problem**: ML forecasts are just numbers. MSME merchants need:
- Plain-language explanations ("Why is demand increasing?")
- Actionable recommendations ("Order 50 kg Atta by Friday")
- Multilingual support (Hindi, Marathi)
- Conversational interface (chat, not dashboards)

**Why LLMs are Essential**:
1. **Natural Language Generation**: Convert forecasts into human-readable insights
2. **Contextual Reasoning**: Explain "why" demand is changing (seasonality, trends, anomalies)
3. **Multilingual Support**: Claude 3 natively supports Hindi, Marathi
4. **Conversational AI**: Enable low-tech merchants to ask questions in natural language
5. **Automated Report Generation**: Create weekly action plans without manual analysis

**Example Transformation**:

**Without LLM** (raw forecast):
```
Product: Atta 1kg
Forecast (7-day): [45, 48, 52, 55, 60, 65, 70]
Confidence: 82%
```

**With LLM** (actionable insight):
```
📈 Atta 1kg Demand Forecast (Next 7 Days)
Expected Sales: 395 kg (up 25% from last week)

Why? Demand is increasing due to:
- Upcoming festival season (Diwali in 2 weeks)
- Weekly seasonality (higher sales on weekends)

Action: Order 475 kg by Friday (395 kg forecast + 20% safety stock)
Confidence: High (82%)

⚠️ Risk: If you don't order now, you may face stockouts during peak demand.
```

**Hackathon Justification**:
- LLMs enable **Bharat-first design** (low-tech onboarding via chat)
- Demonstrates **meaningful AI use** (not just dashboards)
- Aligns with **Responsible AI** (explainability, confidence scoring)

---

### 5.3 Prompt Design Principles

**Principle 1: Grounding in Data (RAG Pattern)**
- Always include merchant's actual data in the prompt
- Never let LLM hallucinate product names or numbers
- Use structured context (JSON format) for clarity

**Principle 2: Clear Instructions**
- Specify output format (concise, actionable, multilingual)
- Set constraints (max 500 tokens, no jargon)
- Define role ("You are a business advisor for MSME merchants")

**Principle 3: Confidence Calibration**
- Instruct LLM to indicate uncertainty ("Based on limited data...")
- Append confidence scores calculated from data availability
- Add disclaimers ("AI-generated advice. Verify before acting.")

**Principle 4: Multilingual Support**
- Specify language in system prompt ("Respond in Hindi")
- Use native language examples in few-shot prompts
- Validate output language matches request

**Example Prompt Template**:

```python
system_prompt = f"""You are a helpful business advisor for Indian MSME merchants.
You have access to their sales data, demand forecasts, and inventory insights.

Guidelines:
- Be concise and actionable (max 3 sentences)
- Always explain your reasoning
- Use simple language (avoid technical jargon)
- Respond in {language} language (en/hi/mr)
- If data is insufficient, say "I need more data to answer this"
- Never make up product names or numbers

Format:
1. Direct answer
2. Reasoning (why?)
3. Confidence level (High/Medium/Low)
"""

user_prompt = f"""Merchant Context:
Products: {json.dumps(product_list)}
Recent Forecasts: {json.dumps(forecast_summary)}
Anomalies: {json.dumps(anomaly_summary)}

Question: {user_query}

Answer:"""
```

---

### 5.4 Explainability Strategy

**Goal**: Every AI recommendation must include "why" and "how confident"

**Implementation**:

**1. Forecast Explainability**:
- Display forecast chart with historical data + prediction + confidence bands
- LLM generates explanation:
  - "Demand is increasing due to weekly seasonality (higher sales on weekends)"
  - "Forecast confidence is high (85%) because we have 90 days of historical data"

**2. Anomaly Explainability**:
- Detect spike/drop using statistical methods (Z-score, week-over-week change)
- LLM generates possible causes:
  - "Spike in Cold Drinks likely due to recent heatwave"
  - "Drop in Umbrellas likely due to end of monsoon season"

**3. Inventory Recommendation Explainability**:
- Show calculation: `Reorder Qty = Forecasted Demand (7 days) + Safety Stock (20%)`
- LLM explains urgency:
  - "Order now (High urgency) because current stock will run out in 3 days"

**4. Price Optimization Explainability**:
- Show price elasticity calculation from historical data
- LLM explains impact:
  - "Increase price by ₹5 → Expected revenue +8% (demand is inelastic)"

**UI Design**:
- Every recommendation card has "Why?" button that expands explanation
- Confidence score displayed as color-coded badge (Green: >80%, Yellow: 60-80%, Red: <60%)

---

### 5.5 Confidence Scoring Mechanism

**Goal**: Quantify prediction uncertainty to help merchants make informed decisions

**Confidence Score Calculation**:

**1. Forecast Confidence**:
```python
# Based on prediction interval width (Prophet output)
avg_interval_width = (forecast['yhat_upper'] - forecast['yhat_lower']).mean()
avg_prediction = forecast['yhat'].mean()
confidence_score = max(0, min(100, 100 - (avg_interval_width / avg_prediction * 100)))
```

**Interpretation**:
- Narrow prediction interval → High confidence (model is certain)
- Wide prediction interval → Low confidence (high uncertainty)

**2. Data Availability Confidence**:
```python
# Based on historical data quantity
if days_of_data >= 90:
    data_confidence = 90
elif days_of_data >= 60:
    data_confidence = 75
elif days_of_data >= 30:
    data_confidence = 60
else:
    data_confidence = 40
```

**3. Combined Confidence**:
```python
final_confidence = (forecast_confidence * 0.7) + (data_confidence * 0.3)
```

**4. Chat Response Confidence**:
```python
# Based on data availability for answering query
if query_answerable_with_data:
    confidence = 85
elif query_partially_answerable:
    confidence = 65
else:
    confidence = 40  # LLM will say "I need more data"
```

**Display Strategy**:
- **High (>80%)**: Green badge, "Highly confident"
- **Medium (60-80%)**: Yellow badge, "Moderately confident"
- **Low (<60%)**: Red badge, "Low confidence - verify manually"

---

## 🌐 6. Multilingual Design

### 6.1 Language Support Strategy

**Supported Languages**:
- English (en) - Default
- Hindi (hi) - Primary vernacular
- Marathi (mr) - Regional language

**Implementation Approach**:

**Option 1: Native LLM Multilingual Support (Recommended for MVP)**
- Claude 3 natively supports Hindi and Marathi
- Simply specify language in system prompt: "Respond in Hindi"
- No additional translation service required
- **Pros**: Simple, cost-effective, maintains context
- **Cons**: Quality depends on LLM training data

**Option 2: AWS Translate (Fallback)**
- Generate response in English first
- Translate using AWS Translate API
- **Pros**: Consistent translation quality
- **Cons**: Additional cost, potential context loss

**MVP Decision**: Use Option 1 (native LLM support) for hackathon

### 6.2 Language Selection Flow

```
1. User selects language in UI (dropdown: EN/HI/MR)
   ↓
2. Frontend stores preference in localStorage
   ↓
3. All API calls include language parameter: {"language": "hi"}
   ↓
4. Lambda functions pass language to Bedrock prompts
   ↓
5. LLM generates response in requested language
   ↓
6. Frontend displays response (no additional processing needed)
```

### 6.3 Language Fallback Logic

```python
def get_llm_response(user_query, language, context):
    # Try to generate response in requested language
    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'system': f"Respond in {language} language",
                'messages': [{'role': 'user', 'content': user_query}]
            })
        )
        return response
    except Exception as e:
        # Fallback to English if language not supported
        logger.warning(f"Language {language} failed, falling back to English")
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'system': "Respond in English",
                'messages': [{'role': 'user', 'content': user_query}]
            })
        )
        return response
```

### 6.4 UI Localization

**Static Text Translation**:
- Use i18n library (react-i18next) for UI labels
- Translation files:
  - `locales/en.json`: English labels
  - `locales/hi.json`: Hindi labels
  - `locales/mr.json`: Marathi labels

**Example**:
```json
// locales/hi.json
{
  "dashboard.title": "डैशबोर्ड",
  "upload.button": "CSV अपलोड करें",
  "forecast.title": "मांग पूर्वानुमान",
  "chat.placeholder": "अपना सवाल पूछें..."
}
```

**Dynamic Content Translation**:
- All LLM-generated content (forecasts, recommendations, chat) translated by LLM
- No need for separate translation service

---

## 🛡️ 7. Responsible AI Design

### 7.1 Safety Filters

**Input Validation**:
```python
def validate_chat_input(user_message):
    # 1. Check for prompt injection patterns
    injection_patterns = [
        r"ignore previous instructions",
        r"disregard all",
        r"system prompt",
        r"<script>",
        r"DROP TABLE",
        r"'; DELETE FROM"
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, user_message, re.IGNORECASE):
            return False, "Invalid input detected"
    
    # 2. Check message length (max 500 characters)
    if len(user_message) > 500:
        return False, "Message too long"
    
    # 3. Check for off-topic queries
    business_keywords = ['product', 'sales', 'order', 'stock', 'price', 'demand', 'forecast']
    if not any(keyword in user_message.lower() for keyword in business_keywords):
        return False, "Query must be related to your business data"
    
    return True, "Valid"
```

**Output Filtering**:
```python
def validate_llm_output(llm_response, merchant_products):
    # 1. Check if LLM hallucinated product names
    mentioned_products = extract_product_names(llm_response)
    for product in mentioned_products:
        if product not in merchant_products:
            logger.warning(f"LLM hallucinated product: {product}")
            # Remove hallucinated product from response
            llm_response = llm_response.replace(product, "[Unknown Product]")
    
    # 2. Check for unsafe content (Bedrock Guardrails)
    # AWS Bedrock has built-in content filtering
    
    return llm_response
```

### 7.2 Hallucination Reduction

**Strategy 1: Grounding in Data (RAG)**
- Always include merchant's actual data in prompt
- Instruct LLM: "Only use data provided in context. Never make up product names or numbers."

**Strategy 2: Structured Output**
- Request JSON output for structured data (forecasts, recommendations)
- Validate JSON schema before displaying to user

**Strategy 3: Confidence Thresholds**
- If LLM confidence < 60%, display warning: "Low confidence - verify manually"
- For critical actions (e.g., large orders), require human confirmation

**Strategy 4: Human-in-the-Loop**
- Merchants can provide feedback (thumbs up/down) on recommendations
- Low-rated responses flagged for admin review
- Feedback used to improve prompts and fine-tune models (future)

### 7.3 Disclaimers

**Display Locations**:

**1. Dashboard Header**:
```
⚠️ AI-generated recommendations. Verify before acting.
```

**2. Chat Interface**:
```
💬 Copilot Chat
This is an AI assistant. Recommendations are based on your data but may not be perfect.
Always use your business judgment.
```

**3. Weekly Report**:
```
📊 Weekly Action Plan (AI-Generated)
This report is automatically generated using AI. Review carefully and adjust based on your business knowledge.
```

**4. API Responses**:
```json
{
  "message": "Order 50 kg Atta by Friday",
  "confidence_score": 85,
  "disclaimer": "AI-generated advice. Verify before acting."
}
```

### 7.4 Human Oversight

**Admin Dashboard** (for hackathon team):
- View all LLM responses flagged as low-confidence (<60%)
- Review user feedback (thumbs down ratings)
- Monitor anomaly detection false positives
- Adjust prompt templates based on feedback

**Merchant Feedback Loop**:
- Every recommendation has thumbs up/down button
- Feedback stored in DynamoDB: Feedback table
- Weekly review of low-rated recommendations

**Escalation Path**:
- If merchant reports incorrect recommendation, admin investigates
- Root cause analysis: data quality issue, model error, or prompt issue
- Corrective action: update prompt, retrain model, or improve data validation

---

## 💰 8. Cost Optimization Strategy

### 8.1 Bedrock Cost Control

**Cost Breakdown** (per merchant/month):

| Component | Usage | Cost |
|-----------|-------|------|
| Chat queries | 50 queries × 1000 tokens × $0.00025/1K | $0.0125 |
| Weekly reports | 4 reports × 2000 tokens × $0.00025/1K | $0.002 |
| Forecast explanations | 20 products × 500 tokens × $0.00025/1K | $0.0025 |
| **Total Bedrock** | | **$0.017/month (~₹1.40)** |

**Optimization Techniques**:

**1. Model Selection**:
- Use Claude 3 Haiku (cheapest) for chat and explanations
- Use Claude 3 Sonnet only for complex weekly reports
- Avoid Claude 3 Opus (most expensive)

**2. Token Reduction**:
- Limit context window to top 5 products (not all products)
- Set max_tokens=500 for chat, 1000 for reports
- Use concise prompts (avoid verbose instructions)

**3. Caching**:
```python
import hashlib

def get_cached_llm_response(query, context):
    # Generate cache key
    cache_key = hashlib.md5(f"{query}:{context}".encode()).hexdigest()
    
    # Check Redis cache
    cached_response = redis.get(cache_key)
    if cached_response:
        return json.loads(cached_response)
    
    # Call Bedrock if not cached
    response = bedrock.invoke_model(...)
    
    # Cache response (TTL: 1 hour)
    redis.setex(cache_key, 3600, json.dumps(response))
    
    return response
```

**4. Batch Processing**:
- Generate all weekly reports in a single Lambda invocation (not per-user)
- Use batch inference for forecast explanations


### 8.2 Lambda Cost Optimization

**Cost Breakdown** (per merchant/month):

| Lambda Function | Invocations | Duration | Memory | Cost |
|-----------------|-------------|----------|--------|------|
| UploadHandler | 4 | 5s | 512 MB | $0.0004 |
| DataValidator | 4 | 30s | 1024 MB | $0.0024 |
| ForecastGenerator | 4 | 120s | 2048 MB | $0.0192 |
| ChatHandler | 50 | 3s | 512 MB | $0.0030 |
| ReportGenerator | 4 | 20s | 512 MB | $0.0008 |
| **Total Lambda** | | | | **$0.026/month (~₹2.15)** |

**Optimization Techniques**:

**1. Right-Sizing Memory**:
- Use 512 MB for simple tasks (upload, chat)
- Use 1024 MB for data processing (validation)
- Use 2048 MB only for ML inference (forecasting)

**2. Async Invocations**:
- Use `InvocationType='Event'` for non-blocking tasks
- Reduces API Gateway wait time and improves UX

**3. Lambda Layers**:
- Package common dependencies (pandas, numpy, prophet) in Lambda Layer
- Reduces deployment package size and cold start time

**4. Provisioned Concurrency** (optional):
- For production, provision 1-2 instances of ForecastGenerator
- Eliminates cold starts for critical functions
- Cost: ~$10/month (skip for MVP)

### 8.3 DynamoDB Cost Optimization

**Cost Breakdown** (per merchant/month):

| Table | Reads | Writes | Storage | Cost |
|-------|-------|--------|---------|------|
| Forecasts | 1000 | 100 | 1 MB | $0.25 |
| ChatHistory | 500 | 50 | 0.5 MB | $0.13 |
| WeeklyReports | 100 | 4 | 0.1 MB | $0.03 |
| **Total DynamoDB** | | | | **$0.41/month (~₹34)** |

**Optimization Techniques**:

**1. On-Demand Pricing**:
- Use on-demand mode (pay-per-request) for MVP
- Switch to provisioned capacity if usage becomes predictable

**2. TTL (Time-to-Live)**:
- Auto-delete old forecasts after 7 days
- Reduces storage costs

**3. Sparse Indexes**:
- Only create GSIs (Global Secondary Indexes) for frequent queries
- Avoid over-indexing

### 8.4 S3 Cost Optimization

**Cost Breakdown** (per merchant/month):

| Storage Type | Size | Cost |
|--------------|------|------|
| Raw CSV (uploads/) | 10 MB | $0.0002 |
| Cleaned CSV (cleaned/) | 10 MB | $0.0002 |
| **Total S3** | | **$0.0004/month (~₹0.03)** |

**Optimization Techniques**:

**1. Lifecycle Policies**:
- Move `uploads/` to Glacier after 30 days (90% cost reduction)
- Delete `cleaned/` after 90 days (no longer needed)

**2. Compression**:
- Compress CSV files using gzip before storage
- Reduces storage and transfer costs by 70-80%

### 8.5 Total Cost Summary

**Per Merchant/Month**:
- Bedrock: $0.017 (~₹1.40)
- Lambda: $0.026 (~₹2.15)
- DynamoDB: $0.41 (~₹34)
- S3: $0.0004 (~₹0.03)
- **Total: $0.45/month (~₹37)**

**For 100 Merchants**:
- Total: $45/month (~₹3,700)
- Well within hackathon budget constraints

**Additional Costs** (shared across all merchants):
- API Gateway: $3.50/million requests (~$1/month for MVP)
- CloudFront: $0.085/GB (~$2/month for MVP)
- Cognito: Free tier (50,000 MAUs)
- **Grand Total: ~$50/month for 100 merchants**

---

## 🔐 9. Security & Compliance

### 9.1 IAM Roles & Permissions

**Principle of Least Privilege**: Each Lambda function has minimal required permissions

**UploadHandler Lambda Role**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::merchant-data/uploads/*"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:PutItem"],
      "Resource": "arn:aws:dynamodb:ap-south-1:*:table/Uploads"
    },
    {
      "Effect": "Allow",
      "Action": ["lambda:InvokeFunction"],
      "Resource": "arn:aws:lambda:ap-south-1:*:function:DataValidator"
    }
  ]
}
```

**ChatHandler Lambda Role**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel"],
      "Resource": "arn:aws:bedrock:ap-south-1::foundation-model/anthropic.claude-3-haiku-*"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:Query", "dynamodb:PutItem"],
      "Resource": [
        "arn:aws:dynamodb:ap-south-1:*:table/Forecasts",
        "arn:aws:dynamodb:ap-south-1:*:table/ChatHistory"
      ]
    }
  ]
}
```

### 9.2 Data Isolation

**User Data Segregation**:
- All S3 objects prefixed with `user_id`: `uploads/{user_id}/file.csv`
- All DynamoDB items partitioned by `user_id`
- Lambda functions validate `user_id` from JWT token before accessing data

**Access Control**:
```python
def lambda_handler(event, context):
    # Extract user_id from Cognito JWT token
    user_id = event['requestContext']['authorizer']['claims']['sub']
    
    # Validate that requested resource belongs to user
    requested_user_id = event['pathParameters']['user_id']
    if user_id != requested_user_id:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Forbidden'})
        }
    
    # Proceed with authorized access
    ...
```

### 9.3 Secure CSV Uploads

**Validation**:
```python
def validate_csv_upload(file_content):
    # 1. Check file size (<10MB)
    if len(file_content) > 10 * 1024 * 1024:
        raise ValueError("File too large")
    
    # 2. Check file extension
    if not filename.endswith('.csv'):
        raise ValueError("Only CSV files allowed")
    
    # 3. Scan for malicious content
    if b'<script>' in file_content or b'DROP TABLE' in file_content:
        raise ValueError("Malicious content detected")
    
    # 4. Validate CSV structure
    df = pd.read_csv(io.BytesIO(file_content))
    if len(df.columns) > 50:  # Prevent CSV bomb attacks
        raise ValueError("Too many columns")
    
    return True
```

**Encryption**:
- All S3 objects encrypted at rest (SSE-S3)
- All data in transit encrypted (HTTPS/TLS 1.2+)

### 9.4 Compliance (India DPDPA 2023)

**Data Privacy Requirements**:

**1. Consent**:
- Terms of Service: "By uploading data, you consent to AI-powered analysis"
- Privacy Policy: "Your data is used only for generating insights. Not shared with third parties."

**2. Data Retention**:
- Raw CSV files: Retained for 90 days, then deleted
- Forecasts: Auto-deleted after 7 days (DynamoDB TTL)
- Chat history: Retained for 30 days

**3. Right to Deletion**:
- Merchants can request account deletion
- Lambda function deletes all user data from S3 and DynamoDB

**4. Data Localization**:
- All data stored in ap-south-1 (Mumbai) region
- Complies with India data localization requirements

---

## 🚢 10. Deployment Strategy

### 10.1 Infrastructure as Code (IaC)

**Tool**: AWS SAM (Serverless Application Model)

**Project Structure**:
```
merchant-copilot/
├── template.yaml              # SAM template (infrastructure)
├── src/
│   ├── upload_handler/
│   │   └── app.py
│   ├── data_validator/
│   │   └── app.py
│   ├── forecast_generator/
│   │   └── app.py
│   ├── chat_handler/
│   │   └── app.py
│   └── report_generator/
│       └── app.py
├── layers/
│   └── ml_dependencies/
│       └── requirements.txt   # pandas, numpy, prophet
├── frontend/
│   └── build/                 # React build output
└── README.md
```

**SAM Template** (template.yaml):
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.11
    Timeout: 60
    Environment:
      Variables:
        REGION: ap-south-1

Resources:
  # S3 Bucket
  MerchantDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: merchant-data
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: MoveToGlacier
            Status: Enabled
            Transitions:
              - StorageClass: GLACIER
                TransitionInDays: 30

  # DynamoDB Tables
  ForecastsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: Forecasts
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: user_id
          AttributeType: S
        - AttributeName: product_name
          AttributeType: S
      KeySchema:
        - AttributeName: user_id
          KeyType: HASH
        - AttributeName: product_name
          KeyType: RANGE
      TimeToLiveSpecification:
        Enabled: true
        AttributeName: ttl

  # Lambda Functions
  UploadHandlerFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: UploadHandler
      CodeUri: src/upload_handler/
      Handler: app.lambda_handler
      MemorySize: 512
      Policies:
        - S3WritePolicy:
            BucketName: !Ref MerchantDataBucket
        - DynamoDBWritePolicy:
            TableName: !Ref UploadsTable

  # API Gateway
  MerchantAPI:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Auth:
        DefaultAuthorizer: CognitoAuthorizer
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: !GetAtt CognitoUserPool.Arn

  # Cognito User Pool
  CognitoUserPool:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: MerchantCopilotUsers
      AutoVerifiedAttributes:
        - email
```

### 10.2 CI/CD Pipeline

**Tool**: GitHub Actions

**Workflow** (.github/workflows/deploy.yml):
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1
      
      - name: Build Lambda Layers
        run: |
          pip install -r layers/ml_dependencies/requirements.txt -t layers/ml_dependencies/python
      
      - name: Deploy SAM Application
        run: |
          sam build
          sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
      
      - name: Build Frontend
        run: |
          cd frontend
          npm install
          npm run build
      
      - name: Deploy Frontend to S3
        run: |
          aws s3 sync frontend/build/ s3://merchant-copilot-frontend/
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_ID }} --paths "/*"
```

### 10.3 Environment Separation

**Environments**:
- **dev**: Development environment (for testing)
- **staging**: Pre-production environment (for demo)
- **prod**: Production environment (post-hackathon)

**Configuration**:
```yaml
# samconfig.toml
[dev.deploy.parameters]
stack_name = "merchant-copilot-dev"
s3_bucket = "merchant-copilot-artifacts-dev"
region = "ap-south-1"

[staging.deploy.parameters]
stack_name = "merchant-copilot-staging"
s3_bucket = "merchant-copilot-artifacts-staging"
region = "ap-south-1"
```

**Deployment Commands**:
```bash
# Deploy to dev
sam deploy --config-env dev

# Deploy to staging (for hackathon demo)
sam deploy --config-env staging
```

---

## 📈 11. Scalability & Future Expansion

### 11.1 WhatsApp Bot Integration

**Architecture**:
```
WhatsApp Business API
  ↓
Twilio/MessageBird Webhook
  ↓
API Gateway → WhatsAppHandler Lambda
  ↓
ChatHandler Lambda (reuse existing logic)
  ↓
Bedrock (LLM response)
  ↓
WhatsApp Business API (send response)
```

**Implementation**:
```python
def whatsapp_handler(event, context):
    # 1. Parse incoming WhatsApp message
    message = json.loads(event['body'])
    user_phone = message['from']
    user_message = message['text']
    
    # 2. Map phone number to user_id (DynamoDB lookup)
    user_id = get_user_id_by_phone(user_phone)
    
    # 3. Call existing ChatHandler logic
    response = chat_handler({'user_id': user_id, 'message': user_message, 'language': 'hi'})
    
    # 4. Send response via WhatsApp API
    send_whatsapp_message(user_phone, response['message'])
    
    return success_response()
```

**Benefits**:
- Merchants can interact with Copilot via WhatsApp (no app required)
- Weekly reports delivered as WhatsApp messages
- Alerts sent as WhatsApp notifications


### 11.2 Voice Assistant Integration

**Architecture**:
```
Merchant speaks in Hindi/Marathi
  ↓
AWS Transcribe (speech-to-text)
  ↓
ChatHandler Lambda
  ↓
Bedrock (LLM response)
  ↓
AWS Polly (text-to-speech)
  ↓
Audio response played to merchant
```

**Implementation**:
```python
def voice_handler(event, context):
    # 1. Receive audio file from frontend
    audio_file = event['audio_base64']
    language = event['language']  # hi-IN, mr-IN
    
    # 2. Transcribe audio to text (AWS Transcribe)
    transcribe = boto3.client('transcribe')
    job_name = f"transcribe_{timestamp()}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://merchant-data/audio/{job_name}.mp3'},
        MediaFormat='mp3',
        LanguageCode=language
    )
    
    # Wait for transcription to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            break
        time.sleep(2)
    
    # 3. Extract transcribed text
    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    transcript = requests.get(transcript_uri).json()
    user_message = transcript['results']['transcripts'][0]['transcript']
    
    # 4. Get LLM response (reuse ChatHandler logic)
    response = chat_handler({'user_id': user_id, 'message': user_message, 'language': language})
    
    # 5. Convert response to speech (AWS Polly)
    polly = boto3.client('polly')
    audio_response = polly.synthesize_speech(
        Text=response['message'],
        OutputFormat='mp3',
        VoiceId='Aditi' if language == 'hi-IN' else 'Raveena',  # Hindi/Marathi voices
        Engine='neural'
    )
    
    # 6. Return audio file
    return {
        'statusCode': 200,
        'body': base64.b64encode(audio_response['AudioStream'].read()).decode('utf-8'),
        'headers': {'Content-Type': 'audio/mpeg'}
    }
```

**Benefits**:
- Merchants can ask questions by speaking (no typing required)
- Ideal for low-literacy users
- Supports Hindi and Marathi voices

### 11.3 Market Intelligence Retrieval

**Architecture**:
```
Merchant asks: "What is the market trend for Cold Drinks?"
  ↓
ChatHandler Lambda detects market intelligence query
  ↓
Lambda calls external APIs:
  - Weather API (temperature trends)
  - News API (local events, festivals)
  - Competitor API (price trends)
  ↓
Bedrock combines merchant data + market data
  ↓
Response: "Cold Drinks demand is rising due to heatwave. Competitors increased prices by 10%."
```

**Implementation**:
```python
def get_market_intelligence(product_name, location):
    # 1. Get weather data (OpenWeatherMap API)
    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}").json()
    temperature = weather['main']['temp']
    
    # 2. Get news data (NewsAPI)
    news = requests.get(f"https://newsapi.org/v2/everything?q={product_name}").json()
    recent_news = news['articles'][:3]
    
    # 3. Get competitor prices (web scraping or API)
    competitor_prices = scrape_competitor_prices(product_name, location)
    
    # 4. Combine with merchant data
    context = {
        'merchant_data': get_merchant_data(user_id, product_name),
        'weather': {'temperature': temperature},
        'news': recent_news,
        'competitor_prices': competitor_prices
    }
    
    # 5. LLM generates insights
    prompt = f"""Analyze market trends for {product_name}:
    
Merchant Data: {context['merchant_data']}
Weather: {context['weather']}
Recent News: {context['news']}
Competitor Prices: {context['competitor_prices']}

Provide actionable insights."""

    response = bedrock.invoke_model(...)
    return response
```

**Benefits**:
- Enriches forecasts with external market data
- Helps merchants understand "why" demand is changing
- Competitive intelligence for pricing decisions

### 11.4 Multi-Store Support

**Architecture**:
```
Merchant manages 3 stores: Store A, Store B, Store C
  ↓
Each store uploads separate CSV files
  ↓
System generates forecasts per store
  ↓
Dashboard shows:
  - Consolidated view (all stores)
  - Store-level drill-down
  - Transfer recommendations (move stock from Store A to Store B)
```

**Database Schema**:
```python
# DynamoDB: Forecasts Table
{
  'user_id': 'merchant123',
  'store_id': 'store_a',  # New attribute
  'product_name': 'Atta 1kg',
  'forecast_data': {...}
}
```

**Transfer Recommendations**:
```python
def calculate_transfer_recommendations(user_id):
    # 1. Get forecasts for all stores
    stores = ['store_a', 'store_b', 'store_c']
    forecasts = {}
    for store in stores:
        forecasts[store] = get_forecasts(user_id, store)
    
    # 2. Identify surplus and deficit
    recommendations = []
    for product in all_products:
        surplus_stores = [s for s in stores if forecasts[s][product]['current_stock'] > forecasts[s][product]['forecast_7d'] * 1.5]
        deficit_stores = [s for s in stores if forecasts[s][product]['current_stock'] < forecasts[s][product]['forecast_7d'] * 0.5]
        
        if surplus_stores and deficit_stores:
            recommendations.append({
                'product': product,
                'from': surplus_stores[0],
                'to': deficit_stores[0],
                'quantity': calculate_transfer_qty(...)
            })
    
    return recommendations
```

**Benefits**:
- Optimize inventory across multiple locations
- Reduce stockouts by transferring surplus stock
- Consolidated reporting for multi-store merchants

---

## ✅ 12. Hackathon Readiness Checklist

### 12.1 MVP Scope (Must-Have for Demo)

**Core Features** (Priority 0):
- ✅ CSV upload and validation
- ✅ Demand forecasting (Prophet-based)
- ✅ Forecast visualization (charts with confidence bands)
- ✅ Copilot chat (Bedrock-powered Q&A)
- ✅ Multilingual support (English, Hindi, Marathi)
- ✅ Confidence scoring for all AI outputs
- ✅ Explainability ("Why?" for each recommendation)
- ✅ Weekly action plan generation
- ✅ Anomaly detection (spikes, drops)
- ✅ Inventory reorder recommendations

**Nice-to-Have** (Priority 1):
- ⚠️ Price optimization suggestions (if time permits)
- ⚠️ Email notifications (weekly reports)
- ⚠️ Admin dashboard (for monitoring)

**Out of Scope** (Post-Hackathon):
- ❌ WhatsApp integration
- ❌ Voice assistant
- ❌ Multi-store support
- ❌ Real-time POS integration

### 12.2 Demo Flow Mapping

**Demo Scenario**: Rajesh Kumar, Kirana Store Owner, Mumbai

**Step 1: Login** (30 seconds)
- Show Cognito authentication
- Merchant logs in with email/password

**Step 2: CSV Upload** (1 minute)
- Merchant uploads sample CSV (90 days of sales data)
- System validates and displays data quality report
- Show: "100 rows, 15 products, 95% completeness"

**Step 3: Dashboard View** (2 minutes)
- Show demand forecasts for top 5 products
- Highlight confidence scores (Green: 85%, Yellow: 70%)
- Show anomaly alerts: "Spike in Cold Drinks (+40%)"

**Step 4: Copilot Chat** (2 minutes)
- Merchant asks: "Which products should I order this week?"
- LLM responds in Hindi: "आपको इस सप्ताह आटा (50 kg), चावल (30 kg), और दाल (20 kg) ऑर्डर करनी चाहिए..."
- Show confidence score: 85%
- Show disclaimer: "AI-generated advice. Verify before acting."

**Step 5: Weekly Action Plan** (1 minute)
- Show auto-generated report:
  - Top 3 priorities: Reorder Atta, Discount Slow-Moving Products, Monitor Cold Drinks Spike
  - Explanations for each priority
  - Expected business impact

**Step 6: Explainability** (1 minute)
- Click "Why?" button on Atta recommendation
- Show: "Demand is forecasted to increase 25% due to upcoming festival season (Diwali in 2 weeks)"
- Show forecast chart with historical data + prediction + confidence bands

**Total Demo Time**: 7-8 minutes

### 12.3 Evaluation Criteria Alignment

**Criterion 1: Meaningful AI Use**
- ✅ Time-series ML forecasting (Prophet/ARIMA)
- ✅ LLM reasoning and explanation (Bedrock Claude 3)
- ✅ Anomaly detection (statistical methods)
- ✅ Natural language chat interface
- ✅ Automated report generation

**Criterion 2: Bharat-First Design**
- ✅ CSV upload (no API integrations required)
- ✅ Multilingual support (Hindi, Marathi)
- ✅ Low-cost architecture (~₹37/merchant/month)
- ✅ Mobile-responsive UI
- ✅ Simple, intuitive interface (no technical jargon)

**Criterion 3: Responsible AI**
- ✅ Confidence scores for all AI outputs
- ✅ Explainability ("Why?" for each recommendation)
- ✅ Disclaimers ("AI-generated advice. Verify before acting.")
- ✅ Input validation (prompt injection prevention)
- ✅ Human-in-the-loop (feedback mechanism)
- ✅ Bias mitigation (test across diverse products/regions)

**Criterion 4: Problem-Solution Mapping**
- ✅ Clear problem statement (MSME inventory wastage, suboptimal pricing)
- ✅ Quantified impact (reduce wastage by 20%, increase revenue by 10-15%)
- ✅ Feasible solution (AWS-native, low-cost, scalable)
- ✅ Target user personas (Kirana stores, small retailers)

**Criterion 5: Feasibility**
- ✅ Deployable in 48 hours (AWS SAM template)
- ✅ Single-region deployment (ap-south-1 Mumbai)
- ✅ Serverless architecture (no EC2 management)
- ✅ Well-documented codebase (README, comments)

### 12.4 Technical Validation Checklist

**Pre-Demo Testing**:
- [ ] Test CSV upload with sample data (100 rows, 15 products)
- [ ] Verify forecasts are generated within 60 seconds
- [ ] Test chat in all 3 languages (English, Hindi, Marathi)
- [ ] Verify confidence scores are displayed correctly
- [ ] Test anomaly detection with spike/drop scenarios
- [ ] Verify weekly report generation
- [ ] Test on mobile device (responsive UI)
- [ ] Load test: 10 concurrent users uploading CSVs
- [ ] Security test: Attempt prompt injection in chat
- [ ] Cost validation: Monitor AWS billing dashboard

**Backup Plan**:
- If Bedrock API fails: Use pre-generated responses (cached)
- If Prophet fails: Use simple moving average as fallback
- If DynamoDB throttles: Increase on-demand capacity temporarily

### 12.5 Presentation Materials

**Slide Deck** (10 slides):
1. Problem Statement (MSME challenges)
2. Solution Overview (Merchant Intelligence Copilot)
3. Architecture Diagram (AWS services)
4. AI Components (Forecasting + LLM reasoning)
5. Bharat-First Design (CSV, multilingual, low-cost)
6. Responsible AI (confidence, explainability, disclaimers)
7. Live Demo (7-8 minutes)
8. Impact Metrics (reduce wastage, increase revenue)
9. Scalability & Future Roadmap (WhatsApp, voice, multi-store)
10. Q&A

**Demo Video** (backup):
- Record 5-minute demo video showing all features
- Use in case of live demo technical issues

**GitHub Repository**:
- Clean, well-documented code
- README with setup instructions
- Architecture diagram (draw.io or Lucidchart)
- Sample CSV data for testing

---

## ⚠️ 13. Risk Mitigation

### 13.1 Technical Risks

**Risk 1: Bedrock API Latency**
- **Mitigation**: Use Claude 3 Haiku (fastest model), cache frequent queries, set timeout=30s

**Risk 2: Prophet Model Training Time**
- **Mitigation**: Use Lambda with 2048 MB memory, limit to 100 products per merchant, use ARIMA for products with <60 days data

**Risk 3: DynamoDB Throttling**
- **Mitigation**: Use on-demand capacity mode (auto-scaling), batch write operations

**Risk 4: Cold Start Latency**
- **Mitigation**: Use Lambda Layers for dependencies, keep functions warm with EventBridge (ping every 5 minutes)

### 13.2 Data Quality Risks

**Risk 1: Insufficient Historical Data**
- **Mitigation**: Require minimum 30 days of data, display warning if <60 days, use simple moving average as fallback

**Risk 2: Inconsistent Product Names**
- **Mitigation**: Normalize product names (lowercase, trim), use fuzzy matching for similar names

**Risk 3: Missing Values**
- **Mitigation**: Forward-fill for dates, median imputation for prices, flag rows with >50% missing values

### 13.3 User Adoption Risks

**Risk 1: Merchants Don't Trust AI**
- **Mitigation**: Show confidence scores, provide explainability, add disclaimers, enable feedback mechanism

**Risk 2: Language Barriers**
- **Mitigation**: Support Hindi and Marathi, use simple language (no jargon), provide voice input (future)

**Risk 3: Technical Complexity**
- **Mitigation**: Simple CSV upload (no API integrations), intuitive UI, video tutorials

---

## 🎯 14. Success Metrics (Post-Launch)

### 14.1 User Engagement Metrics

- **Daily Active Users (DAU)**: Target 60% of registered merchants
- **CSV Upload Frequency**: Target 1 upload/week per merchant
- **Chat Queries**: Target 10 queries/week per merchant
- **Weekly Report Open Rate**: Target 70%

### 14.2 AI Performance Metrics

- **Forecast Accuracy (MAPE)**: Target <20%
- **LLM Response Relevance**: Target >85% (human evaluation)
- **Confidence Score Calibration**: Target >80%
- **Anomaly Detection Precision**: Target >75%

### 14.3 Business Impact Metrics

- **Inventory Wastage Reduction**: Target 20% (measured via user surveys)
- **Revenue Increase**: Target 10-15% (measured via user surveys)
- **Time Saved**: Target 5+ hours/week per merchant (measured via user surveys)

### 14.4 Cost Metrics

- **AWS Cost per Merchant**: Target <₹50/month
- **Bedrock Cost per Merchant**: Target <₹2/month
- **Total System Cost**: Target <₹5,000/month for 100 merchants

---

## 🏆 15. Conclusion

The Merchant Intelligence Copilot is a production-ready, AI-powered decision support system designed specifically for Indian MSMEs. The architecture leverages AWS-native services (Bedrock, Lambda, DynamoDB, S3) to deliver:

1. **Meaningful AI**: Time-series forecasting + LLM reasoning + anomaly detection
2. **Bharat-First Design**: CSV upload, multilingual, low-cost, mobile-responsive
3. **Responsible AI**: Confidence scoring, explainability, disclaimers, human oversight
4. **Scalability**: Serverless architecture, pay-per-use pricing, future-ready (WhatsApp, voice, multi-store)
5. **Feasibility**: Deployable in 48 hours, well-documented, cost-effective (~₹37/merchant/month)

This design document provides a complete blueprint for building and deploying the MVP within the hackathon timeline, with clear alignment to evaluation criteria and a roadmap for post-hackathon expansion.

---

**End of Design Document**

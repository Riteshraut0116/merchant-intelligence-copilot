# Implementation Plan: Merchant Intelligence Copilot for Indian MSMEs

## Overview

This implementation plan breaks down the Merchant Intelligence Copilot into actionable coding tasks for a 48-hour hackathon MVP. The focus is on P0 (Must-Have) features using an AWS-only serverless stack (Lambda, Bedrock, S3, DynamoDB, API Gateway, Cognito).

**Key Technologies**:
- Backend: python 3.12 (Lambda functions)
- Frontend: React 18 with TypeScript
- ML: Prophet (time-series forecasting)
- LLM: Amazon Bedrock (Claude 3 Haiku/Sonnet)
- Infrastructure: AWS SAM (Infrastructure as Code)

**Implementation Strategy**:
- Build backend services first (data pipeline, forecasting, LLM integration)
- Implement frontend dashboard and chat interface
- Wire everything together with API Gateway
- Deploy using AWS SAM

---

## Tasks

- [ ] 1. Set up project structure and AWS infrastructure
  - Create directory structure for Lambda functions, frontend, and IaC
  - Initialize AWS SAM template with core resources (S3, DynamoDB tables, API Gateway, Cognito)
  - Configure IAM roles with least-privilege permissions for each Lambda function
  - Set up Python Lambda Layer with dependencies (pandas, numpy, prophet, boto3)
  - _Requirements: TC-1.1, TC-3.1, NFR-3.2_

- [ ] 2. Implement CSV upload and data validation pipeline
  - [ ] 2.1 Create UploadHandler Lambda function
    - Implement multipart/form-data parsing for CSV uploads
    - Validate file size (<10MB) and format (.csv extension)
    - Upload raw CSV to S3 with user-scoped path: `uploads/{user_id}/{timestamp}.csv`
    - Store upload metadata in DynamoDB Uploads table
    - Trigger DataValidator Lambda asynchronously
    - _Requirements: FR-1.1, NFR-3.3_
  
  - [ ] 2.2 Create DataValidator Lambda function
    - Download CSV from S3 and parse with pandas
    - Validate required columns (date, product_name, quantity_sold, price, revenue)
    - Clean data: normalize product names, convert dates, handle missing values
    - Detect outliers using Z-score method (threshold > 3)
    - Generate data quality report (completeness score, outliers, date range)
    - Save cleaned CSV to S3: `cleaned/{user_id}/{timestamp}_cleaned.csv`
    - Store quality report in DynamoDB DataQuality table
    - Trigger ForecastGenerator Lambda asynchronously
    - _Requirements: FR-1.2, RAI-4.2_
  
  - [ ]* 2.3 Write unit tests for data validation
    - Test CSV parsing with valid and invalid formats
    - Test missing value handling (forward-fill, median imputation)
    - Test outlier detection with synthetic data
    - Test error handling for malformed CSV files
    - _Requirements: FR-1.2_

- [ ] 3. Implement demand forecasting engine
  - [ ] 3.1 Create ForecastGenerator Lambda function
    - Load cleaned CSV from S3 and group by product and date
    - For each product with ≥30 days of data, train Prophet model
    - Configure Prophet with daily and weekly seasonality
    - Generate 7-day and 30-day forecasts with confidence intervals
    - Calculate confidence score based on prediction interval width
    - Store forecasts in DynamoDB Forecasts table with TTL (7 days)
    - Trigger AnomalyDetector and ReportGenerator Lambdas asynchronously
    - _Requirements: FR-2.1, NFR-2.2_
  
  - [ ]* 3.2 Write property test for forecast generation
    - **Property 1: Forecast output structure**
    - **Validates: Requirements FR-2.1**
    - For any valid product sales data with ≥30 days, generating a forecast should produce output containing forecast_7d, forecast_30d, and confidence_score fields
    - _Requirements: FR-2.1_
  
  - [ ]* 3.3 Write unit tests for edge cases
    - Test handling of products with <30 days of data (should skip)
    - Test confidence score calculation with wide vs narrow prediction intervals
    - Test Prophet model training with seasonal vs non-seasonal data
    - _Requirements: FR-2.1_

- [ ] 4. Implement anomaly detection system
  - [ ] 4.1 Create AnomalyDetector Lambda function
    - Retrieve forecasts from DynamoDB for user
    - Load historical sales data from S3
    - Calculate week-over-week change for each product
    - Detect spikes (>30% increase), drops (>30% decrease), and slow-moving products (<50% average velocity)
    - Classify anomaly severity (high: >50% change, medium: 30-50%)
    - Store anomalies in DynamoDB Anomalies table
    - _Requirements: FR-5.1, FR-10.1, FR-10.2_
  
  - [ ]* 4.2 Write property test for anomaly detection
    - **Property 2: Anomaly detection consistency**
    - **Validates: Requirements FR-5.1**
    - For any product with week-over-week change >30%, the anomaly detector should flag it as either a spike or drop with appropriate severity
    - _Requirements: FR-5.1_

- [ ] 5. Checkpoint - Ensure data pipeline tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement LLM-powered chat interface
  - [ ] 6.1 Create ChatHandler Lambda function
    - Extract user_id from Cognito JWT token in API Gateway event
    - Parse user message and language preference from request body
    - Retrieve merchant context from DynamoDB (forecasts, anomalies, recent data)
    - Build RAG prompt with system instructions and merchant context
    - Call Amazon Bedrock (Claude 3 Haiku) with temperature=0.3 for factual responses
    - Parse LLM response and calculate confidence score based on data availability
    - Store chat history in DynamoDB ChatHistory table
    - Return response with confidence score and disclaimer
    - _Requirements: FR-6.1, FR-7.1, RAI-2.1_
  
  - [ ] 6.2 Implement prompt safety and input validation
    - Validate chat input for prompt injection patterns (regex checks)
    - Reject messages >500 characters or unrelated to business data
    - Filter LLM output to remove hallucinated product names not in merchant's data
    - Log suspicious queries for admin review
    - _Requirements: FR-6.2, RAI-3.2, RAI-4.1_
  
  - [ ]* 6.3 Write property test for chat safety
    - **Property 3: Prompt injection prevention**
    - **Validates: Requirements FR-6.2, RAI-4.1**
    - For any input containing prompt injection patterns (e.g., "ignore previous instructions"), the validation function should reject it
    - _Requirements: FR-6.2, RAI-4.1_
  
  - [ ]* 6.4 Write unit tests for chat handler
    - Test context building with various merchant data scenarios
    - Test confidence score calculation (high data vs low data)
    - Test multilingual response generation (EN, HI, MR)
    - Test error handling for Bedrock API failures
    - _Requirements: FR-6.1, FR-7.1_

- [ ] 7. Implement forecast explainability with LLM
  - [ ] 7.1 Create ForecastExplainer Lambda function
    - Retrieve forecast data for specific product from DynamoDB
    - Extract key drivers (seasonality components, trend, recent changes)
    - Build prompt for Bedrock to generate plain-language explanation
    - Call Bedrock (Claude 3 Haiku) with structured context
    - Return explanation with confidence score
    - _Requirements: FR-2.2, FR-9.2, RAI-5.1_
  
  - [ ]* 7.2 Write unit tests for explainability
    - Test explanation generation for increasing vs decreasing trends
    - Test handling of seasonal patterns in explanations
    - Test multilingual explanation generation
    - _Requirements: FR-2.2, FR-9.2_

- [ ] 8. Implement weekly action plan generator
  - [ ] 8.1 Create ReportGenerator Lambda function
    - Retrieve all forecasts and anomalies for user from DynamoDB
    - Calculate inventory reorder recommendations (forecast + 20% safety stock)
    - Identify top 5 products to reorder and slow-moving products
    - Build comprehensive prompt for Bedrock (Claude 3 Sonnet for better reasoning)
    - Generate structured weekly action plan with top 3 priorities and explanations
    - Store report in DynamoDB WeeklyReports table
    - _Requirements: FR-3.1, FR-8.1, RAI-5.1_
  
  - [ ]* 8.2 Write unit tests for report generation
    - Test reorder quantity calculation with various forecast scenarios
    - Test priority ranking logic (urgency levels)
    - Test report generation with different data availability levels
    - _Requirements: FR-3.1, FR-8.1_

- [ ] 9. Checkpoint - Ensure backend Lambda tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Set up API Gateway and authentication
  - [ ] 10.1 Configure API Gateway REST API
    - Define API endpoints: /upload, /forecast, /chat, /report, /alerts
    - Configure CORS for frontend domain
    - Set up request validation with JSON schemas
    - Configure throttling (1000 req/sec per user, burst: 2000)
    - _Requirements: TC-1.1, NFR-2.1_
  
  - [ ] 10.2 Set up AWS Cognito authentication
    - Create Cognito User Pool with email verification
    - Configure Cognito Authorizer for API Gateway
    - Set up JWT token validation
    - Create test users for demo
    - _Requirements: NFR-3.2_
  
  - [ ] 10.3 Wire Lambda functions to API Gateway
    - Connect UploadHandler to POST /upload endpoint
    - Connect ChatHandler to POST /chat endpoint
    - Connect ForecastExplainer to GET /forecast/{product_id}/explain endpoint
    - Connect ReportGenerator to GET /report/weekly endpoint
    - Create Lambda function for GET /forecast/all to retrieve all forecasts
    - Create Lambda function for GET /alerts to retrieve anomalies
    - _Requirements: TC-1.1_

- [ ] 11. Implement React frontend dashboard
  - [ ] 11.1 Set up React project with TypeScript
    - Initialize React app with TypeScript template
    - Install dependencies: recharts, axios, tailwindcss, aws-amplify
    - Configure Tailwind CSS for mobile-responsive design
    - Set up AWS Amplify for Cognito authentication
    - Create routing structure (Dashboard, Upload, Chat, Reports)
    - _Requirements: TC-3.2_
  
  - [ ] 11.2 Create CSV upload interface
    - Build drag-and-drop file upload component
    - Implement client-side CSV validation (file size, format)
    - Show upload progress indicator
    - Display data quality report after validation
    - Handle error states with clear messages
    - _Requirements: FR-1.1, FR-1.2_
  
  - [ ] 11.3 Create forecast dashboard with visualizations
    - Build forecast cards showing 7-day and 30-day predictions
    - Implement time-series charts with Recharts (historical + forecast + confidence bands)
    - Display confidence scores with color-coded badges (Green >80%, Yellow 60-80%, Red <60%)
    - Add "Why?" button to expand forecast explanations
    - Show reorder recommendations with urgency indicators
    - _Requirements: FR-2.1, FR-2.2, FR-3.1, FR-9.1, FR-9.2_
  
  - [ ] 11.4 Create alerts panel for anomalies
    - Display anomaly cards (spikes, drops, slow-moving products)
    - Show severity indicators (high, medium)
    - Include LLM-generated explanations for each anomaly
    - Implement filtering by anomaly type
    - _Requirements: FR-5.1, FR-10.1, FR-10.2_
  
  - [ ]* 11.5 Write integration tests for dashboard
    - Test forecast data fetching and rendering
    - Test chart rendering with various data scenarios
    - Test confidence score display logic
    - Test responsive layout on mobile devices
    - _Requirements: FR-2.1, FR-9.1_

- [ ] 12. Implement Copilot chat interface
  - [ ] 12.1 Create chat UI component
    - Build chat message list with user and assistant messages
    - Implement message input with send button
    - Show typing indicator while waiting for LLM response
    - Display confidence scores and disclaimers with each response
    - Persist chat history in component state
    - _Requirements: FR-6.1, RAI-2.1_
  
  - [ ] 12.2 Implement language selector
    - Create dropdown for language selection (English, Hindi, Marathi)
    - Store language preference in localStorage
    - Pass language parameter with all API calls
    - Update UI labels using react-i18next
    - _Requirements: FR-7.1_
  
  - [ ]* 12.3 Write integration tests for chat
    - Test message sending and response rendering
    - Test language switching functionality
    - Test confidence score display
    - Test error handling for API failures
    - _Requirements: FR-6.1, FR-7.1_

- [ ] 13. Implement weekly action plan view
  - [ ] 13.1 Create report display component
    - Fetch weekly report from API
    - Display structured action plan with priorities
    - Show explanations and expected business impact
    - Add disclaimer banner at top
    - Implement print/export functionality
    - _Requirements: FR-8.1, RAI-2.1_
  
  - [ ]* 13.2 Write unit tests for report component
    - Test report data parsing and rendering
    - Test priority display logic
    - Test multilingual report display
    - _Requirements: FR-8.1_

- [ ] 14. Implement authentication flow in frontend
  - [ ] 14.1 Create login and signup pages
    - Build login form with email/password fields
    - Implement Cognito authentication with AWS Amplify
    - Handle authentication errors with user-friendly messages
    - Store JWT token in localStorage
    - Implement auto-redirect to dashboard after login
    - _Requirements: NFR-3.2_
  
  - [ ] 14.2 Add authentication guards to routes
    - Protect dashboard routes with authentication check
    - Redirect unauthenticated users to login page
    - Add logout functionality
    - _Requirements: NFR-3.2_

- [ ] 15. Checkpoint - Ensure frontend integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Implement confidence scoring system
  - [ ] 16.1 Create confidence calculation utilities
    - Implement forecast confidence based on prediction interval width
    - Implement data availability confidence based on historical data quantity
    - Combine forecast and data confidence with weighted average (70/30)
    - Implement chat confidence based on context availability
    - _Requirements: FR-9.1, RAI-1.1_
  
  - [ ]* 16.2 Write property test for confidence calibration
    - **Property 4: Confidence score bounds**
    - **Validates: Requirements FR-9.1, RAI-1.1**
    - For any forecast or recommendation, the confidence score should be between 0 and 100 inclusive
    - _Requirements: FR-9.1, RAI-1.1_

- [ ] 17. Implement multilingual support
  - [ ] 17.1 Create i18n translation files
    - Create locales/en.json with English UI labels
    - Create locales/hi.json with Hindi translations
    - Create locales/mr.json with Marathi translations
    - Configure react-i18next with language files
    - _Requirements: FR-7.1_
  
  - [ ] 17.2 Update LLM prompts for multilingual output
    - Modify system prompts to specify output language
    - Test LLM responses in all three languages
    - Implement fallback to English if language not supported
    - _Requirements: FR-7.1_
  
  - [ ]* 17.3 Write unit tests for multilingual support
    - Test language switching in UI
    - Test LLM response generation in each language
    - Test fallback behavior
    - _Requirements: FR-7.1_

- [ ] 18. Implement responsible AI features
  - [ ] 18.1 Add disclaimers throughout UI
    - Add banner to dashboard: "AI-generated recommendations. Verify before acting."
    - Add disclaimer to chat interface
    - Add disclaimer to weekly reports
    - Include disclaimer in all API responses
    - _Requirements: RAI-2.1, RAI-2.2_
  
  - [ ] 18.2 Implement feedback mechanism
    - Add thumbs up/down buttons to recommendations
    - Create FeedbackHandler Lambda to store feedback in DynamoDB
    - Wire feedback buttons to API endpoint
    - _Requirements: RAI-3.3_
  
  - [ ]* 18.3 Write unit tests for feedback system
    - Test feedback submission and storage
    - Test feedback retrieval for admin review
    - _Requirements: RAI-3.3_

- [ ] 19. Deploy infrastructure with AWS SAM
  - [ ] 19.1 Complete SAM template configuration
    - Define all Lambda functions with proper memory and timeout settings
    - Configure DynamoDB tables with on-demand capacity and TTL
    - Set up S3 bucket with lifecycle policies (move to Glacier after 30 days)
    - Configure API Gateway with Cognito authorizer
    - Define IAM roles with least-privilege permissions
    - _Requirements: TC-1.1, TC-3.1, NFR-4.2_
  
  - [ ] 19.2 Build and deploy backend
    - Build Lambda Layer with Python dependencies
    - Run `sam build` to package Lambda functions
    - Run `sam deploy` to deploy to ap-south-1 region
    - Verify all resources created successfully in AWS Console
    - Test API endpoints with Postman or curl
    - _Requirements: TC-3.1_
  
  - [ ] 19.3 Deploy frontend to S3 and CloudFront
    - Build React app with `npm run build`
    - Create S3 bucket for static hosting
    - Upload build files to S3
    - Create CloudFront distribution for HTTPS
    - Configure custom domain (optional)
    - _Requirements: TC-3.2_

- [ ] 20. End-to-end integration testing
  - [ ] 20.1 Test complete user journey
    - Test user signup and login flow
    - Test CSV upload with sample data (90 days, 15 products)
    - Verify data quality report displays correctly
    - Verify forecasts generate within 60 seconds
    - Test chat queries in all three languages
    - Verify weekly report generation
    - Test anomaly alerts display
    - _Requirements: All FR requirements_
  
  - [ ]* 20.2 Perform security testing
    - Test prompt injection attempts in chat
    - Test SQL injection in CSV uploads
    - Verify JWT token validation
    - Test user data isolation (users can only access their own data)
    - _Requirements: NFR-3.3, RAI-4.1_
  
  - [ ]* 20.3 Perform load testing
    - Test 10 concurrent CSV uploads
    - Test 50 concurrent chat queries
    - Monitor Lambda execution times and errors
    - Verify DynamoDB throttling doesn't occur
    - _Requirements: NFR-1.1, NFR-2.1_

- [ ] 21. Prepare demo materials
  - [ ] 21.1 Create sample data and test accounts
    - Generate realistic sample CSV with 90 days of sales data for 15 products
    - Include seasonal patterns and anomalies in sample data
    - Create demo user accounts in Cognito
    - Pre-load sample data for instant demo
    - _Requirements: Demo readiness_
  
  - [ ] 21.2 Document setup and deployment
    - Write README with architecture overview
    - Document deployment steps (SAM commands)
    - Create architecture diagram (Mermaid or draw.io)
    - Document API endpoints and request/response formats
    - Add troubleshooting guide
    - _Requirements: TC-3.1_
  
  - [ ] 21.3 Create demo script and presentation
    - Write 7-8 minute demo script covering all key features
    - Prepare slide deck (10 slides) covering problem, solution, architecture, AI components, Bharat-first design, responsible AI
    - Record backup demo video (5 minutes)
    - Test demo flow end-to-end
    - _Requirements: Demo readiness_

- [ ] 22. Final checkpoint - Ensure all systems operational
  - Ensure all tests pass, ask the user if questions arise.

---

## Notes

- Tasks marked with `*` are optional testing tasks that can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties across generated inputs
- Unit tests validate specific examples and edge cases
- Focus on P0 (Must-Have) features for 48-hour hackathon timeline
- P1 features (price optimization, email notifications) can be added post-hackathon if time permits

---

## Testing Strategy

**Dual Testing Approach**:
- **Unit Tests**: Validate specific examples, edge cases, and error conditions for each component
- **Property Tests**: Validate universal properties across randomly generated inputs (minimum 100 iterations per test)

**Property-Based Testing Configuration**:
- Use `hypothesis` library for Python property tests
- Use `fast-check` library for TypeScript property tests (frontend)
- Each property test must reference its design document property
- Tag format: `# Feature: merchant-intelligence-copilot, Property {number}: {property_text}`

**Test Coverage Goals**:
- Backend Lambda functions: >80% code coverage
- Frontend components: >70% code coverage
- Critical paths (CSV upload, forecasting, chat): 100% coverage

**Testing Priority**:
- P0: Data validation, forecasting, chat safety, authentication
- P1: Anomaly detection, report generation, multilingual support
- P2: UI components, feedback mechanism

---

## Deployment Checklist

**Pre-Deployment**:
- [ ] All unit tests passing
- [ ] All property tests passing (100+ iterations each)
- [ ] Security validation complete (prompt injection, data isolation)
- [ ] Sample data prepared
- [ ] Demo accounts created

**Deployment**:
- [ ] SAM template validated (`sam validate`)
- [ ] Backend deployed to ap-south-1 (`sam deploy`)
- [ ] Frontend built and deployed to S3/CloudFront
- [ ] API endpoints tested with Postman
- [ ] End-to-end user journey tested

**Post-Deployment**:
- [ ] Monitor CloudWatch logs for errors
- [ ] Verify AWS costs within budget (~$50/month for 100 merchants)
- [ ] Test demo flow multiple times
- [ ] Prepare backup plan (cached responses, fallback models)

---

## Cost Monitoring

**Target Costs** (per merchant/month):
- Bedrock: ~$0.017 (~₹1.40)
- Lambda: ~$0.026 (~₹2.15)
- DynamoDB: ~$0.41 (~₹34)
- S3: ~$0.0004 (~₹0.03)
- **Total: ~$0.45/month (~₹37)**

**For 100 Merchants**: ~$50/month total

**Cost Optimization Techniques**:
- Use Claude 3 Haiku (cheapest model) for chat
- Cache frequent LLM queries in ElastiCache (optional)
- Set max_tokens limits (500 for chat, 1000 for reports)
- Use DynamoDB TTL to auto-delete old forecasts
- Compress CSV files before S3 storage

---

**End of Implementation Plan**

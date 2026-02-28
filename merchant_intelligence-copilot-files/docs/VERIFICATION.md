# Verification Checklist

## Local Development Verification (SAM Local)

### Backend Setup
- [ ] Navigate to `backend` directory
- [ ] Run `sam build` successfully
- [ ] Run `sam local start-api --port 3000`
- [ ] Verify health endpoint: `curl http://127.0.0.1:3000/health`
- [ ] Backend responds with 200 OK

### Frontend Setup
- [ ] Navigate to `frontend` directory
- [ ] Run `npm install` successfully
- [ ] Copy `.env.example` to `.env`
- [ ] Set `VITE_API_BASE_URL=http://127.0.0.1:3000`
- [ ] Set `VITE_GITHUB_URL` (optional)
- [ ] Run `npm run dev` successfully
- [ ] Frontend opens at `http://localhost:5173`

### UI Features Verification

#### Header & Navigation
- [ ] App name displays: "Merchant Intelligence Copilot"
- [ ] Team name displays: "Bharat Brain Wave"
- [ ] API status indicator shows "API Connected" (green) or "API Not Connected" (red/gray)
- [ ] Theme toggle button works (☀️/🌙)
- [ ] GitHub icon appears (if VITE_GITHUB_URL is set)
- [ ] GitHub link opens in new tab with correct URL
- [ ] Info banner displays: "AI‑assisted insights to support smarter business decisions."
- [ ] Sidebar navigation works on desktop
- [ ] Mobile menu button works on mobile
- [ ] Footer displays copyright and hackathon info

#### Upload Data Page
- [ ] Drag-and-drop area works
- [ ] Browse files button works
- [ ] CSV validation checks required columns
- [ ] Error message shows for invalid CSV
- [ ] Preview shows first 5 rows
- [ ] File name and size display correctly
- [ ] Language selector works (EN/HI/MR)
- [ ] "Analyze Data" button triggers API call
- [ ] Loading state shows during analysis
- [ ] Success redirects to Dashboard
- [ ] Data persists in localStorage

#### Dashboard Page
- [ ] Shows empty state with CTA when no data
- [ ] KPI cards display correct values:
  - Products Analyzed
  - Alerts Count
  - Average Confidence
  - Top Reorder Item
- [ ] Product selector dropdown populates
- [ ] Forecast chart renders with selected product
- [ ] Chart shows confidence bands (if available)
- [ ] Insights table displays all products
- [ ] Confidence badges color-coded correctly:
  - Green >80%
  - Yellow 60-80%
  - Red <60%
- [ ] Urgency badges display (high/medium)
- [ ] Anomaly alerts show with chips
- [ ] "Why?" button opens explainability drawer
- [ ] Drawer shows:
  - Demand reasoning
  - Reorder logic
  - Confidence explanation
  - Disclaimer
- [ ] Drawer closes on click outside or X button

#### Copilot Chat Page
- [ ] Empty state shows with sample questions
- [ ] Sample question buttons populate input
- [ ] Language selector works
- [ ] Input field accepts text
- [ ] Enter key sends message
- [ ] Send button works
- [ ] User messages appear on right (blue)
- [ ] Assistant messages appear on left (gray)
- [ ] Loading animation shows during API call
- [ ] Confidence score displays (if available)
- [ ] Disclaimer banner shows
- [ ] Graceful fallback if /chat endpoint missing
- [ ] Messages scroll to bottom automatically

#### Weekly Report Page
- [ ] Fetches from /weekly-report endpoint
- [ ] Falls back to client-side generation if endpoint missing
- [ ] Shows top 3 priorities with:
  - Title
  - Description
  - Expected impact
- [ ] Shows risks and alerts
- [ ] Generation date displays
- [ ] "Export" button copies Markdown to clipboard
- [ ] Disclaimer banner shows

#### About Page
- [ ] Problem section displays
- [ ] Solution section displays
- [ ] AI Usage section explains:
  - Forecasting
  - Amazon Bedrock reasoning
- [ ] Responsible AI section explains:
  - Confidence scoring
  - Transparency
  - Disclaimers
- [ ] Hackathon context displays
- [ ] All content readable in light and dark modes

### Theme & Responsiveness
- [ ] Light mode works correctly
- [ ] Dark mode works correctly
- [ ] Theme persists in localStorage
- [ ] All pages responsive on mobile (< 640px)
- [ ] All pages responsive on tablet (640px - 1024px)
- [ ] All pages responsive on desktop (> 1024px)
- [ ] Sidebar collapses on mobile
- [ ] Mobile menu works

### API Integration
- [ ] Health check works
- [ ] POST /generate-insights works with CSV
- [ ] Response data structure handled correctly
- [ ] Defensive parsing for varying response formats
- [ ] Error states handled gracefully
- [ ] Loading states show during API calls
- [ ] API errors display user-friendly messages

## Production Deployment Verification (AWS)

### Backend Deployment
- [ ] `sam build` completes successfully
- [ ] `sam deploy --guided` completes successfully
- [ ] CloudFormation stack created
- [ ] API Gateway endpoint created
- [ ] Lambda functions deployed
- [ ] IAM roles created with Bedrock permissions
- [ ] Health endpoint accessible: `curl https://<api-url>/prod/health`
- [ ] Generate insights endpoint works

### Frontend Deployment
- [ ] `npm run build` completes successfully
- [ ] Build output in `dist/` directory
- [ ] Deployed to hosting platform (Netlify/Vercel/S3)
- [ ] Environment variables set:
  - VITE_API_BASE_URL points to API Gateway URL
  - VITE_GITHUB_URL set (optional)
- [ ] Frontend accessible via public URL
- [ ] API calls work from deployed frontend
- [ ] CORS configured correctly

### End-to-End Testing
- [ ] Upload CSV from deployed frontend
- [ ] Data analyzed successfully
- [ ] Dashboard displays insights
- [ ] Charts render correctly
- [ ] Chat works (or shows graceful fallback)
- [ ] Weekly report generates
- [ ] All features work in production

## Acceptance Criteria

### Must Have (All Required)
- [x] npm run dev works (frontend)
- [x] Header shows theme toggle + GitHub icon (env-driven)
- [x] API status indicator works via GET /health
- [x] CSV upload works with validation + preview + analyze
- [x] Dashboard shows KPIs, charts, badges, and "Why?" drawer
- [x] Copilot Chat does not crash without /chat endpoint
- [x] Weekly Report works with backend OR client-side fallback
- [x] About page + footer present
- [x] README clearly explains Local (SAM) vs AWS API Gateway usage
- [x] Mobile responsive and polished UI
- [x] Light/dark theme toggle works
- [x] No hardcoded API URLs (env-driven only)
- [x] Defensive parsing for backend response differences
- [x] Loading skeletons and friendly empty/error states

### Nice to Have (Optional)
- [ ] Chat endpoint implemented and working
- [ ] Weekly report endpoint implemented
- [ ] Additional languages beyond EN/HI/MR
- [ ] Advanced chart interactions
- [ ] User authentication
- [ ] Data persistence beyond localStorage

## Known Limitations
- Chat and Weekly Report endpoints may not exist yet (graceful fallback implemented)
- Client-side CSV parsing (no server-side validation beyond API)
- localStorage used for persistence (no database)
- No user authentication (demo mode)
- Single-user experience (no multi-tenancy)

## Quick Verification Commands

### Local Development
```powershell
# Terminal 1: Backend
cd backend
sam build
sam local start-api --port 3000

# Terminal 2: Frontend
cd frontend
npm install
copy .env.example .env
# Edit .env: VITE_API_BASE_URL=http://127.0.0.1:3000
npm run dev

# Terminal 3: Test
curl http://127.0.0.1:3000/health
# Open browser: http://localhost:5173
```

### Production
```powershell
# Deploy backend
cd backend
sam build
sam deploy --guided --region ap-south-1
# Note the ApiUrl output

# Deploy frontend
cd frontend
# Update .env: VITE_API_BASE_URL=<ApiUrl>
npm run build
# Deploy dist/ to hosting platform
```

## Success Indicators
✅ All pages load without errors
✅ API status indicator shows green
✅ CSV upload and analysis works
✅ Dashboard displays insights with charts
✅ Theme toggle works
✅ Mobile responsive
✅ No console errors
✅ Graceful error handling
✅ Professional, polished UI

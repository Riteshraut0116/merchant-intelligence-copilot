# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites
- Node.js 18+ installed
- python 3.12+ installed
- AWS SAM CLI installed ([Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html))
- PowerShell (Windows) or Bash (Mac/Linux)

### Step 1: Clone Repository
```powershell
git clone https://github.com/Riteshraut0116/merchant-intelligence-copilot.git
cd merchant-intelligence-copilot/merchant_intelligence-copilot-files
```

### Step 2: Start Backend (Terminal 1)
```powershell
cd backend
sam build
sam local start-api --port 3000
```

Wait for: `Running on http://127.0.0.1:3000`

### Step 3: Start Frontend (Terminal 2)
```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Wait for: `Local: http://localhost:5173`

### Step 4: Open Browser
Navigate to: `http://localhost:5173`

### Step 5: Upload Sample Data
1. Click "Upload Data" in sidebar
2. Drag and drop `sample-data/msme_sales_90days.csv`
3. Select language (English/Hindi/Marathi)
4. Click "Analyze Data"
5. Wait 10-30 seconds
6. View insights on Dashboard!

## 🎯 Quick Demo Flow

1. **Dashboard** - View KPIs, charts, and insights
2. **Click "Why?"** - See explainability for any product
3. **Copilot Chat** - Ask "Which products should I order?"
4. **Weekly Report** - View automated action plan
5. **About** - Learn about responsible AI features
6. **Theme Toggle** - Try light/dark mode (top right)

## 🔧 Troubleshooting

### Backend won't start
- Ensure AWS SAM CLI is installed: `sam --version`
- Check Python version: `python --version` (should be 3.11+)
- Try: `sam build --use-container` if local build fails

### Frontend won't start
- Ensure Node.js is installed: `node --version` (should be 18+)
- Delete `node_modules` and run `npm install` again
- Check `.env` file exists with `VITE_API_BASE_URL=http://127.0.0.1:3000`

### API Not Connected
- Verify backend is running on port 3000
- Check: `curl http://127.0.0.1:3000/health`
- Ensure `.env` has correct `VITE_API_BASE_URL`

### CSV Upload Fails
- Ensure CSV has required columns: date, product_name, quantity_sold, price, revenue
- Check file is valid CSV format (not Excel)
- Try sample file: `sample-data/msme_sales_90days.csv`

## 📱 Mobile Testing
Open browser dev tools (F12) and toggle device toolbar to test mobile responsiveness.

## 🎨 Features to Try

- ✅ Upload CSV with drag-and-drop
- ✅ View forecast chart with confidence bands
- ✅ Click "Why?" to see AI explanations
- ✅ Toggle light/dark theme
- ✅ Try chat (graceful fallback if endpoint missing)
- ✅ Export weekly report as Markdown
- ✅ Test on mobile (responsive design)

## 🚢 Production Deployment

See `README.md` for full production deployment instructions using:
- AWS SAM for backend (API Gateway + Lambda)
- Netlify/Vercel/S3 for frontend

## 📚 Documentation

- `README.md` - Full documentation
- `VERIFICATION.md` - Complete verification checklist
- `IMPLEMENTATION_SUMMARY.md` - Technical details

## 🆘 Need Help?

Check the verification checklist in `VERIFICATION.md` for detailed testing steps.

---

**Ready to impress the judges!** 🏆

# Complete Installation Guide

## Step-by-Step Setup for Windows

### Part 1: Install Node.js

#### Option A: Using Official Installer (Recommended)

1. **Download Node.js**
   - Open your web browser
   - Go to: https://nodejs.org/
   - You'll see two versions:
     - **LTS (Long Term Support)** - Recommended for most users
     - **Current** - Latest features
   - Click the **LTS** button to download (e.g., "20.11.0 LTS")

2. **Run the Installer**
   - Open your Downloads folder
   - Double-click the downloaded file (e.g., `node-v20.11.0-x64.msi`)
   - Click "Next" on the welcome screen
   - Accept the license agreement and click "Next"
   - Choose installation location (default is fine) and click "Next"
   - Keep all default features selected and click "Next"
   - Click "Install" (may require administrator permission)
   - Wait for installation to complete
   - Click "Finish"

3. **Verify Installation**
   - Open PowerShell (search for "PowerShell" in Start menu)
   - Type the following commands:
   ```powershell
   node --version
   ```
   - You should see something like: `v20.11.0`
   
   - Then check npm:
   ```powershell
   npm --version
   ```
   - You should see something like: `10.2.4`

   If you see version numbers, Node.js is installed correctly! ✅

#### Option B: Using Chocolatey (Alternative)

If you have Chocolatey package manager installed:

```powershell
# Run PowerShell as Administrator
nof
```

### Part 2: Install Python (Required for Backend)

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Click "Download python 3.12.x" (or latest 3.11 version)

2. **Run the Installer**
   - **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation**
   ```powershell
   python --version
   ```
   - Should show: `python 3.12.x`

   ```powershell
   pip --version
   ```
   - Should show pip version

### Part 3: Install AWS SAM CLI (Required for Backend)

#### Option A: Using MSI Installer (Recommended)

1. **Download AWS SAM CLI**
   - Go to: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
   - Click on "Windows" tab
   - Download the MSI installer (64-bit)

2. **Run the Installer**
   - Double-click the downloaded MSI file
   - Follow the installation wizard
   - Click "Finish"

3. **Verify Installation**
   ```powershell
   sam --version
   ```
   - Should show: `SAM CLI, version 1.x.x`

#### Option B: Using Chocolatey

```powershell
# Run PowerShell as Administrator
choco install aws-sam-cli
```

### Part 4: Install Git (Optional but Recommended)

1. **Download Git**
   - Go to: https://git-scm.com/download/win
   - Download will start automatically

2. **Run the Installer**
   - Use default settings (just keep clicking "Next")
   - Click "Install"
   - Click "Finish"

3. **Verify Installation**
   ```powershell
   git --version
   ```
   - Should show: `git version 2.x.x`

---

## Part 5: Run the Application

### Step 1: Navigate to Project Directory

```powershell
# If you cloned from GitHub:
cd merchant-intelligence-copilot/merchant_intelligence-copilot-files

# If you're already in the project, just navigate to the folder
cd path\to\merchant-intelligence-copilot\merchant_intelligence-copilot-files
```

### Step 2: Start the Backend (Terminal 1)

Open PowerShell and run:

```powershell
# Navigate to backend directory
cd backend

# Build the SAM application
sam build

# This will take 1-2 minutes the first time
# You should see: "Build Succeeded"

# Start the local API server
sam local start-api --port 3000

# Wait for: "Running on http://127.0.0.1:3000"
# Keep this terminal window open!
```

**Expected Output:**
```
Mounting HealthFunction at http://127.0.0.1:3000/health [GET]
Mounting GenerateInsightsFunction at http://127.0.0.1:3000/generate-insights [POST]
You can now browse to the above endpoints to invoke your functions.
```

### Step 3: Start the Frontend (Terminal 2)

Open a **NEW** PowerShell window and run:

```powershell
# Navigate to frontend directory
cd merchant-intelligence-copilot\merchant_intelligence-copilot-files\frontend

# Install dependencies (first time only)
npm install

# This will take 2-3 minutes
# You should see: "added XXX packages"

# Create environment file
copy .env.example .env

# Start the development server
npm run dev

# Wait for: "Local: http://localhost:5173"
```

**Expected Output:**
```
VITE v5.2.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### Step 4: Open the Application

1. Open your web browser (Chrome, Edge, or Firefox)
2. Go to: **http://localhost:5173**
3. You should see the Merchant Intelligence Copilot homepage!

---

## Part 6: Test the Application

### Quick Test Steps:

1. **Check API Status**
   - Look at the top-right corner of the page
   - You should see a green dot with "API Connected"
   - If it's red, make sure the backend is running (Step 2)

2. **Upload Sample Data**
   - Click "Upload Data" in the sidebar
   - Navigate to: `merchant-intelligence-copilot\merchant_intelligence-copilot-files\sample-data\`
   - Drag and drop `msme_sales_90days.csv` into the upload area
   - OR click "Browse Files" and select the file
   - Select a language (English, Hindi, or Marathi)
   - Click "Analyze Data"
   - Wait 10-30 seconds

3. **View Dashboard**
   - You'll be automatically redirected to the Dashboard
   - You should see:
     - 4 KPI cards at the top
     - A product selector dropdown
     - A forecast chart
     - A table with product insights

4. **Try Other Features**
   - Click "Copilot Chat" to ask questions
   - Click "Weekly Report" to see action plan
   - Click "About" to learn more
   - Try the theme toggle (sun/moon icon) in the top-right

---

## Troubleshooting

### Problem: "node is not recognized"

**Solution:**
- Close and reopen PowerShell
- If still not working, restart your computer
- Verify PATH: Go to System Properties → Environment Variables → Check if Node.js is in PATH

### Problem: "sam is not recognized"

**Solution:**
- Close and reopen PowerShell
- Reinstall AWS SAM CLI
- Run PowerShell as Administrator

### Problem: "npm install" fails

**Solution:**
```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules folder
Remove-Item -Recurse -Force node_modules

# Delete package-lock.json
Remove-Item package-lock.json

# Try again
npm install
```

### Problem: Backend won't start

**Solution:**
```powershell
# Make sure you're in the backend directory
cd backend

# Try building with container
sam build --use-container

# If that fails, check Python installation
python --version
```

### Problem: Port 3000 or 5173 already in use

**Solution:**
```powershell
# For backend, use a different port
sam local start-api --port 3001

# Then update frontend .env file:
# VITE_API_BASE_URL=http://127.0.0.1:3001

# For frontend, Vite will automatically use next available port
```

### Problem: "API Not Connected" (red indicator)

**Solution:**
1. Make sure backend is running (Terminal 1)
2. Check if you can access: http://127.0.0.1:3000/health in browser
3. Verify `.env` file has: `VITE_API_BASE_URL=http://127.0.0.1:3000`
4. Restart frontend: Press `Ctrl+C` in Terminal 2, then run `npm run dev` again

### Problem: CSV upload fails

**Solution:**
1. Make sure your CSV has these columns:
   - date
   - product_name
   - quantity_sold
   - price
   - revenue
2. Use the sample file first to test: `sample-data/msme_sales_90days.csv`
3. Check backend terminal for error messages

---

## Quick Reference Commands

### Stop the Application

**Backend (Terminal 1):**
```powershell
# Press Ctrl+C
```

**Frontend (Terminal 2):**
```powershell
# Press Ctrl+C
```

### Restart the Application

**Backend:**
```powershell
cd backend
sam local start-api --port 3000
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

### Update Dependencies

```powershell
cd frontend
npm install
```

---

## File Structure Reference

```
merchant-intelligence-copilot/
└── merchant_intelligence-copilot-files/
    ├── backend/
    │   ├── src/
    │   ├── template.yaml
    │   └── requirements.txt
    ├── frontend/
    │   ├── src/
    │   ├── .env.example
    │   ├── .env (you create this)
    │   ├── package.json
    │   └── vite.config.ts
    └── sample-data/
        └── msme_sales_90days.csv
```

---

## Environment Variables Explained

### Frontend `.env` file:

```env
# Local development (SAM Local)
VITE_API_BASE_URL=http://127.0.0.1:3000

# GitHub repository (optional - shows GitHub icon)
VITE_GITHUB_URL=https://github.com/Riteshraut0116/merchant-intelligence-copilot
```

**For Production:**
```env
# AWS API Gateway URL (after deployment)
VITE_API_BASE_URL=https://abc123.execute-api.ap-south-1.amazonaws.com/prod

VITE_GITHUB_URL=https://github.com/Riteshraut0116/merchant-intelligence-copilot
```

---

## Next Steps

Once everything is running:

1. ✅ Test all features (Dashboard, Upload, Chat, Report, About)
2. ✅ Try theme toggle (light/dark mode)
3. ✅ Test on mobile (browser dev tools → device toolbar)
4. ✅ Upload your own CSV data
5. ✅ Prepare for demo presentation

---

## Production Deployment

See `README.md` for instructions on deploying to AWS:
- Backend: `sam deploy --guided`
- Frontend: Deploy to Netlify, Vercel, or AWS S3

---

## Need More Help?

- Check `QUICKSTART.md` for 5-minute setup
- Check `VERIFICATION.md` for detailed testing checklist
- Check `README.md` for full documentation

---

**You're all set!** 🚀

If you followed all steps, you should now have:
- ✅ Node.js installed
- ✅ Python installed
- ✅ AWS SAM CLI installed
- ✅ Backend running on http://127.0.0.1:3000
- ✅ Frontend running on http://localhost:5173
- ✅ Application accessible in browser

**Happy coding!** 💻

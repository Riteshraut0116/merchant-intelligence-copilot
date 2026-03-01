# PowerShell frontend deployment script to S3
$ErrorActionPreference = "Stop"

# Configuration
$S3_BUCKET = if ($env:S3_BUCKET) { $env:S3_BUCKET } else { "merchant-intelligence-frontend-$(Get-Date -Format 'yyyyMMddHHmmss')" }
$AWS_REGION = "ap-south-1"
$CLOUDFRONT_ID = $env:CLOUDFRONT_ID

Write-Host "🚀 Starting frontend deployment..." -ForegroundColor Green
Write-Host "S3 Bucket: $S3_BUCKET"
Write-Host "Region: $AWS_REGION"

# Check if bucket exists, create if not
try {
    aws s3 ls "s3://$S3_BUCKET" --region $AWS_REGION 2>&1 | Out-Null
    Write-Host "✅ Bucket exists" -ForegroundColor Green
} catch {
    Write-Host "📦 Creating S3 bucket..." -ForegroundColor Cyan
    aws s3 mb "s3://$S3_BUCKET" --region $AWS_REGION
    
    # Enable static website hosting
    aws s3 website "s3://$S3_BUCKET" `
        --index-document index.html `
        --error-document index.html
    
    # Set bucket policy for public read
    $bucketPolicy = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$S3_BUCKET/*"
        }
    ]
}
"@
    $bucketPolicy | Out-File -FilePath "$env:TEMP\bucket-policy.json" -Encoding utf8
    aws s3api put-bucket-policy --bucket $S3_BUCKET --policy "file://$env:TEMP\bucket-policy.json"
    Remove-Item "$env:TEMP\bucket-policy.json"
}

# Build the frontend
Write-Host "🔨 Building frontend..." -ForegroundColor Cyan
npm run build

# Upload to S3
Write-Host "📤 Uploading to S3..." -ForegroundColor Cyan
aws s3 sync dist/ "s3://$S3_BUCKET" `
    --delete `
    --cache-control "public, max-age=31536000" `
    --exclude "index.html"

# Upload index.html with no-cache
aws s3 cp dist/index.html "s3://$S3_BUCKET/index.html" `
    --cache-control "no-cache, no-store, must-revalidate"

# Invalidate CloudFront if ID provided
if ($CLOUDFRONT_ID) {
    Write-Host "🔄 Invalidating CloudFront cache..." -ForegroundColor Cyan
    aws cloudfront create-invalidation `
        --distribution-id $CLOUDFRONT_ID `
        --paths "/*"
}

Write-Host "✅ Frontend deployed successfully!" -ForegroundColor Green
Write-Host "Website URL: http://$S3_BUCKET.s3-website-$AWS_REGION.amazonaws.com"

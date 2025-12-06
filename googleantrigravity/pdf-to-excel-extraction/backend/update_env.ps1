# Update .env file with Gemini API Key
$envFile = ".env"
$geminiKey = "GEMINI_API_KEY=AIzaSyBHGTsWdopPuzmbjNV-WRJP8Cr44rupJjQ"
$geminiModel = "GEMINI_MODEL=gemini-1.5-flash"
$ocrProvider = "OCR_PROVIDER=gemini"

# Read existing .env file
if (Test-Path $envFile) {
    $content = Get-Content $envFile
    
    # Replace or remove OpenAI keys
    $newContent = $content | Where-Object { 
        $_ -notmatch "^OPENAI_API_KEY=" -and 
        $_ -notmatch "^OPENAI_MODEL=" -and
        $_ -notmatch "^GEMINI_API_KEY=" -and 
        $_ -notmatch "^GEMINI_MODEL="
    }
    
    # Add Gemini configuration at the top
    $finalContent = @($geminiKey, $geminiModel) + $newContent
    
    # Update OCR_PROVIDER if it exists
    $finalContent = $finalContent | ForEach-Object {
        if ($_ -match "^OCR_PROVIDER=") {
            $ocrProvider
        }
        else {
            $_
        }
    }
    
    # Write back
    $finalContent | Set-Content $envFile -Encoding UTF8
    Write-Host "Successfully updated .env file with Gemini API configuration" -ForegroundColor Green
}
else {
    # Create from example
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" $envFile
        $content = Get-Content $envFile
        $content = $content -replace "^GEMINI_API_KEY=.*", $geminiKey
        $content = $content -replace "^GEMINI_MODEL=.*", $geminiModel  
        $content = $content -replace "^OCR_PROVIDER=.*", $ocrProvider
        $content | Set-Content $envFile -Encoding UTF8
        Write-Host "Created .env file with Gemini API configuration" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Configuration applied:" -ForegroundColor Cyan
Write-Host "- API Key: AIzaSyBHGT...rupJjQ" -ForegroundColor Yellow
Write-Host "- Model: gemini-1.5-flash" -ForegroundColor Yellow
Write-Host "- Provider: gemini" -ForegroundColor Yellow

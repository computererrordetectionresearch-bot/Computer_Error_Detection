# FILE: tests/run_tests.ps1
# PowerShell test script for Installation Error Fixer API

$API_URL = "http://localhost:5000"

Write-Host "🧪 Running Installation Error Fixer Test Suite" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$API_URL/health" -Method Get
    if ($response.status -eq "ok") {
        Write-Host "✅ PASS: Health check successful" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Health check failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ FAIL: Health check failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Installation Request
Write-Host "Test 2: Installation Request - Adobe Photoshop" -ForegroundColor Yellow
try {
    $body = @{
        text = "I want to install Adobe Photoshop"
        software = "Adobe Photoshop"
        os = "Windows 11"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
    if ($response.type -eq "installation") {
        Write-Host "✅ PASS: Installation request detected" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Installation request not detected" -ForegroundColor Red
        Write-Host "Response: $($response | ConvertTo-Json)"
    }
} catch {
    Write-Host "❌ FAIL: Installation request test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Error Fix - App Closing
Write-Host "Test 3: Error Fix - App Closing" -ForegroundColor Yellow
try {
    $body = @{
        text = "app is closing"
        software = "Adobe Photoshop"
        os = "Windows 11"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
    if ($response.type -eq "error" -and $response.category -like "*Application Crash*") {
        Write-Host "✅ PASS: Error correctly classified" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Error classification failed" -ForegroundColor Red
        Write-Host "Response: $($response | ConvertTo-Json)"
    }
} catch {
    Write-Host "❌ FAIL: Error fix test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 4: Error Fix - Installation Failed
Write-Host "Test 4: Error Fix - Installation Failed" -ForegroundColor Yellow
try {
    $body = @{
        text = "installation failed"
        software = "Visual Studio Code"
        os = "Windows 10"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
    if ($response.type -eq "error" -and $response.category -like "*Installation Failed*") {
        Write-Host "✅ PASS: Installation error correctly classified" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Installation error classification failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ FAIL: Installation error test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 5: Error Fix - Missing DLL
Write-Host "Test 5: Error Fix - Missing DLL" -ForegroundColor Yellow
try {
    $body = @{
        text = "missing dll"
        software = "Node.js"
        os = "Windows 11"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
    if ($response.type -eq "error" -and $response.category -like "*Missing DLL*") {
        Write-Host "✅ PASS: Missing DLL error correctly classified" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Missing DLL error classification failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ FAIL: Missing DLL test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 6: Error Fix - Permission Denied
Write-Host "Test 6: Error Fix - Permission Denied" -ForegroundColor Yellow
try {
    $body = @{
        text = "permission denied"
        software = "Docker"
        os = "Windows 11"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
    if ($response.type -eq "error" -and $response.category -like "*Permission Denied*") {
        Write-Host "✅ PASS: Permission error correctly classified" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Permission error classification failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ FAIL: Permission error test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 7: Error Fix - License Error
Write-Host "Test 7: Error Fix - License Error" -ForegroundColor Yellow
try {
    $body = @{
        text = "license error"
        software = "Adobe Premiere Pro"
        os = "MacOS"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
    if ($response.type -eq "error" -and $response.category -like "*License*") {
        Write-Host "✅ PASS: License error correctly classified" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: License error classification failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ FAIL: License error test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 8: Error Fix - Network Error
Write-Host "Test 8: Error Fix - Network Error" -ForegroundColor Yellow
try {
    $body = @{
        text = "network error"
        software = "Spotify"
        os = "Windows 11"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
    if ($response.type -eq "error" -and $response.category -like "*Network*") {
        Write-Host "✅ PASS: Network error correctly classified" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Network error classification failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ FAIL: Network error test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 9: Feedback Submission
Write-Host "Test 9: Feedback Submission" -ForegroundColor Yellow
try {
    $body = @{
        fix_id = 1
        success = $true
        text = "app is closing"
        software = "Adobe Photoshop"
        os = "Windows 11"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$API_URL/api/feedback" -Method Post -Body $body -ContentType "application/json"
    if ($response.success -eq $true) {
        Write-Host "✅ PASS: Feedback submitted successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ FAIL: Feedback submission failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ FAIL: Feedback submission test failed - $_" -ForegroundColor Red
}
Write-Host ""

# Test 10: Invalid Request
Write-Host "Test 10: Invalid Request - Missing Fields" -ForegroundColor Yellow
try {
    $body = @{
        text = "test"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$API_URL/api/detect" -Method Post -Body $body -ContentType "application/json"
        Write-Host "❌ FAIL: Should have returned error for missing fields" -ForegroundColor Red
    } catch {
        Write-Host "✅ PASS: Missing fields error handled correctly" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ FAIL: Invalid request test failed - $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Test Suite Complete!" -ForegroundColor Cyan
Write-Host ""


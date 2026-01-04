# FILE: tests/run_tests.sh
#!/bin/bash

# Test script for Installation Error Fixer API

API_URL="http://localhost:5000"

echo "🧪 Running Installation Error Fixer Test Suite"
echo "=============================================="
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
response=$(curl -s http://localhost:5000/health)
if [[ $response == *"ok"* ]]; then
    echo "✅ PASS: Health check successful"
else
    echo "❌ FAIL: Health check failed"
fi
echo ""

# Test 2: Installation Request
echo "Test 2: Installation Request - Adobe Photoshop"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"I want to install Adobe Photoshop","software":"Adobe Photoshop","os":"Windows 11"}')
if [[ $response == *"installation"* ]]; then
    echo "✅ PASS: Installation request detected"
else
    echo "❌ FAIL: Installation request not detected"
    echo "Response: $response"
fi
echo ""

# Test 3: Error Fix - App Closing
echo "Test 3: Error Fix - App Closing"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"app is closing","software":"Adobe Photoshop","os":"Windows 11"}')
if [[ $response == *"error"* ]] && [[ $response == *"Application Crash"* ]]; then
    echo "✅ PASS: Error correctly classified"
else
    echo "❌ FAIL: Error classification failed"
    echo "Response: $response"
fi
echo ""

# Test 4: Error Fix - Installation Failed
echo "Test 4: Error Fix - Installation Failed"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"installation failed","software":"Visual Studio Code","os":"Windows 10"}')
if [[ $response == *"error"* ]] && [[ $response == *"Installation Failed"* ]]; then
    echo "✅ PASS: Installation error correctly classified"
else
    echo "❌ FAIL: Installation error classification failed"
    echo "Response: $response"
fi
echo ""

# Test 5: Error Fix - Missing DLL
echo "Test 5: Error Fix - Missing DLL"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"missing dll","software":"Node.js","os":"Windows 11"}')
if [[ $response == *"error"* ]] && [[ $response == *"Missing DLL"* ]]; then
    echo "✅ PASS: Missing DLL error correctly classified"
else
    echo "❌ FAIL: Missing DLL error classification failed"
    echo "Response: $response"
fi
echo ""

# Test 6: Error Fix - Permission Denied
echo "Test 6: Error Fix - Permission Denied"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"permission denied","software":"Docker","os":"Windows 11"}')
if [[ $response == *"error"* ]] && [[ $response == *"Permission Denied"* ]]; then
    echo "✅ PASS: Permission error correctly classified"
else
    echo "❌ FAIL: Permission error classification failed"
    echo "Response: $response"
fi
echo ""

# Test 7: Error Fix - License Error
echo "Test 7: Error Fix - License Error"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"license error","software":"Adobe Premiere Pro","os":"MacOS"}')
if [[ $response == *"error"* ]] && [[ $response == *"License"* ]]; then
    echo "✅ PASS: License error correctly classified"
else
    echo "❌ FAIL: License error classification failed"
    echo "Response: $response"
fi
echo ""

# Test 8: Error Fix - Network Error
echo "Test 8: Error Fix - Network Error"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"network error","software":"Spotify","os":"Windows 11"}')
if [[ $response == *"error"* ]] && [[ $response == *"Network"* ]]; then
    echo "✅ PASS: Network error correctly classified"
else
    echo "❌ FAIL: Network error classification failed"
    echo "Response: $response"
fi
echo ""

# Test 9: Feedback Submission
echo "Test 9: Feedback Submission"
response=$(curl -s -X POST $API_URL/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"fix_id":1,"success":true,"text":"app is closing","software":"Adobe Photoshop","os":"Windows 11"}')
if [[ $response == *"success"* ]] || [[ $response == *"recorded"* ]]; then
    echo "✅ PASS: Feedback submitted successfully"
else
    echo "❌ FAIL: Feedback submission failed"
    echo "Response: $response"
fi
echo ""

# Test 10: Invalid Request (Missing Fields)
echo "Test 10: Invalid Request - Missing Fields"
response=$(curl -s -X POST $API_URL/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text":"test"}')
if [[ $response == *"error"* ]] && [[ $response == *"Missing"* ]]; then
    echo "✅ PASS: Missing fields error handled correctly"
else
    echo "❌ FAIL: Missing fields error not handled"
    echo "Response: $response"
fi
echo ""

echo "=============================================="
echo "Test Suite Complete!"
echo ""


#!/bin/bash

# Shorten a URL
echo "Testing URL shortening..."
RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"url":"https://www.example.com/very/long/url/that/needs/shortening"}' http://localhost:5000/shorten)
echo "Response: $RESPONSE"

# Extract the short code from the response
SHORT_CODE=$(echo $RESPONSE | grep -o '"short_code":"[^"]*"' | cut -d'"' -f4)

if [ -z "$SHORT_CODE" ]; then
    echo "Failed to get a short code."
    exit 1
fi

echo "Got short code: $SHORT_CODE"

# Test the redirection (this will follow the redirect and show the HTML of example.com)
echo "Testing redirection..."
curl -s -L http://localhost:5000/$SHORT_CODE | head -n 5

echo ""
echo "Test completed."
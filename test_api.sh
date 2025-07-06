#!/bin/bash

# Test script for Quantum Hackathon API
# Make sure the server is running before executing this script

API_BASE="http://localhost:8080/api"

echo "🚀 Testing Quantum Hackathon API"
echo "================================="

# Test API health
echo "📡 Testing API health..."
curl -s "$API_BASE/../hello" && echo -e "\n"

# Create test users
echo "👤 Creating test users..."

USER1_RESPONSE=$(curl -s -X POST "$API_BASE/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_quantum",
    "email": "alice@quantum.dev",
    "fullName": "Alice Johnson",
    "teamName": "Quantum Pioneers",
    "experienceLevel": "Advanced"
  }')

USER1_ID=$(echo $USER1_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Created user Alice with ID: $USER1_ID"

USER2_RESPONSE=$(curl -s -X POST "$API_BASE/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bob_circuits",
    "email": "bob@quantum.dev",
    "fullName": "Bob Smith",
    "teamName": "Circuit Breakers",
    "experienceLevel": "Intermediate"
  }')

USER2_ID=$(echo $USER2_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Created user Bob with ID: $USER2_ID"

echo ""

# Create test experiments
echo "⚛️  Creating test experiments..."

if [ ! -z "$USER1_ID" ]; then
  EXPERIMENT1_RESPONSE=$(curl -s -X POST "$API_BASE/experiments" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"Bell State Preparation\",
      \"circuitType\": \"Entanglement\",
      \"qubitCount\": 2,
      \"gateSequence\": \"H(0), CNOT(0,1)\",
      \"user\": {\"id\": \"$USER1_ID\"}
    }")
  
  EXPERIMENT1_ID=$(echo $EXPERIMENT1_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
  echo "Created Bell State experiment with ID: $EXPERIMENT1_ID"
fi

if [ ! -z "$USER2_ID" ]; then
  EXPERIMENT2_RESPONSE=$(curl -s -X POST "$API_BASE/experiments" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"Single Qubit Rotation\",
      \"circuitType\": \"Single Qubit\",
      \"qubitCount\": 1,
      \"gateSequence\": \"RX(π/2), RY(π/4)\",
      \"user\": {\"id\": \"$USER2_ID\"}
    }")
  
  EXPERIMENT2_ID=$(echo $EXPERIMENT2_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
  echo "Created rotation experiment with ID: $EXPERIMENT2_ID"
fi

echo ""

# Update experiment results
echo "📊 Updating experiment results..."

if [ ! -z "$EXPERIMENT1_ID" ]; then
  curl -s -X PUT "$API_BASE/experiments/$EXPERIMENT1_ID/results" \
    -H "Content-Type: application/json" \
    -d '{
      "measurementResults": "00: 0.501, 11: 0.499",
      "successProbability": 0.95
    }' > /dev/null
  echo "Updated Bell State experiment results"
fi

if [ ! -z "$EXPERIMENT2_ID" ]; then
  curl -s -X PUT "$API_BASE/experiments/$EXPERIMENT2_ID/results" \
    -H "Content-Type: application/json" \
    -d '{
      "measurementResults": "0: 0.7, 1: 0.3",
      "successProbability": 0.88
    }' > /dev/null
  echo "Updated rotation experiment results"
fi

echo ""

# Get all users
echo "👥 All users:"
curl -s "$API_BASE/users" | python3 -m json.tool
echo ""

# Get all experiments
echo "⚗️  All experiments:"
curl -s "$API_BASE/experiments" | python3 -m json.tool
echo ""

# Get statistics
echo "📈 Hackathon statistics:"
curl -s "$API_BASE/stats" | python3 -m json.tool
echo ""

echo "✅ API testing completed!"
echo ""
echo "🌐 You can also view the database at: http://localhost:8080 (phpMyAdmin)"
echo "   Username: quantum_user"
echo "   Password: quantum_password"
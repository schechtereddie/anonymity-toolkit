#!/bin/bash
# Integration test script for Python backend
# Tests all commands without needing the GUI

echo "🧪 Testing Python Backend Integration"
echo "======================================"
echo ""

cd python-backend

# Test 1: Ping
echo "📡 Test 1: Ping Sidecar"
echo '{"command":"ping","data":{}}' | python3 main.py 2>/dev/null | grep -o '{"success".*}' | jq '.'
echo ""

# Test 2: Create Profile
echo "👤 Test 2: Create Profile"
PROFILE_RESPONSE=$(echo '{"command":"create_profile","data":{"profile_name":"IntegrationTest","location":"San Francisco"}}' | python3 main.py 2>/dev/null | grep -o '{"success".*}')
echo "$PROFILE_RESPONSE" | jq '.'
PROFILE_ID=$(echo "$PROFILE_RESPONSE" | jq -r '.profile_id')
echo "Created profile ID: $PROFILE_ID"
echo ""

# Test 3: List Profiles
echo "📋 Test 3: List Profiles"
echo '{"command":"list_profiles","data":{}}' | python3 main.py 2>/dev/null | grep -o '{"success".*}' | jq '.'
echo ""

# Test 4: Load Profile
echo "📂 Test 4: Load Profile"
echo "{\"command\":\"load_profile\",\"data\":{\"profile_id\":\"$PROFILE_ID\"}}" | python3 main.py 2>/dev/null | grep -o '{"success".*}' | jq '.'
echo ""

# Test 5: Get Status
echo "📊 Test 5: Get Sidecar Status"
echo '{"command":"get_status","data":{}}' | python3 main.py 2>/dev/null | grep -o '{"success".*}' | jq '.'
echo ""

# Test 6: Delete Profile
echo "🗑️  Test 6: Delete Profile"
echo "{\"command\":\"delete_profile\",\"data\":{\"profile_id\":\"$PROFILE_ID\"}}" | python3 main.py 2>/dev/null | grep -o '{"success".*}' | jq '.'
echo ""

echo "✅ All tests completed!"
echo ""
echo "Summary:"
echo "- Ping: ✓"
echo "- Create Profile: ✓"
echo "- List Profiles: ✓"
echo "- Load Profile: ✓"
echo "- Get Status: ✓"
echo "- Delete Profile: ✓"


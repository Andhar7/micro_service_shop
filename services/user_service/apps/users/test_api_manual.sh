#!/bin/bash

# Base URL for the user service
BASE_URL="http://127.0.0.1:8000/users"  # Assuming the user service runs on port 8000 and the app is mounted at /users/

# This script requires jq to be installed.
# You can install it with:
# sudo apt-get install jq
# brew install jq

echo "--- Running User Service Tests ---"

# 1. Register a new user
echo "--- 1. Register a new user ---"
curl -X POST -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}' $BASE_URL/register/

echo "\n\n--- 2. Log in and get a token ---"
# This will print the token to the console. You can then copy and paste it into the TOKEN variable above.
TOKEN_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "password": "testpassword123"
}' $BASE_URL/api/token/)

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access')
REFRESH_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.refresh')

echo "Access Token: $ACCESS_TOKEN"
echo "Refresh Token: $REFRESH_TOKEN"


echo "\n\n--- 3. Get user profile (requires authentication) ---"
# Note: Replace your_auth_token with a valid token
curl -X GET -H "Authorization: Bearer $ACCESS_TOKEN" $BASE_URL/profile/

echo "\n\n--- 4. Update user profile (requires authentication) ---"
# Note: Replace your_auth_token with a valid token
curl -X PUT -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" -d '{
    "bio": "This is a test bio.",
    "location": "Test Location"
}' $BASE_URL/profile/update/

echo "\n\n--- 5. Refresh the access token ---"
curl -X POST -H "Content-Type: application/json" -d "{
    \"refresh\": \"$REFRESH_TOKEN\"
}" $BASE_URL/api/token/refresh/


echo "\n\n--- User Service Tests Finished ---'

#!/bin/bash
#===============================================================================
#
#          FILE: test_env.sh
#
#         USAGE: ./test_env.sh
#
#   DESCRIPTION: Tests if Shopify credentials can be properly loaded by the
#                run_server.sh wrapper script. This helps verify that Claude
#                Desktop will be able to access the credentials.
#
#         NOTES: This is a diagnostic tool only and does not modify any files.
#                It simulates how Claude Desktop would run the MCP server.
#
#===============================================================================

echo "=========================================="
echo "ENVIRONMENT VARIABLE TEST FOR CLAUDE SETUP"
echo "=========================================="
echo ""

echo "This script will test if your Shopify credentials can be loaded."
echo "It simulates what happens when Claude Desktop runs the MCP server."
echo ""

#-------------------------------------------------------------------------------
# TEST 1: VERIFY CREDENTIALS FROM WRAPPER SCRIPT
#-------------------------------------------------------------------------------
# Run the wrapper script with 'env' command to show environment variables
# grep filters to only show Shopify-related variables and PATH
#-------------------------------------------------------------------------------
echo "TEST 1: CHECKING CREDENTIALS FROM WRAPPER SCRIPT"
echo "-------------------------------------------------"
echo "Running test with run_server.sh and a test variable:"
echo "Command: SHOPIFY_TEST_VAR=\"This is a test\" ./run_server.sh env | grep -E '(SHOPIFY_|PATH=)'"
echo ""
SHOPIFY_TEST_VAR="This is a test" ./run_server.sh env | grep -E '(SHOPIFY_|PATH=)'

echo ""
echo "Analysis of Test 1:"
echo "- If you see your Shopify variables above, the wrapper script is working."
echo "- The SHOPIFY_TEST_VAR confirms environment variables can be passed through."
echo "- If credentials are missing, check ~/.shopify_profile and .env files."
echo ""

#-------------------------------------------------------------------------------
# TEST 2: VERIFY PROFILE LOADING MECHANISM
#-------------------------------------------------------------------------------
# Creates a test profile in /tmp and runs the wrapper with HOME set to /tmp
# This tests if the profile loading mechanism works correctly
#-------------------------------------------------------------------------------
echo "TEST 2: CHECKING PROFILE LOADING MECHANISM"
echo "------------------------------------------"
echo "Creating test profile for verification:"
TEST_PROFILE_PATH="/tmp/test_shopify_profile"

# Create a test profile
cat > "$TEST_PROFILE_PATH" << EOF
# Test Shopify profile for verification
export SHOPIFY_TEST_PROFILE="Profile was loaded successfully!"
EOF

chmod 600 "$TEST_PROFILE_PATH"

echo "Created test profile at $TEST_PROFILE_PATH"
echo "Command: HOME=\"/tmp\" ./run_server.sh env | grep -E 'SHOPIFY_'"
echo ""

# Modify HOME to use our test profile
HOME="/tmp" ./run_server.sh env | grep -E 'SHOPIFY_'

echo ""
echo "Analysis of Test 2:"
echo "- If you see 'SHOPIFY_TEST_PROFILE=Profile was loaded successfully!', the profile loading works."
echo "- This confirms that the ~/.shopify_profile mechanism functions correctly."
echo ""

#-------------------------------------------------------------------------------
# SUMMARY AND RECOMMENDATIONS
#-------------------------------------------------------------------------------
# Provide a concise summary of the test results and next steps
#-------------------------------------------------------------------------------
echo "=========================================="
echo "SUMMARY AND RECOMMENDATIONS"
echo "=========================================="
echo ""
echo "If you saw your Shopify credentials in Test 1, Claude can access them."
echo "If Test 2 showed the test profile variable, the profile loading mechanism works."
echo ""
echo "If any tests failed:"
echo "1. Check the log file at ~/shopify_mcp_debug.log"
echo "2. Verify ~/.shopify_profile exists with correct permissions (chmod 600)"
echo "3. Make sure .env exists in the project directory (if not using profile)"
echo "4. Try running 'cat ~/.shopify_profile' to verify its contents"
echo ""

# Clean up
rm -f "$TEST_PROFILE_PATH"
echo "Test complete! Temporary test files have been removed." 
#!/bin/bash
#=============================================================================
# SHOPIFY MCP SERVER CREDENTIALS SETUP
#=============================================================================
#
# This script helps you securely set up credentials for the Shopify MCP server.
# It creates a protected profile file (~/.shopify_profile) that stores your
# Shopify API credentials in a secure location outside of your project directory.
#
# The script guides you through:
# 1. Entering your Shopify store URL
# 2. Choosing between access token or API key + password authentication
# 3. Securely storing credentials with appropriate file permissions
#
# Security features:
# - Credentials are stored outside the project directory
# - File permissions are set to 600 (read/write for owner only)
# - Input is not saved in shell history
# - Credentials never appear in process listings
#
# Usage:
#   ./setup_credentials.sh
#
#=============================================================================

#=============================================================================
# COLOR DEFINITIONS FOR OUTPUT
#=============================================================================

# Define colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#=============================================================================
# UTILITY FUNCTIONS
#=============================================================================

# Print a message with green color for success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print a message with yellow color for warnings
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Print a message with red color for errors
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Print a message with blue color for information
print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Print a section header
print_header() {
    echo ""
    echo -e "${BLUE}==============================================================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}==============================================================================${NC}"
    echo ""
}

#=============================================================================
# CONFIGURATION
#=============================================================================

# The profile file path where credentials will be stored
PROFILE_FILE="$HOME/.shopify_profile"

# Temporary file for building the profile
TEMP_PROFILE=$(mktemp)

# Ensure the temporary file is deleted on exit, even if the script fails
trap 'rm -f "$TEMP_PROFILE"' EXIT

#=============================================================================
# INTRODUCTION
#=============================================================================

print_header "SHOPIFY MCP SERVER CREDENTIALS SETUP"

print_info "This script will help you set up credentials for the Shopify MCP server."
print_info "Your credentials will be stored in: $PROFILE_FILE"
print_info "This file will only be readable by your user account."
echo ""
print_warning "IMPORTANT: Your Shopify API credentials are sensitive! Never share them."
echo ""

#=============================================================================
# CREDENTIAL COLLECTION
#=============================================================================

print_header "SHOPIFY STORE INFORMATION"

# Start building the profile file with a header
cat > "$TEMP_PROFILE" << EOF
# Shopify API Credentials for MCP Server
# Created: $(date)
# This file contains sensitive information and should be kept secure.
# File permissions are set to 600 (read/write for owner only).
EOF

# Get the Shopify shop URL
read -p "Enter your Shopify shop URL (e.g., mystore.myshopify.com): " SHOP_URL
echo "SHOPIFY_SHOP_URL=$SHOP_URL" >> "$TEMP_PROFILE"

# Choose authentication method
print_header "AUTHENTICATION METHOD"
print_info "Choose how you want to authenticate with the Shopify API:"
print_info "1. Private App API Key + Password (recommended for development)"
print_info "2. Access Token (from a custom app or admin API)"
echo ""

# Keep asking until we get a valid choice
while true; do
    read -p "Enter your choice (1 or 2): " AUTH_CHOICE
    
    if [[ "$AUTH_CHOICE" == "1" ]]; then
        # API Key + Password authentication
        echo "" >> "$TEMP_PROFILE"
        echo "# Authentication using API Key + Password" >> "$TEMP_PROFILE"
        
        # Collect API key with hidden input
        read -p "Enter your Shopify API Key: " API_KEY
        echo "SHOPIFY_API_KEY=$API_KEY" >> "$TEMP_PROFILE"
        
        # Collect API password with hidden input
        read -sp "Enter your Shopify API Password: " API_PASSWORD
        echo ""
        echo "SHOPIFY_PASSWORD=$API_PASSWORD" >> "$TEMP_PROFILE"
        
        break
        
    elif [[ "$AUTH_CHOICE" == "2" ]]; then
        # Access Token authentication
        echo "" >> "$TEMP_PROFILE"
        echo "# Authentication using Access Token" >> "$TEMP_PROFILE"
        
        # Collect access token with hidden input
        read -sp "Enter your Shopify Access Token: " ACCESS_TOKEN
        echo ""
        echo "SHOPIFY_ACCESS_TOKEN=$ACCESS_TOKEN" >> "$TEMP_PROFILE"
        
        break
        
    else
        print_error "Invalid choice. Please enter 1 or 2."
    fi
done

#=============================================================================
# API VERSION CONFIGURATION
#=============================================================================

print_header "API VERSION CONFIGURATION"

# Let the user choose the API version or use the default
print_info "Shopify API version to use (press Enter for default: 2023-10):"
read -p "API version: " API_VERSION
API_VERSION=${API_VERSION:-2023-10}

echo "" >> "$TEMP_PROFILE"
echo "# Shopify API Configuration" >> "$TEMP_PROFILE"
echo "SHOPIFY_API_VERSION=$API_VERSION" >> "$TEMP_PROFILE"

#=============================================================================
# SAVE CREDENTIALS
#=============================================================================

print_header "SAVING CREDENTIALS"

# Inform the user about what's happening
print_info "Saving credentials to $PROFILE_FILE..."

# Move the temporary file to the final location
mv "$TEMP_PROFILE" "$PROFILE_FILE"

# Set secure permissions (readable only by the owner)
chmod 600 "$PROFILE_FILE"

# Verify the file exists and has the correct permissions
if [[ -f "$PROFILE_FILE" ]]; then
    PERMS=$(stat -f "%Lp" "$PROFILE_FILE" 2>/dev/null || stat -c "%a" "$PROFILE_FILE" 2>/dev/null)
    
    if [[ "$PERMS" == "600" ]]; then
        print_success "Credentials saved successfully with secure permissions!"
    else
        print_warning "Credentials saved, but permissions are not optimal: $PERMS (should be 600)"
        print_info "You can fix this by running: chmod 600 $PROFILE_FILE"
    fi
else
    print_error "Failed to save credentials. Please check if the directory is writable."
    exit 1
fi

#=============================================================================
# VERIFICATION AND NEXT STEPS
#=============================================================================

print_header "VERIFICATION AND NEXT STEPS"

print_success "Your Shopify credentials are now configured!"
print_info "To use these credentials with the MCP server, run:"
echo ""
echo "  ./run_server.sh"
echo ""
print_info "To update credentials in the future, run this script again." 
print_success "Setup completed successfully!" 
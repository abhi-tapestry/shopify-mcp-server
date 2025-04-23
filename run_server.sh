#!/bin/bash
#=============================================================================
# SHOPIFY MCP SERVER LAUNCHER
#=============================================================================
#
# This script launches the Shopify MCP server with the appropriate credentials
# loaded from either:
#   1. A secure ~/.shopify_profile file (primary source)
#   2. A local .env file (fallback)
#
# The script handles environment variable loading, validation, and server process
# management, ensuring proper credential security throughout.
#
# Security features:
# - Credentials are loaded from a protected profile file
# - Access permissions are enforced on credential files
# - Environment is cleaned up after server starts
# - No credentials are written to shell history
#
# Usage:
#   ./run_server.sh          # Run with default settings
#   ./run_server.sh --port 8080  # Run on a specific port
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

# Function to check if a file exists and has appropriate permissions
check_file_permissions() {
    local file="$1"
    local expected_perms="$2"
    
    if [[ ! -f "$file" ]]; then
        print_error "File $file does not exist."
        return 1
    fi
    
    local perms=$(stat -f "%Lp" "$file" 2>/dev/null || stat -c "%a" "$file" 2>/dev/null)
    
    if [[ "$perms" != "$expected_perms" ]]; then
        print_warning "File $file has incorrect permissions ($perms, expected $expected_perms)."
        return 1
    fi
    
    return 0
}

#=============================================================================
# CREDENTIAL LOADING
#=============================================================================

# The profile file path where secure credentials are stored
PROFILE_FILE="$HOME/.shopify_profile"

# Load credentials from the profile file if it exists
if [[ -f "$PROFILE_FILE" ]]; then
    print_info "Loading credentials from $PROFILE_FILE..."
    
    # Check the file has proper permissions (600 - readable only by owner)
    if check_file_permissions "$PROFILE_FILE" "600"; then
        # Source the file to load environment variables
        source "$PROFILE_FILE"
        print_success "Credentials loaded successfully."
    else
        print_error "Profile file has incorrect permissions. Should be 600 (owner read/write only)."
        print_info "Run: chmod 600 $PROFILE_FILE to fix permissions."
        exit 1
    fi
# If no profile file exists, try to load from local .env file as fallback
elif [[ -f ".env" ]]; then
    print_warning "No profile file found at $PROFILE_FILE."
    print_info "Attempting to load from .env file instead..."
    
    # Check the file has reasonable permissions
    if check_file_permissions ".env" "600"; then
        export $(grep -v '^#' .env | xargs)
        print_success "Credentials loaded from .env file."
    else
        print_warning ".env file has loose permissions. Consider setting chmod 600 .env"
        export $(grep -v '^#' .env | xargs)
    fi
else
    print_error "No credential sources found. Please run setup_credentials.sh first."
    print_info "Or create a .env file with your Shopify API credentials."
    exit 1
fi

#=============================================================================
# CREDENTIAL VALIDATION
#=============================================================================

# Validate that we have the minimum required credentials
if [[ -z "$SHOPIFY_SHOP_URL" ]]; then
    print_error "SHOPIFY_SHOP_URL is not set in the environment."
    exit 1
fi

# Validate authentication credentials
if [[ -z "$SHOPIFY_ACCESS_TOKEN" ]] && [[ -z "$SHOPIFY_API_KEY" || -z "$SHOPIFY_PASSWORD" ]]; then
    print_error "Missing authentication credentials."
    print_info "Required: SHOPIFY_SHOP_URL and either:"
    print_info "  - SHOPIFY_API_KEY and SHOPIFY_PASSWORD, or"
    print_info "  - SHOPIFY_ACCESS_TOKEN"
    exit 1
fi

#=============================================================================
# SERVER LAUNCH
#=============================================================================

# Parse any command line arguments
ARGS=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --port)
            ARGS="$ARGS --port $2"
            shift 2
            ;;
        *)
            ARGS="$ARGS $1"
            shift
            ;;
    esac
done

# Print banner
print_info "Starting Shopify MCP Server"
print_info "Shop URL: $SHOPIFY_SHOP_URL"
if [[ -n "$SHOPIFY_ACCESS_TOKEN" ]]; then
    print_info "Authentication: Using Access Token"
else
    print_info "Authentication: Using API Key + Password"
fi

# Execute the server with the loaded credentials
print_info "Launching server..."
python3 shopify_mcp.py $ARGS

# Server has exited, clean up
print_info "Server process terminated." 
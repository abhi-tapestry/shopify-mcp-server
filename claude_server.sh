#!/bin/bash

# Change to the directory where this script is located
cd "$(dirname "$0")"

# Read credentials from .env file
if [[ -f ".env" ]]; then
    echo "Loading credentials from .env file..." >&2
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found. Please create it with your Shopify credentials." >&2
    exit 1
fi

# Validate that required environment variables are set
if [[ -z "$SHOPIFY_SHOP_URL" ]]; then
    echo "Error: SHOPIFY_SHOP_URL is not set in the .env file." >&2
    exit 1
fi

if [[ -z "$SHOPIFY_ACCESS_TOKEN" ]] && [[ -z "$SHOPIFY_API_KEY" || -z "$SHOPIFY_PASSWORD" ]]; then
    echo "Error: Missing authentication credentials in .env file." >&2
    exit 1
fi

# Print some info
echo "Starting Shopify MCP Server" >&2
echo "Shop URL: $SHOPIFY_SHOP_URL" >&2

# Activate the virtual environment where the MCP package is installed
source .venv-py312/bin/activate

# Run the MCP server
python shopify_mcp_fastmcp.py 
# Setting up Shopify MCP Server with Claude Desktop

This guide provides instructions for setting up the Shopify MCP (Model Context Protocol) server to work with Claude Desktop.

## Prerequisites

- Python 3.12 or later
- A Shopify store with API access
- Claude Desktop installed on your computer

## Configuration

1. **Set up your environment variables**

   The server requires Shopify API credentials to function. You can set these up in two ways:

   a. Create a `.env` file in the project root with the following variables:
   ```
   SHOPIFY_SHOP_URL="your-store-name.myshopify.com"
   SHOPIFY_API_KEY="your-api-key"
   SHOPIFY_PASSWORD="your-api-password"
   SHOPIFY_ACCESS_TOKEN="your-access-token"
   ```

   b. Or use the `setup_credentials.sh` script to create a secure profile:
   ```bash
   ./setup_credentials.sh
   ```

2. **Install required packages**

   Make sure you have all required packages installed in your Python environment:
   ```bash
   source .venv-py312/bin/activate
   pip install shopify mcp
   ```

## Running the server

To start the Shopify MCP server:

```bash
./claude_server.sh
```

The server will start and listen for MCP protocol requests on the standard input/output streams.

## Claude Desktop Configuration

1. Open Claude Desktop and go to Settings

2. Configure the Shopify MCP Server:
   - Path: `/Users/yourusername/shopify-mcp-server/claude_server.sh`
   - Working Directory: `/Users/yourusername/shopify-mcp-server`

3. Save the configuration

## Troubleshooting

- **Environment Variables**: Make sure your Shopify API credentials are correctly set
- **File Permissions**: Ensure that `claude_server.sh` and `shopify_mcp_fastmcp.py` are executable (`chmod +x` if needed)
- **Python Environment**: Verify that you have the right version of Python with all required packages

## Available Tools

The Shopify MCP server provides several tools for Claude to use:

- `get_products`: Retrieve a list of products from your store
- `get_product_details`: Get detailed information about a specific product
- `get_customers`: Retrieve a list of customers
- `get_customer_details`: Get detailed information about a specific customer
- `get_orders`: Retrieve a list of orders
- `search_products`: Search for products by name, type, or vendor
- `get_store_info`: Get information about your Shopify store

## Security Considerations

- Keep your Shopify API credentials confidential
- Do not share your `.env` file or profile credentials
- Consider setting the permissions on your credential files to be readable only by you
- This server is read-only and cannot modify your Shopify store data 
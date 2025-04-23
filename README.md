# Shopify MCP Server for Claude

A Model Context Protocol (MCP) server that enables Claude and other MCP-compatible AI assistants to interact with your Shopify store data. This integration allows AI assistants to directly access product catalogs, customer information, and order details, providing more accurate and contextual assistance for e-commerce tasks.

<p align="center">
  <img src="https://github.com/anthropics/mcp/raw/main/docs/assets/mcp-logo.png" alt="MCP Logo" width="150">
</p>

## 🌟 Features

- **Product Management**
  - Retrieve complete product catalog with titles, descriptions, and pricing
  - Access variant information including SKUs and inventory levels
  - View product images and metadata

- **Customer Insights**
  - Access customer profiles with contact information
  - View customer purchase history and addresses
  - Track total spent and order counts

- **Order Processing**
  - Retrieve order details including line items and totals
  - Access shipping information and fulfillment status
  - View financial status and payment information

- **Search Capabilities**
  - Search products by title, vendor, or product type
  - Filter results based on specific criteria

- **Store Information**
  - Access store metadata, currency, and timezone information
  - Retrieve shop owner and contact details

## 📋 Prerequisites

- Python 3.10 or higher (Python 3.12 recommended)
- A Shopify store with API access credentials (Admin API access)
- [Claude Desktop](https://claude.ai/desktop) or any MCP-compatible AI assistant
- Basic understanding of terminal commands

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/shopify-mcp-server.git
cd shopify-mcp-server
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install ShopifyAPI python-dotenv
```

### 4. Configure Shopify Credentials

You have two options for configuring your Shopify API credentials:

#### Option A: Using the .env file (quickest setup)

Create a `.env` file in the project root:

```
SHOPIFY_SHOP_URL=your-store.myshopify.com
SHOPIFY_API_KEY=your_api_key_here
SHOPIFY_PASSWORD=your_private_app_password_here
```

Or if using an access token:

```
SHOPIFY_SHOP_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token_here
```

#### Option B: Using a secure profile (recommended for production)

Run the setup script which will guide you through the process:

```bash
chmod +x setup_credentials.sh
./setup_credentials.sh
```

This creates a secure `~/.shopify_profile` file with restricted permissions.

### 5. Test Your Configuration

Verify your setup by running:

```bash
chmod +x test_env.sh
./test_env.sh
```

This checks if your credentials are properly loaded and accessible.

### 6. Start the Server

Make the server script executable and run it:

```bash
chmod +x shopify_mcp.py
chmod +x run_server.sh
./run_server.sh
```

By default, the server runs on port 8080. To use a different port:

```bash
./run_server.sh --port 8888
```

## 🔧 Configuring Claude Desktop

To add the Shopify MCP server to Claude Desktop:

1. Open Claude Desktop's configuration file:
   ```bash
   # macOS
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add the following Shopify configuration to your existing `mcpServers` section:

   ```json
   {
     "mcpServers": {
       "shopify": {
         "command": "/Users/your-username/shopify-mcp-server/run_server.sh",
         "workingDir": "/Users/your-username/shopify-mcp-server"
       }
     }
   }
   ```
   
   Important notes:
   - Replace `/Users/your-username/` with the actual path to your project
   - If you already have other MCP servers configured, just add the "shopify" entry to your existing "mcpServers" object
   - The configuration above assumes you're using the default port (8080)

3. Restart Claude Desktop to apply the changes

4. In the Claude Desktop app, you should now see Shopify tools available for use

## 🛠️ Available MCP Tools

The server exposes the following MCP tools to Claude:

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `get_product_list` | Retrieves a list of products | `limit`: Maximum number of products (default: 10) |
| `get_customer_list` | Retrieves a list of customers | `limit`: Maximum number of customers (default: 10) |
| `get_order_list` | Retrieves a list of orders | `limit`: Maximum number of orders (default: 10) |
| `search_products` | Searches for products | `query`: Search term for products |
| `get_store_info` | Retrieves store information | None |

## 🔍 API Endpoints

The server also exposes REST API endpoints that can be accessed directly:

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/health` | GET | Health check for the server | None |
| `/api/products` | GET | Get list of products | `limit`: Number of products |
| `/api/customers` | GET | Get list of customers | `limit`: Number of customers |
| `/api/orders` | GET | Get list of orders | `limit`: Number of orders |
| `/api/search` | GET | Search for products | `q`: Search query |
| `/api/store` | GET | Get store information | None |
| `/mcp` | POST | MCP protocol endpoint | JSON body with method and params |

## 🔒 Security Best Practices

- **Credential Protection**: API credentials are stored with restricted file permissions (600)
- **No Plaintext in Config**: The wrapper script loads credentials at runtime
- **Minimal Access**: Configure your Shopify API access with the least privileges needed
- **Local Only**: By default, the server listens only on localhost for security
- **Regular Rotation**: Periodically rotate your API keys and tokens

## ❓ Troubleshooting

### Common Issues

1. **Credentials Not Loading**
   - Verify credentials exist in `.env` or `~/.shopify_profile`
   - Check permissions on profile file: `ls -la ~/.shopify_profile`
   - Run `./test_env.sh` to diagnose credential issues

2. **Connection Errors**
   - Verify your Shopify URL is correct
   - Ensure API keys are valid and have sufficient permissions
   - Check if your IP is allowed in Shopify API settings

3. **Claude Desktop Integration**
   - Ensure the path in `claude_desktop_config.json` is absolute and correct
   - Verify Claude Desktop has been restarted after changes
   - Check that the server scripts are executable

### Debug Mode

To run the server with verbose output:

```bash
DEBUG=1 ./run_server.sh
```

## 🧠 How Claude Uses This Server

Claude can use this server to:

1. Look up product information when helping customers with product questions
2. Access customer order history to provide personalized recommendations
3. Review inventory levels when discussing product availability
4. Search for products matching specific criteria
5. Get store information for contextual understanding

Example prompt for Claude:

> "Use the Shopify tools to find all products from vendor 'Acme', and then summarize their price range and average inventory level."

## 🏗️ Project Structure

- `shopify_mcp.py` - Main MCP server implementation
- `run_server.sh` - Wrapper script for loading credentials and starting the server
- `setup_credentials.sh` - Helper script for secure credential configuration
- `test_env.sh` - Diagnostic tool for verifying environment setup
- `.env.example` - Example environment variables file

## 🌐 Technical Details

- **MCP Protocol**: Implements the [Model Context Protocol](https://github.com/anthropics/mcp) specification
- **ShopifyAPI**: Uses the [Shopify Python API](https://github.com/Shopify/shopify_python_api) for authenticated access
- **HTTP Server**: Built on Python's stdlib http.server module
- **Security**: Implements credential isolation and permission restrictions

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📬 Contact

If you have any questions or need help with setup, please open an issue on the GitHub repository.

---

<p align="center">
  Made with ❤️ for Claude and Shopify enthusiasts
</p>

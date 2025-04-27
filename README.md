# Python Shopify MCP Server for Claude

A Python implementation of the Model Context Protocol (MCP) server that enables Claude AI to seamlessly interact with your Shopify store data. With this integration, Claude can access product catalogs, customer information, and order details, providing more intelligent and contextual assistance for e-commerce tasks.

<p align="center">
  <img src="https://avatars.githubusercontent.com/u/182288589?s=200&v=4" alt="MCP Logo" width="150">
</p>

## 🌟 Features

- **Seamless Claude Integration**
  - Access your Shopify store data directly within Claude conversations
  - No need to copy-paste data or switch between applications
  - Claude can analyze and reason about your store information

- **Complete Product Access**
  - Query your entire product catalog
  - Access detailed product information, variants, and inventory
  - Search products by title, vendor, or product type

- **Customer Insights**
  - Retrieve customer profiles and purchase history
  - Access contact information and shipping addresses
  - View spending patterns and order frequency

- **Order Management**
  - Access order details, line items, and fulfillment status
  - View payment information and shipping details
  - Analyze order metrics and patterns

- **Store Information**
  - Access metadata about your Shopify store
  - View currency, locale, and timezone settings
  - Retrieve shop owner and business details

## 📋 Prerequisites

- Python 3.10 or higher (Python 3.12 recommended)
- A Shopify store with Admin API access credentials
- [Claude Desktop](https://claude.ai/desktop) installed
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
python -m venv .venv-py312

# Activate on macOS/Linux
source .venv-py312/bin/activate

# Activate on Windows
.venv-py312\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install ShopifyAPI fastmcp python-dotenv
```

### 4. Configure Shopify Credentials

Create a `.env` file in the project root:

```
SHOPIFY_SHOP_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token_here
```

Or for API key authentication:

```
SHOPIFY_SHOP_URL=your-store.myshopify.com
SHOPIFY_API_KEY=your_api_key_here
SHOPIFY_PASSWORD=your_private_app_password_here
```

Alternatively, you can use the setup script for a more secure configuration:

```bash
chmod +x setup_credentials.sh
./setup_credentials.sh
```

### 5. Test Your Configuration

Verify your setup by running:

```bash
chmod +x test_env.sh
./test_env.sh
```

### 6. Make the Server Executable

```bash
chmod +x claude_server.sh
```

## 🔧 Configuring Claude Desktop

To add the Shopify MCP server to Claude Desktop:

1. Open Claude Desktop and click on the settings icon

2. In the MCP settings section, add a new server with these settings:
   - Name: Shopify Store
   - Command: /full/path/to/shopify-mcp-server/claude_server.sh
   - Working Directory: /full/path/to/shopify-mcp-server

   Make sure to replace `/full/path/to/` with your actual file path.

3. Save the configuration and restart Claude Desktop

4. Claude should now have access to your Shopify store data!

## 🧠 Using Shopify Tools with Claude

Once configured, you can ask Claude to use the Shopify tools in your conversations. Here are some examples:

- "Show me the top 5 products in my store"
- "Find all customers who have spent more than $100"
- "Search for products made by vendor X"
- "Get details about my recent orders"
- "What's the average price of products in my catalog?"

Claude will access your Shopify data through the MCP server and provide insightful responses based on your actual store information.

## 🔒 Security Best Practices

- **Credential Protection**: Store API credentials with restricted file permissions (600)
- **Read-Only Access**: The MCP server only retrieves data and cannot modify your store
- **Minimal Access**: Configure your Shopify API access with the least privileges needed
- **Local Only**: The server runs locally on your machine for maximum security
- **Credential Rotation**: Periodically rotate your API keys and tokens

## ❓ Troubleshooting

If you encounter issues with the Shopify MCP server:

1. **Check your credentials**
   - Verify your Shopify API credentials are correct in your `.env` file
   - Make sure your shop URL is properly formatted (e.g., `your-store.myshopify.com`)

2. **Verify Claude Desktop configuration**
   - Ensure paths in the Claude Desktop settings are absolute and correct
   - Check that the working directory is properly set
   - Restart Claude Desktop after making configuration changes

3. **Check server execution**
   - Make sure `claude_server.sh` is executable
   - If you encounter permission issues, run `chmod +x claude_server.sh`

For more detailed setup information, refer to the [CLAUDE_SETUP.md](CLAUDE_SETUP.md) file.

## 📚 Available MCP Tools

The Shopify MCP server provides Claude with the following capabilities:

| Tool | Description |
|------|-------------|
| `get_products` | Retrieve a list of products from your Shopify store |
| `get_product_details` | Get detailed information about a specific product |
| `get_customers` | Retrieve a list of customers from your store |
| `get_customer_details` | Get detailed information about a specific customer |
| `get_orders` | Retrieve a list of orders from your store |
| `search_products` | Search for products by name, type, or vendor |
| `get_store_info` | Get information about your Shopify store |

## 🏗️ Project Structure

- `shopify_mcp_fastmcp.py` - Main Python MCP server implementation using FastMCP
- `claude_server.sh` - Bash script that launches the Python MCP server for Claude
- `setup_credentials.sh` - Helper script for secure credential configuration
- `test_env.sh` - Diagnostic tool for verifying environment setup
- `.env.example` - Example environment variables file
- `CLAUDE_SETUP.md` - Detailed setup instructions for Claude Desktop

## 🧪 Technology Stack

- **Python**: Core implementation language (3.10+ compatible, 3.12 recommended)
- **FastMCP**: Python library for efficient MCP implementation
- **Shopify API**: Official Python client for Shopify API integration
- **Python-dotenv**: For secure environment variable management

## 🌐 Learning More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Documentation](https://claude.ai/docs/desktop)
- [Shopify API Documentation](https://shopify.dev/docs/api)
- [FastMCP Python Library](https://github.com/anthropics/mcp/tree/main/python)

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

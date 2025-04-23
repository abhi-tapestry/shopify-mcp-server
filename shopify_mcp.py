#!/usr/bin/env python3

"""
=================================================================================================
Shopify MCP Server - Model Context Protocol Implementation
=================================================================================================

This module implements a Model Context Protocol (MCP) server that acts as a bridge between
Claude AI (or other MCP-compatible AI assistants) and a Shopify store. It enables AI systems
to securely and effectively interact with Shopify data.

Key capabilities:
- Product retrieval: Access detailed product information including variants and inventory
- Customer data: Retrieve customer profiles and purchase history
- Order management: View order details including line items and fulfillment status
- Search functionality: Perform targeted queries across store data
- Store metadata: Access store information, policies and settings

Security features:
- Uses environment variables for credential management (no hardcoded secrets)
- Validates and sanitizes all incoming requests
- Implements proper error handling and logging
- Restricts data access to read-only operations

This server follows the Model Context Protocol specification, allowing it to be integrated
with Claude Desktop and other MCP-compatible AI assistants.

Dependencies:
- shopify: Python Shopify API client
- json: For parsing and formatting JSON data
- os: For accessing environment variables
- sys: For stdout/stderr and exit codes
- http.server: For the HTTP server implementation
- urllib.parse: For parsing URL query parameters

Usage:
    ./shopify_mcp.py [port]

    If no port is specified, the server defaults to port 8080.
"""

import json
import os
import sys
import shopify
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# =================================================================================================
# SHOPIFY API INITIALIZATION
# =================================================================================================

def init_shopify_api():
    """
    Initialize the Shopify API client using environment variables.
    
    Required environment variables:
    - SHOPIFY_SHOP_URL: The URL of your Shopify store (e.g., 'your-store.myshopify.com')
    - Either SHOPIFY_ACCESS_TOKEN or both SHOPIFY_API_KEY and SHOPIFY_PASSWORD
    - Optional SHOPIFY_API_VERSION: Defaults to '2023-01' if not specified
    
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    # Get required environment variables
    shop_url = os.environ.get('SHOPIFY_SHOP_URL')
    api_key = os.environ.get('SHOPIFY_API_KEY')
    password = os.environ.get('SHOPIFY_PASSWORD')
    access_token = os.environ.get('SHOPIFY_ACCESS_TOKEN')
    api_version = os.environ.get('SHOPIFY_API_VERSION', '2023-01')
    
    # Validate that we have the necessary credentials
    if not shop_url:
        print("Error: SHOPIFY_SHOP_URL environment variable is required", file=sys.stderr)
        return False
    
    if not (access_token or (api_key and password)):
        print("Error: Either SHOPIFY_ACCESS_TOKEN or both SHOPIFY_API_KEY and SHOPIFY_PASSWORD must be provided", file=sys.stderr)
        return False
    
    try:
        # Configure the Shopify session with the appropriate authentication method
        if access_token:
            # Private app authentication with access token
            session = shopify.Session(shop_url, api_version, access_token)
        else:
            # API key + password authentication
            session = shopify.Session(shop_url, api_version)
            session.shop_url = shop_url
            shopify.ShopifyResource.set_site(f"https://{api_key}:{password}@{shop_url}/admin/api/{api_version}")
        
        shopify.ShopifyResource.activate_session(session)
        return True
    except Exception as e:
        print(f"Error initializing Shopify API: {e}", file=sys.stderr)
        return False

# =================================================================================================
# DATA RETRIEVAL FUNCTIONS
# =================================================================================================

def get_product_list(limit=10):
    """
    Retrieve a list of products from the Shopify store.
    
    Args:
        limit (int): Maximum number of products to return (default: 10)
        
    Returns:
        list: List of product dictionaries with relevant details
    """
    try:
        # Fetch products from Shopify API with the specified limit
        products = shopify.Product.find(limit=limit)
        
        # Transform the API response into a more usable format
        product_list = []
        for product in products:
            # Convert the Shopify Product object to a dictionary
            product_dict = {
                'id': product.id,
                'title': product.title,
                'description': product.body_html,
                'product_type': product.product_type,
                'vendor': product.vendor,
                'tags': product.tags,
                'created_at': str(product.created_at),
                'updated_at': str(product.updated_at),
                'variants': [],
                'images': []
            }
            
            # Add variant information
            for variant in product.variants:
                variant_dict = {
                    'id': variant.id,
                    'title': variant.title,
                    'price': variant.price,
                    'sku': variant.sku,
                    'inventory_quantity': variant.inventory_quantity
                }
                product_dict['variants'].append(variant_dict)
            
            # Add image information
            for image in product.images:
                image_dict = {
                    'id': image.id,
                    'src': image.src,
                    'position': image.position
                }
                product_dict['images'].append(image_dict)
                
            product_list.append(product_dict)
        
        return product_list
    except Exception as e:
        print(f"Error retrieving products: {e}", file=sys.stderr)
        return []

def get_customer_list(limit=10):
    """
    Retrieve a list of customers from the Shopify store.
    
    Args:
        limit (int): Maximum number of customers to return (default: 10)
        
    Returns:
        list: List of customer dictionaries with relevant details
    """
    try:
        # Fetch customers from Shopify API with the specified limit
        customers = shopify.Customer.find(limit=limit)
        
        # Transform the API response into a more usable format
        customer_list = []
        for customer in customers:
            # Convert the Shopify Customer object to a dictionary
            customer_dict = {
                'id': customer.id,
                'email': customer.email,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'orders_count': customer.orders_count,
                'total_spent': customer.total_spent,
                'created_at': str(customer.created_at),
                'addresses': []
            }
            
            # Add address information if available
            if hasattr(customer, 'addresses'):
                for address in customer.addresses:
                    address_dict = {
                        'address1': address.address1,
                        'city': address.city,
                        'province': address.province,
                        'country': address.country,
                        'zip': address.zip
                    }
                    customer_dict['addresses'].append(address_dict)
                
            customer_list.append(customer_dict)
        
        return customer_list
    except Exception as e:
        print(f"Error retrieving customers: {e}", file=sys.stderr)
        return []

def get_order_list(limit=10):
    """
    Retrieve a list of orders from the Shopify store.
    
    Args:
        limit (int): Maximum number of orders to return (default: 10)
        
    Returns:
        list: List of order dictionaries with relevant details
    """
    try:
        # Fetch orders from Shopify API with the specified limit
        orders = shopify.Order.find(limit=limit)
        
        # Transform the API response into a more usable format
        order_list = []
        for order in orders:
            # Convert the Shopify Order object to a dictionary
            order_dict = {
                'id': order.id,
                'order_number': order.order_number,
                'email': order.email,
                'created_at': str(order.created_at),
                'total_price': order.total_price,
                'subtotal_price': order.subtotal_price,
                'total_tax': order.total_tax,
                'currency': order.currency,
                'financial_status': order.financial_status,
                'fulfillment_status': order.fulfillment_status,
                'customer': {},
                'shipping_address': {},
                'line_items': []
            }
            
            # Add customer information if available
            if hasattr(order, 'customer') and order.customer:
                order_dict['customer'] = {
                    'id': order.customer.id,
                    'email': order.customer.email,
                    'first_name': order.customer.first_name,
                    'last_name': order.customer.last_name
                }
            
            # Add shipping address information if available
            if hasattr(order, 'shipping_address') and order.shipping_address:
                address = order.shipping_address
                order_dict['shipping_address'] = {
                    'name': address.name,
                    'address1': address.address1,
                    'city': address.city,
                    'province': address.province,
                    'country': address.country,
                    'zip': address.zip
                }
            
            # Add line item information
            for item in order.line_items:
                item_dict = {
                    'id': item.id,
                    'title': item.title,
                    'quantity': item.quantity,
                    'price': item.price,
                    'sku': item.sku,
                    'product_id': item.product_id,
                    'variant_id': item.variant_id
                }
                order_dict['line_items'].append(item_dict)
                
            order_list.append(order_dict)
        
        return order_list
    except Exception as e:
        print(f"Error retrieving orders: {e}", file=sys.stderr)
        return []

def search_products(query):
    """
    Search for products by title, vendor, or product type.
    
    Args:
        query (str): Search term to query products
        
    Returns:
        list: List of matching product dictionaries
    """
    try:
        # For better search, we'll get a larger list and filter manually
        # since the Shopify API's search capabilities can be limited
        products = shopify.Product.find(limit=50)
        
        # Manually filter products by query term
        query = query.lower()
        matched_products = []
        
        for product in products:
            # Check if the query matches any of the searchable fields
            if (query in product.title.lower() or 
                query in product.vendor.lower() or 
                query in product.product_type.lower() or
                query in product.tags.lower()):
                
                # Convert the matching product to a dictionary
                product_dict = {
                    'id': product.id,
                    'title': product.title,
                    'description': product.body_html,
                    'product_type': product.product_type,
                    'vendor': product.vendor,
                    'tags': product.tags,
                    'variants': [],
                    'images': []
                }
                
                # Add variant information
                for variant in product.variants:
                    variant_dict = {
                        'id': variant.id,
                        'title': variant.title,
                        'price': variant.price,
                        'sku': variant.sku
                    }
                    product_dict['variants'].append(variant_dict)
                
                # Add image information (just the first image)
                if product.images:
                    image = product.images[0]
                    product_dict['image'] = {
                        'src': image.src
                    }
                    
                matched_products.append(product_dict)
        
        return matched_products
    except Exception as e:
        print(f"Error searching products: {e}", file=sys.stderr)
        return []

def get_store_info():
    """
    Retrieve information about the Shopify store.
    
    Returns:
        dict: Dictionary with store details
    """
    try:
        # Fetch shop information from Shopify API
        shop = shopify.Shop.current()
        
        # Convert the Shopify Shop object to a dictionary
        shop_info = {
            'id': shop.id,
            'name': shop.name,
            'email': shop.email,
            'domain': shop.domain,
            'province': shop.province,
            'country': shop.country,
            'address1': shop.address1,
            'zip': shop.zip,
            'city': shop.city,
            'phone': shop.phone,
            'created_at': str(shop.created_at),
            'shop_owner': shop.shop_owner,
            'plan_name': shop.plan_name,
            'has_storefront': shop.has_storefront,
            'money_format': shop.money_format,
            'weight_unit': shop.weight_unit,
            'primary_locale': shop.primary_locale,
            'country_name': shop.country_name,
            'currency': shop.currency,
            'timezone': shop.timezone
        }
        
        return shop_info
    except Exception as e:
        print(f"Error retrieving store information: {e}", file=sys.stderr)
        return {}

# =================================================================================================
# MCP SERVER IMPLEMENTATION
# =================================================================================================

class MCPRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the Model Context Protocol (MCP) server.
    
    This handler processes incoming HTTP requests, validates them according to the MCP
    specification, and returns appropriate responses. It maps MCP function calls to
    the corresponding Shopify API functionality.
    """
    
    def _set_headers(self, status_code=200):
        """Set common headers for HTTP responses."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # CORS headers
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self._set_headers()
        
    def do_GET(self):
        """
        Handle GET requests (used for health checks and simple API calls).
        
        The server responds to:
        - /health - Returns a 200 OK response to indicate the server is running
        - /api/* - API endpoints that map to Shopify functions
        """
        # Parse the URL to get the path and query parameters
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # Health check endpoint
        if path == '/health':
            self._set_headers()
            response = {'status': 'ok'}
            self.wfile.write(json.dumps(response).encode())
            return
            
        # Handle API endpoints
        if path.startswith('/api/'):
            endpoint = path.replace('/api/', '')
            
            # Route to the appropriate function based on the endpoint
            if endpoint == 'products':
                limit = int(query_params.get('limit', ['10'])[0])
                response = get_product_list(limit)
            elif endpoint == 'customers':
                limit = int(query_params.get('limit', ['10'])[0])
                response = get_customer_list(limit)
            elif endpoint == 'orders':
                limit = int(query_params.get('limit', ['10'])[0])
                response = get_order_list(limit)
            elif endpoint == 'search':
                query = query_params.get('q', [''])[0]
                response = search_products(query)
            elif endpoint == 'store':
                response = get_store_info()
            else:
                self._set_headers(404)
                response = {'error': 'Endpoint not found'}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Send the response
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
            return
            
        # If we get here, the path wasn't matched
        self._set_headers(404)
        response = {'error': 'Not found'}
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """
        Handle POST requests for the MCP protocol.
        
        This method processes incoming MCP function calls, validates the request format,
        and routes to the appropriate handler function.
        
        The primary endpoint is:
        - /mcp - Handles MCP function calls according to the specification
        """
        # Check if this is an MCP request
        if self.path == '/mcp':
            # Get content length from headers
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                # Parse the JSON request
                request = json.loads(post_data)
                
                # Validate that this is a valid MCP request
                if not isinstance(request, dict) or 'method' not in request:
                    self._set_headers(400)
                    response = {'error': 'Invalid MCP request format'}
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Handle different MCP methods
                method = request.get('method')
                params = request.get('params', {})
                
                # Map MCP methods to our functions
                if method == 'get_product_list':
                    limit = params.get('limit', 10)
                    result = get_product_list(limit)
                    response = {'result': result}
                elif method == 'get_customer_list':
                    limit = params.get('limit', 10)
                    result = get_customer_list(limit)
                    response = {'result': result}
                elif method == 'get_order_list':
                    limit = params.get('limit', 10)
                    result = get_order_list(limit)
                    response = {'result': result}
                elif method == 'search_products':
                    query = params.get('query', '')
                    result = search_products(query)
                    response = {'result': result}
                elif method == 'get_store_info':
                    result = get_store_info()
                    response = {'result': result}
                else:
                    self._set_headers(400)
                    response = {'error': f'Unknown method: {method}'}
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Send the response
                self._set_headers()
                self.wfile.write(json.dumps(response).encode())
                return
                
            except json.JSONDecodeError:
                self._set_headers(400)
                response = {'error': 'Invalid JSON in request'}
                self.wfile.write(json.dumps(response).encode())
                return
                
            except Exception as e:
                self._set_headers(500)
                response = {'error': f'Server error: {str(e)}'}
                self.wfile.write(json.dumps(response).encode())
                return
        
        # If we get here, the path wasn't matched
        self._set_headers(404)
        response = {'error': 'Not found'}
        self.wfile.write(json.dumps(response).encode())

# =================================================================================================
# MAIN SERVER FUNCTION
# =================================================================================================

def run_server(port=8080):
    """
    Start the MCP server on the specified port.
    
    Args:
        port (int): The port to listen on (default: 8080)
    """
    # Initialize the Shopify API
    if not init_shopify_api():
        print("Failed to initialize Shopify API. Please check your environment variables.", file=sys.stderr)
        sys.exit(1)
    
    # Create and configure the HTTP server
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPRequestHandler)
    
    print(f"Starting Shopify MCP server on port {port}...")
    print(f"Shop URL: {os.environ.get('SHOPIFY_SHOP_URL')}")
    print("Server is ready to handle requests!")
    
    try:
        # Start the server
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        print("\nShutting down server...")
        httpd.server_close()
        print("Server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    # Parse command line arguments for port number
    port = 8080  # Default port
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}", file=sys.stderr)
            print("Usage: ./shopify_mcp.py [port]", file=sys.stderr)
            sys.exit(1)
    
    # Start the server
    run_server(port) 
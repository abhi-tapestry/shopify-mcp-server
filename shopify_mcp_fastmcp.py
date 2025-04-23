#!/usr/bin/env python3

"""
Shopify MCP Server using FastMCP
This implementation follows the same pattern as the working weather MCP server.
"""

import os
import sys
import shopify
import traceback
import logging
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('shopify_mcp')

# Initialize FastMCP server
mcp = FastMCP("shopify_mcp_server")

# =================================================================================================
# SHOPIFY API INITIALIZATION
# =================================================================================================

def init_shopify_api() -> bool:
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
        logger.error("SHOPIFY_SHOP_URL environment variable is required")
        return False
    
    if not (access_token or (api_key and password)):
        logger.error("Either SHOPIFY_ACCESS_TOKEN or both SHOPIFY_API_KEY and SHOPIFY_PASSWORD must be provided")
        return False
    
    try:
        logger.debug(f"Initializing Shopify API with shop_url={shop_url} and api_version={api_version}")
        
        # Configure the Shopify session with the appropriate authentication method
        if access_token:
            # Private app authentication with access token
            logger.debug("Using access token authentication")
            session = shopify.Session(shop_url, api_version, access_token)
        else:
            # API key + password authentication
            logger.debug("Using API key + password authentication")
            session = shopify.Session(shop_url, api_version)
            session.shop_url = shop_url
            shopify.ShopifyResource.set_site(f"https://{api_key}:{password}@{shop_url}/admin/api/{api_version}")
        
        shopify.ShopifyResource.activate_session(session)
        
        # Test the connection by retrieving the shop information
        shop = shopify.Shop.current()
        logger.debug(f"Successfully connected to Shopify shop: {shop.name}")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing Shopify API: {e}")
        logger.debug(f"Stack trace: {traceback.format_exc()}")
        return False

# =================================================================================================
# MCP TOOL IMPLEMENTATIONS
# =================================================================================================

@mcp.tool()
def get_products(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get a list of products from the Shopify store.
    
    Args:
        limit: Maximum number of products to return (default: 10)
        
    Returns:
        List of product objects with details
    """
    try:
        logger.debug(f"Fetching products with limit={limit}")
        
        # Fetch products from Shopify API with the specified limit (without page parameter)
        products = shopify.Product.find(limit=limit)
        logger.debug(f"Found {len(products)} products")
        
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
        
        logger.debug(f"Processed {len(product_list)} products successfully")
        return product_list
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        logger.debug(f"Stack trace: {traceback.format_exc()}")
        return []

@mcp.tool()
def get_product_details(product_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific product.
    
    Args:
        product_id: The ID of the product to retrieve
        
    Returns:
        Detailed product information
    """
    try:
        product = shopify.Product.find(product_id)
        
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
            
        return product_dict
    except Exception as e:
        logger.error(f"Error retrieving product details: {e}")
        return {}

@mcp.tool()
def get_customers(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get a list of customers from the Shopify store.
    
    Args:
        limit: Maximum number of customers to return (default: 10)
        
    Returns:
        List of customer objects with details
    """
    try:
        logger.debug(f"Fetching customers with limit={limit}")
        
        # Fetch customers from Shopify API with the specified limit
        customers = shopify.Customer.find(limit=limit)
        logger.debug(f"Found {len(customers)} customers")
        
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
        
        logger.debug(f"Processed {len(customer_list)} customers successfully")
        return customer_list
    except Exception as e:
        logger.error(f"Error retrieving customers: {e}")
        logger.debug(f"Stack trace: {traceback.format_exc()}")
        return []

@mcp.tool()
def get_customer_details(customer_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific customer.
    
    Args:
        customer_id: The ID of the customer to retrieve
        
    Returns:
        Detailed customer information
    """
    try:
        customer = shopify.Customer.find(customer_id)
        
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
        
        return customer_dict
    except Exception as e:
        logger.error(f"Error retrieving customer details: {e}")
        return {}

@mcp.tool()
def get_orders(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get a list of orders from the Shopify store.
    
    Args:
        limit: Maximum number of orders to return (default: 10)
        
    Returns:
        List of order objects with details
    """
    try:
        logger.debug(f"Fetching orders with limit={limit}")
        
        # Fetch orders from Shopify API with the specified limit
        orders = shopify.Order.find(limit=limit)
        logger.debug(f"Found {len(orders)} orders")
        
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
        
        logger.debug(f"Processed {len(order_list)} orders successfully")
        return order_list
    except Exception as e:
        logger.error(f"Error retrieving orders: {e}")
        logger.debug(f"Stack trace: {traceback.format_exc()}")
        return []

@mcp.tool()
def search_products(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for products by title, vendor, or product type.
    
    Args:
        query: Search term to query products
        limit: Maximum number of results to return (default: 10)
        
    Returns:
        List of matching products
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
                
                if len(matched_products) >= limit:
                    break
        
        return matched_products
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        return []

@mcp.tool()
def get_store_info() -> Dict[str, Any]:
    """
    Get information about the Shopify store.
    
    Returns:
        Dictionary with store details
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
        logger.error(f"Error retrieving store information: {e}")
        return {}

# =================================================================================================
# MAIN FUNCTION
# =================================================================================================

if __name__ == "__main__":
    # Initialize the Shopify API
    logger.info("Starting Shopify MCP server")
    if not init_shopify_api():
        logger.error("Failed to initialize Shopify API. Please check your environment variables.")
        sys.exit(1)
    
    print("Shopify MCP server is running...", file=sys.stderr)
    logger.debug("Waiting for input...")
    
    try:
        # Run the MCP server with stdio transport (for Claude Desktop)
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        logger.debug(f"Stack trace: {traceback.format_exc()}")
        sys.exit(1) 
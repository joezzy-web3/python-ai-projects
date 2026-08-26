# Create variables representing an item in an online store
product_name = "Wireless Headphones"  # Text (String)
price = 49.99                         # Decimal (Float)
quantity = 3                          # Whole number (Integer)
is_in_stock = True                    # True/False (Boolean)

# Calculate the total cost for the items
total_cost = price * quantity

# Print a clean summary using formatted strings (f-strings)
print("=== Product Details ===")
print(f"Item Name:   {product_name}")
print(f"Unit Price:  ${price}")
print(f"Quantity:    {quantity}")
print(f"In Stock:    {is_in_stock}")
print("-----------------------")
print(f"Total Cost:  ${total_cost}")
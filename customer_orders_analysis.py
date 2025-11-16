"""
Customer Orders Analysis - Source Code

This script defines functions to:
- Create sample data
- Build data structures (customer_orders, category_to_products, etc.)
- Compute totals, classifications, and business insights
- Generate a human-readable text report
"""

# -----------------------------
# 1. Data creation
# -----------------------------

def create_sample_data():
    """Return sample (customer_names, orders)."""
    customer_names = [
        "Alice",
        "Bob",
        "Charlie",
        "Diana",
        "Ethan",
        "Fatima",
        "Grace",
    ]

    # List of order tuples: (customer_name, product, price, category)
    orders = [
        ("Alice",   "Smartphone",       699.99, "Electronics"),
        ("Alice",   "Phone Case",        19.99, "Electronics"),
        ("Alice",   "T-Shirt",           24.99, "Clothing"),
        ("Bob",     "Laptop",          1099.99, "Electronics"),
        ("Bob",     "Desk Lamp",         34.99, "Home Essentials"),
        ("Charlie", "Jeans",             49.99, "Clothing"),
        ("Charlie", "Blender",           59.99, "Home Essentials"),
        ("Diana",   "Vacuum Cleaner",   149.99, "Home Essentials"),
        ("Diana",   "Headphones",        89.99, "Electronics"),
        ("Ethan",   "Coffee Maker",      79.99, "Home Essentials"),
        ("Ethan",   "T-Shirt",           24.99, "Clothing"),
        ("Fatima",  "Smartwatch",       199.99, "Electronics"),
        ("Fatima",  "Dress",             89.99, "Clothing"),
        ("Grace",   "Book",              14.99, "Home Essentials"),
        ("Grace",   "Socks",              9.99, "Clothing"),
    ]

    return customer_names, orders


# -----------------------------
# 2. Core data structures
# -----------------------------

def build_customer_orders(orders):
    """Return dict: customer_name -> list of orders for that customer."""
    customer_orders = {}
    for order in orders:
        name, product, price, category = order
        customer_orders.setdefault(name, []).append(order)
    return customer_orders


def build_product_to_category(orders):
    """Return dict: product -> category."""
    product_to_category = {}
    for _, product, _, category in orders:
        product_to_category[product] = category
    return product_to_category


def get_product_categories(product_to_category):
    """Return set of unique product categories."""
    return set(product_to_category.values())


# -----------------------------
# 3. Customer analysis
# -----------------------------

def calculate_customer_totals(orders):
    """Return dict: customer_name -> total amount spent."""
    totals = {}
    for customer_name, _, price, _ in orders:
        totals[customer_name] = totals.get(customer_name, 0) + price
    return totals


def classify_customer(total_spent):
    """
    Classify customer by total spending:
    > $100   -> High-value
    $50–$100 -> Moderate
    < $50    -> Low-value
    """
    if total_spent > 100:
        return "High-value buyer"
    elif 50 <= total_spent <= 100:
        return "Moderate buyer"
    else:
        return "Low-value buyer"


def get_customer_classes(customer_totals):
    """Return dict: customer_name -> classification string."""
    return {name: classify_customer(total)
            for name, total in customer_totals.items()}


# -----------------------------
# 4. Business insights
# -----------------------------

def compute_category_revenue(orders):
    """Return dict: category -> total revenue."""
    category_revenue = {}
    for _, _, price, category in orders:
        category_revenue[category] = category_revenue.get(category, 0) + price
    return category_revenue


def get_unique_products(orders):
    """Return set of all unique products sold."""
    return {product for _, product, _, _ in orders}


def get_electronics_customers(orders):
    """
    Return a sorted list of unique customers
    who bought 'Electronics' category items.
    """
    return sorted({o[0] for o in orders if o[3] == "Electronics"})


def get_top_n_customers(customer_totals, n=3):
    """Return list of (customer_name, total) sorted by total desc, top n."""
    return sorted(
        customer_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )[:n]


def build_category_to_products(orders):
    """Return dict: category -> set(products)."""
    category_to_products = {}
    for _, product, _, category in orders:
        category_to_products.setdefault(category, set()).add(product)
    return category_to_products


def compute_product_set_operations(category_to_products):
    """
    Example set operations across categories.

    Returns a dict with keys:
        - 'electronics_products'
        - 'clothing_products'
        - 'home_products'
        - 'common_electronics_clothing'
        - 'unique_to_electronics'
    """
    electronics = category_to_products.get("Electronics", set())
    clothing = category_to_products.get("Clothing", set())
    home = category_to_products.get("Home Essentials", set())

    common_electronics_clothing = electronics & clothing
    unique_to_electronics = electronics - (clothing | home)

    return {
        "electronics_products": electronics,
        "clothing_products": clothing,
        "home_products": home,
        "common_electronics_clothing": common_electronics_clothing,
        "unique_to_electronics": unique_to_electronics,
    }


def build_customer_to_categories(orders):
    """Return dict: customer_name -> set(categories they purchased from)."""
    customer_to_categories = {}
    for customer_name, _, _, category in orders:
        customer_to_categories.setdefault(customer_name, set()).add(category)
    return customer_to_categories


def get_multi_category_customers(customer_to_categories):
    """Return set of customers who purchased from more than one category."""
    return {
        name for name, cats in customer_to_categories.items()
        if len(cats) > 1
    }


def get_customers_by_category(customer_to_categories, category):
    """Return set of customers who purchased from a specific category."""
    return {
        name for name, cats in customer_to_categories.items()
        if category in cats
    }


def get_customers_electronics_and_clothing(customer_to_categories):
    """Return set of customers who bought both Electronics and Clothing."""
    electronics_customers = get_customers_by_category(
        customer_to_categories, "Electronics"
    )
    clothing_customers = get_customers_by_category(
        customer_to_categories, "Clothing"
    )
    return electronics_customers & clothing_customers


# -----------------------------
# 5. Convenience: run full analysis
# -----------------------------

def run_full_analysis():
    """
    Run the whole pipeline on the sample data and
    return a dictionary of all useful outputs.
    """
    customer_names, orders = create_sample_data()
    customer_orders = build_customer_orders(orders)
    product_to_category = build_product_to_category(orders)
    product_categories = get_product_categories(product_to_category)

    customer_totals = calculate_customer_totals(orders)
    customer_classes = get_customer_classes(customer_totals)

    category_revenue = compute_category_revenue(orders)
    unique_products = get_unique_products(orders)
    electronics_customers = get_electronics_customers(orders)
    top_three_customers = get_top_n_customers(customer_totals, n=3)

    category_to_products = build_category_to_products(orders)
    product_sets = compute_product_set_operations(category_to_products)

    customer_to_categories = build_customer_to_categories(orders)
    multi_category_customers = get_multi_category_customers(customer_to_categories)
    customers_electronics_and_clothing = get_customers_electronics_and_clothing(
        customer_to_categories
    )

    return {
        "customer_names": customer_names,
        "orders": orders,
        "customer_orders": customer_orders,
        "product_to_category": product_to_category,
        "product_categories": product_categories,
        "customer_totals": customer_totals,
        "customer_classes": customer_classes,
        "category_revenue": category_revenue,
        "unique_products": unique_products,
        "electronics_customers": electronics_customers,
        "top_three_customers": top_three_customers,
        "category_to_products": category_to_products,
        "product_sets": product_sets,
        "customer_to_categories": customer_to_categories,
        "multi_category_customers": multi_category_customers,
        "customers_electronics_and_clothing": customers_electronics_and_clothing,
    }


# -----------------------------
# 6. Text report generator
# -----------------------------

def generate_report(results):
    """
    Generate a detailed, human-readable report summarizing:
      - Customer classifications
      - Total sales per category
      - Key insights about purchase behavior
    """
    customer_classes = results["customer_classes"]
    customer_totals = results["customer_totals"]
    category_revenue = results["category_revenue"]
    electronics_customers = results["electronics_customers"]
    unique_products = results["unique_products"]
    top_three = results["top_three_customers"]
    multi_category_customers = results["multi_category_customers"]
    customers_electronics_and_clothing = results["customers_electronics_and_clothing"]

    report = []
    report.append("Customer Orders Analysis Report")
    report.append("====================================\n")

    report.append("Customer Classification\n-----------------------")
    report.append("High-value buyer: > $100")
    report.append("Moderate buyer: $50–$100")
    report.append("Low-value buyer: < $50\n")
    report.append("Customer Spending & Classification:")
    for name in sorted(customer_totals.keys()):
        report.append(f" - {name}: ${customer_totals[name]:.2f}  ->  {customer_classes[name]}")

    report.append("\nTotal Sales by Category\n------------------------")
    for cat, rev in sorted(category_revenue.items(), key=lambda x: x[0]):
        report.append(f" - {cat}: ${rev:.2f}")

    report.append("\nTop 3 Highest-Spending Customers:")
    for name, total in top_three:
        report.append(f" - {name}: ${total:.2f}")

    report.append("\nCustomers Who Purchased Electronics:")
    if electronics_customers:
        for c in electronics_customers:
            report.append(f" - {c}")
    else:
        report.append(" - None")

    report.append("\nCustomers Purchasing Across Multiple Categories:")
    if multi_category_customers:
        for c in sorted(multi_category_customers):
            report.append(f" - {c}")
    else:
        report.append(" - None")

    report.append("\nCustomers Who Bought BOTH Electronics and Clothing:")
    if customers_electronics_and_clothing:
        for c in sorted(customers_electronics_and_clothing):
            report.append(f" - {c}")
    else:
        report.append(" - None")

    report.append(f"\nNumber of Unique Products Sold: {len(unique_products)}")

    report.append("\nBusiness Interpretation:")
    report.append(
        "Python's core data structures make it easy to compute metrics, "
        "classify customers, and derive insights that support better "
        "business decisions in an e-commerce setting."
    )

    return "\n".join(report)


if __name__ == "__main__":
    # Example usage when running this file directly
    results = run_full_analysis()
    text_report = generate_report(results)
    print(text_report)

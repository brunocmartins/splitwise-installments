import os
import click
from datetime import datetime, timedelta
from splitwise import Splitwise, Expense, Category

API_KEY = os.getenv("API_KEY")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

s = Splitwise(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    api_key=API_KEY
)

def get_available_categories():
    """
    Get all available categories and their subcategories from Splitwise.
    
    Returns:
        dict: A nested dictionary structure where:
            - Keys are category IDs
            - Values are dictionaries containing:
                - 'name': Category name
                - 'subcategories': Dictionary of subcategory IDs and names
    """
    categories = s.getCategories()
    result = {}
    
    for category in categories:
        category_id = category.getId()
        category_name = category.getName()
        
        # Get subcategories
        subcategories = {}
        for subcategory in category.getSubcategories():
            subcategories[subcategory.getId()] = subcategory.getName()
        
        result[category_id] = {
            'name': category_name,
            'subcategories': subcategories
        }
    
    return result

def add_installment(total_amount: float, num_installments: int, description: str, expense_date: str, group_id: int="73326842", category_id: int=None):
    """
    Create installment expenses in Splitwise.
    
    Args:
        total_amount (float): Total amount of the expense
        num_installments (int): Number of installments
        description (str): Description of the expense
        expense_date (str): Date of the expense in YYYY-MM-DD format
        group_id (int): ID of the group where the expense should be created
        category_id (int, optional): ID of the category for the expense
    """
    # group_id = "73326842" # Co-Living
    # group_id = "80044938" # Test
    try:
        # Validate and parse the input date
        expense_date = datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD format")
    
    installment_amount = round(total_amount / num_installments, 2)
    
    # Create installments
    for i in range(num_installments):
        # Calculate due date (first installment is the expense date, then first day of next months)
        if i == 0:
            due_date = expense_date
        else:
            # Get the first day of the next month
            next_month = expense_date.month + i
            next_year = expense_date.year
            if next_month > 12:
                next_month -= 12
                next_year += 1
            due_date = datetime(next_year, next_month, 1)
        
        # Create expense
        expense = Expense()
        expense.setCost(installment_amount)
        expense.setDescription(f"{description} - Installment {i+1}/{num_installments}")
        expense.setDate(due_date.strftime("%Y-%m-%d"))
        expense.setGroupId(group_id)
        expense.setPayment(False)  # Set as group expense, not direct payment
        expense.setSplitEqually(True)  # Split equally among all group members
        
        # Set category if provided
        if category_id:
            category = Category()
            category.setId(category_id)
            expense.setCategory(category)
        
        # Create the expense
        nExpense, errors = s.createExpense(expense)
        if errors:
            print(f"Errors creating expense: {errors}")
        else:
            print(f"Expense created successfully. ID: {nExpense.getId()}")
            print(f"Created expense category: {nExpense.getCategory().getName() if nExpense.getCategory() else 'None'}")


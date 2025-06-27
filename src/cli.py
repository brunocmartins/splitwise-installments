import click
from installment import add_installment, get_available_categories

@click.group()
@click.version_option()
def cli():
    """
    Splitwise
    """
    pass

@cli.command()
@click.option('--amount', type=float, required=True, help='Total amount of the expense')
@click.option('--installments', type=int, required=True, help='Number of installments')
@click.option('--description', type=str, required=True, help='Description of the expense')
@click.option('--date', type=str, required=True, help='Date of the expense in YYYY-MM-DD format')
@click.option('--group-id', type=int, default="73326842", help='ID of the group')
@click.option('--category', type=str, help='Category name for the expense')
@click.option('--subcategory', type=str, help='Subcategory name for the expense')
def add(amount, installments, description, date, group_id, category, subcategory):
    """Create installment expenses in Splitwise."""
    category_id = None
    if category:
        categories = get_available_categories()
        # Find category by name
        category_id = next((cat_id for cat_id, cat_data in categories.items() 
                          if cat_data['name'].lower() == category.lower()), None)
        
        if not category_id:
            available_categories = "\n".join(f"- {cat_data['name']}" 
                                           for cat_data in categories.values())
            raise click.BadParameter(f"Invalid category. Available categories are:\n{available_categories}")
        
        # If subcategory is provided, find its ID
        if subcategory:
            subcategories = categories[category_id]['subcategories']
            category_id = next((sub_id for sub_id, sub_name in subcategories.items() 
                              if sub_name.lower() == subcategory.lower()), None)
            if not category_id:
                available_subcategories = "\n".join(f"- {sub_name}" 
                                                  for sub_name in subcategories.values())
                raise click.BadParameter(f"Invalid subcategory. Available subcategories are:\n{available_subcategories}")
    
    add_installment(amount, installments, description, date, group_id, category_id)

@cli.command()
@click.option('--category', type=str, help='Category name to show details')
def list_categories(category):
    """List all available categories and their subcategories in Splitwise."""
    categories = get_available_categories()
    
    if category:
        # Find category by name
        category_data = next((data for data in categories.values() 
                            if data['name'].lower() == category.lower()), None)
        if category_data:
            click.echo(f"\nCategory: {category_data['name']}")
            click.echo("Subcategories:")
            for sub_id, sub_name in category_data['subcategories'].items():
                click.echo(f"  - {sub_name} (ID: {sub_id})")
        else:
            click.echo(f"Category '{category}' not found.")
    else:
        click.echo("Available categories:")
        for cat_id, cat_data in categories.items():
            click.echo(f"\n{cat_data['name']} (ID: {cat_id})")
            if cat_data['subcategories']:
                click.echo("  Subcategories:")
                for sub_id, sub_name in cat_data['subcategories'].items():
                    click.echo(f"    - {sub_name} (ID: {sub_id})")

if __name__ == '__main__':
    cli()

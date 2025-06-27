from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
from installment import add_installment, get_available_categories
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change-in-production')

@app.route('/', methods=['GET', 'POST'])
def index():
    categories = get_available_categories()
    if request.method == 'POST':
        try:
            # Get form data
            amount = float(request.form['amount'])
            installments = int(request.form['installments'])
            description = request.form['description']
            date = request.form['date']
            group_id = int(request.form.get('group_id', '73326842'))
            category = request.form.get('category')
            subcategory = request.form.get('subcategory')

            # Validate date format
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD', 'error')
                return redirect(url_for('index'))

            # Process category and subcategory
            category_id = None
            if category:
                category_id = next((cat_id for cat_id, cat_data in categories.items() 
                                  if cat_data['name'].lower() == category.lower()), None)
                
                if not category_id:
                    flash('Invalid category selected', 'error')
                    return redirect(url_for('index'))
                
                if subcategory:
                    subcategories = categories[category_id]['subcategories']
                    category_id = next((sub_id for sub_id, sub_name in subcategories.items() 
                                      if sub_name.lower() == subcategory.lower()), None)
                    if not category_id:
                        flash('Invalid subcategory selected', 'error')
                        return redirect(url_for('index'))

            # Add the installment
            add_installment(amount, installments, description, date, group_id, category_id)
            flash('Installment added successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('index'))

    return render_template('index.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True) 
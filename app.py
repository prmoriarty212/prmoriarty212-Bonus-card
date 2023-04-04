import csv
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Session
from flask import make_response
from io import StringIO

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

# Define the database model
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    card_number = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    bonus_points = db.Column(db.Integer)
    birthdate = db.Column(db.String(100))

    # convert object to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'card_number': self.card_number,
            'phone_number': self.phone_number,
            'bonus_points': self.bonus_points,
            'birthdate': self.birthdate
        }

# Index route
@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle POST request
    if request.method == 'POST':
        # Get form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']        
        phone_number = request.form['phoneNumber']
        bonus_points = request.form['bonusPoints']
        birthdate = request.form['birthdate']
        card_number = request.form['cardNumber']
        
        # Convert birthdate to date object
        birthdate_object = datetime.strptime(birthdate, '%Y-%m-%d').date()

        # Add data to database
        data = FormData(first_name, last_name, card_number, phone_number, int(bonus_points), birthdate_object)
        db.session.add(data)
        db.session.commit()

        # Redirect to index
        return redirect(url_for('index'))

    # Get all FormData
    data = FormData.query.all()

    # Render index page with data
    return render_template('index.html', data=data)

# Update record route
@app.route('/update_record', methods=['PUT'])
def update_record():

    # Get JSON data from request
    data = request.get_json()
    record_id = data['id']
    record = FormData.query.get(record_id)

    # Print record before update
    print("Record before update:", record.to_dict())

    # Update record
    record.first_name = data['first_name']
    record.last_name = data['last_name']
    record.card_number = data['card_number']
    record.phone_number = data['phone_number']
    record.bonus_points = data['bonus_points']
    record.birthdate = data['birthdate']

    # Commit changes to database
    db.session.commit()

    # Print record after update
    updated_record = FormData.query.get(record_id)
    print("Record after update:", updated_record.to_dict())

    # Return success status
    return jsonify({'status': 'success'})

# Route for fetching all table data as a JSON object
@app.route('/get_table_data', methods=['GET'])
def get_table_data():

    # Fetch all records from the database
    data = FormData.query.all()
    results = []

    # Loop through the fetched records and append them to the results list
    for row in data:
        results.append({
            'id': row.id,
            'first_name': row.first_name,
            'last_name': row.last_name,
            'card_number': row.card_number,
            'phone_number': row.phone_number,
            'bonus_points': row.bonus_points,
            'birthdate': row.birthdate
        })

    # Return the results list as a JSON object
    return jsonify(results)

# Route for exporting the data to a CSV file
@app.route('/export_csv', methods=['GET'])
def export_csv():

    # Fetch all records from the database
    data = FormData.query.all()
    headers = ['id', 'first_name', 'last_name', 'card_number', 'phone_number', 'bonus_points', 'birthdate']
    
    # Function for generating the CSV content
    def generate():
        csv_data = StringIO()
        writer = csv.writer(csv_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)

        # Loop through the fetched records and write them to the CSV file
        for row in data:
            writer.writerow([row.id, row.first_name, row.last_name, row.card_number, "'" + row.phone_number, row.bonus_points, row.birthdate])
        
        csv_data.seek(0)
        return csv_data.getvalue()

    # Create a response object with the generated CSV content and appropriate headers
    response = make_response(generate())
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    response.headers['Content-type'] = 'text/csv; charset=utf-8-sig'

    return response

# Function for creating the tables in the database before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# main entry point for the application
if __name__ == '__main__':
    app.run(debug=True)

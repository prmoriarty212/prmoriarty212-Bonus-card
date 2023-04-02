from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Session


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    card_number = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    bonus_points = db.Column(db.Integer)
    birthdate = db.Column(db.String(100))

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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']        
        phone_number = request.form['phoneNumber']
        bonus_points = request.form['bonusPoints']
        birthdate = request.form['birthdate']
        card_number = request.form['cardNumber']
        
        birthdate_object = datetime.strptime(birthdate, '%Y-%m-%d').date()

        data = FormData(first_name, last_name, card_number, phone_number, int(bonus_points), birthdate_object)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('index'))

    data = FormData.query.all()
    return render_template('index.html', data=data)

@app.route('/update_record', methods=['PUT'])
def update_record():
    data = request.get_json()
    record_id = data['id']
    record = FormData.query.get(record_id)

    print("Record before update:", record.to_dict())

    record.first_name = data['first_name']
    record.last_name = data['last_name']
    record.card_number = data['card_number']
    record.phone_number = data['phone_number']
    record.bonus_points = data['bonus_points']
    record.birthdate = data['birthdate']

    db.session.commit()

    updated_record = FormData.query.get(record_id)
    print("Record after update:", updated_record.to_dict())

    return jsonify({'status': 'success'})

    
@app.route('/get_table_data', methods=['GET'])
def get_table_data():
    data = FormData.query.all()
    results = []

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

    return jsonify(results)





@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

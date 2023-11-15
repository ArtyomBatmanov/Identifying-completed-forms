from datetime import datetime
import re
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('forms.json')


@app.route('/get_form', methods=['POST'])
def get_form():
    form_data = request.form

    for template in db.all():
        template_fields = set(template.keys()) - {'name'}
        form_fields = set(form_data.keys())

        if template_fields.issubset(form_fields):
            matching_fields = True

            for field in template_fields:
                if form_data[field] != template[field]:
                    matching_fields = False
                    break

            if matching_fields:
                return jsonify({'name': template['name']})

    field_types = {}

    for field, value in form_data.items():
        if validate_date(value):
            field_types[field] = 'date'
        elif validate_phone(value):
            field_types[field] = 'phone'
        elif validate_email(value):
            field_types[field] = 'email'
        else:
            field_types[field] = 'text'

    return jsonify(field_types)


def validate_date(date):
    try:
        formats = ['%d.%m.%Y', '%Y-%m-%d']
        for fmt in formats:
            datetime.strptime(date, fmt)
        return True
    except ValueError:
        return False


def validate_phone(phone):
    return re.match(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', phone) is not None


def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None


if __name__ == '__main__':
    app.run()

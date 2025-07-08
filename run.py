from flask import Flask, render_template, request
from app.google_wallet import GenericPass


app = Flask(__name__)


generic_pass = GenericPass()
    
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/user_form')
def show_form():
    return render_template('user_form.html')

@app.route('/add_to_wallet')
def add():
    link = generic_pass.create_pass_object()
    return f'<a href= {link}></a>'


@app.route('/user_form_submitted', methods=['POST']) 
def user_form():
    print('hello')
    data = request.form.to_dict()
    fname = data['fname']
    lname = data['lname']
    company_name = data['company-name']
    ph_number = data['phNumber']
    print(data)
    link = generic_pass.create_pass_object(fname, lname, company_name, ph_number)
    print(link)
   
    return "Form submitted, check you SMS for a link to your pass"


if __name__ == '__main__':
    app.run(debug=True)
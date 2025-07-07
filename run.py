from flask import Flask
from app.google_wallet import GenericPass

app = Flask(__name__)

generic_pass = GenericPass()
    
@app.route('/')
def index():
    generic_pass.create_class()
    return "This is INDEX"


@app.route('/add_to_wallet')
def add():
    link = generic_pass.create_pass_object()
    return f'<a href= {link}></a>'
    
    



if __name__ == '__main__':
    app.run(debug=True)
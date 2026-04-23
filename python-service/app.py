from flask import Flask, request  

#Configurations , Variables ,etc
# WATCH_DIR = '/opt/lampp/htdocs/Watch-Tower-v1' # Note 1 - this config can using .env?  Yes !

app = Flask(__name__)

@app.route('/')
def home(): 
    user_input = request.args.get('input')
    
    return f'You entered : {user_input}'


if __name__ == '__main__':
    app.run(debug=True)

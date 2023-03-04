from flask import Flask, render_template, request, url_for, send_file
from translate import Translator
import langid
import string
import random

app = Flask(__name__)


def translate_EN(string):
    valid = langid.classify(string)
    translator = Translator(to_lang='en')
    output = translator.translate(string)
    return output


def translate_JP(string):
    valid = langid.classify(string)
    translator = Translator(to_lang='ja')
    output = translator.translate(string)
    return output


def translate_FR(string):
    valid = langid.classify(string)
    translator = Translator(to_lang='fr')
    output = translator.translate(string)
    return output


def translate_KO(string):
    valid = langid.classify(string)
    translator = Translator(to_lang='ko')
    output = translator.translate(string)
    return output


def random_password(length):
    alp = string.ascii_letters + string.digits
    password = ''.join(random.choice(alp) for i in range(length))
    return password


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['Email']
        subject = data['Subject']
        message = data['Message']
        name = data['Name']
        file = database.write(
            f'Name:{name},Email:{email},Subject:{subject},Message:{message}\n')
        


def calc(li):
    eq = li['expression']
    return eval(eq)


@app.route('/')
def origin():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/password_generator')
def password_render():
    return render_template('pw_generator.html')


@app.route('/pw_generate', methods=['POST', 'GET'])
def pw_generator():
    if request.method == 'POST':
        length = request.form.to_dict()
        length = length["pw_length"]
        output = random_password(int(length))
        return render_template('pw.html', pw=output)
    else:
        return render_template('error.html')


@app.route('/translate_form', methods=['POST', 'GET'])
def translator():
    if request.method == "POST":
        li = request.form.to_dict()
        original = li["text"]
        if request.form['Translate'] == 'English':
            translated = translate_EN(original)
            return render_template("text.html", original=original, translated=translated)

        elif request.form['Translate'] == 'Japanese':
            translated = translate_JP(original)
            return render_template('text.html', original=original, translated=translated)

        elif request.form['Translate'] == 'French':
            translated = translate_FR(original)
            return render_template('text.html', original=original, translated=translated)

        elif request.form['Translate'] == 'Korean':
            translated = translate_KO(original)
            return render_template('text.html', original=original, translated=translated)

        else:
            return render_template('error.html')
    else:
        return render_template('error.html')


@app.route('/translator')
def translator_render():
    return render_template('translator_template.html')


@app.route('/calculator')
def calculator_render():
    return render_template('calc_template.html')


@app.route('/calc_form', methods=['POST', 'GET'])
def calculator():
    if request.method == 'POST':
        num = request.form.to_dict()
        result = calc(num)
        return render_template('calc_template.html', result=result)
    else:
        return render_template('error.html')


@app.route('/download')
def download_file():
    path = "templates/PyiCV.pdf"
    return send_file(path, as_attachment=True)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_file(data)
        return render_template('contact.html')
    else:
        return render_template('error.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html'), 404


if __name__ == "__main__":
    app.run()

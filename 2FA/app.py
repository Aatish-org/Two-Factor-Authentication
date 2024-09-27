from flask import Flask, render_template, request, redirect, url_for, flash
import pyotp
import qrcode
import io
from PIL import Image
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Generate a random base32 secret for the user
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)

@app.route('/')
def home():
    return render_template('index.html', secret=secret)

@app.route('/setup')
def setup():
    # Generate the provisioning URI
    provisioning_uri = totp.provisioning_uri("2faCSEadmin@protonmail.com", issuer_name="AATISH")

    # Generate the QR code
    qr = qrcode.make(provisioning_uri)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")

    # Convert the QR code image to a base64 string
    qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return render_template('setup.html', qr_code=qr_base64, provisioning_uri=provisioning_uri)

@app.route('/verify', methods=['POST'])
def verify():
    user_code = request.form.get('code')
    if totp.verify(user_code):
        flash("Verification successful!", "success")
    else:
        flash("Invalid code. Please try again.", "error")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

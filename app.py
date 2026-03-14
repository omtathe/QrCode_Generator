from flask import Flask, request, send_file, render_template_string
import qrcode
import io

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
<title>QR Code Generator</title>

<style>
body{
background:#0f0f0f;
color:white;
font-family:Arial;
height:100vh;
display:flex;
justify-content:center;
align-items:center;
margin:0;
}

.container{
text-align:center;
background:#1e1e1e;
padding:40px;
border-radius:12px;
box-shadow:0 0 20px rgba(0,0,0,0.6);
}

h1{
margin-bottom:20px;
}

input{
padding:12px;
width:250px;
border:none;
border-radius:6px;
margin-right:10px;
outline:none;
}

button{
padding:12px 20px;
border:none;
border-radius:6px;
background:#ff2e63;
color:white;
cursor:pointer;
font-weight:bold;
}

button:hover{
background:#ff4f7a;
}
</style>

</head>

<body>

<div class="container">

<h1>QR Code Generator</h1>

<form action="/generate" method="POST">

<input type="text" name="data" placeholder="Enter text or URL" required>

<button type="submit">Generate</button>

</form>

</div>

</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/generate", methods=["POST"])
def generate():

    data = request.form.get("data")

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
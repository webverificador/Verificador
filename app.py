from flask import Flask, render_template_string, request, send_from_directory
import csv
import os

app = Flask(__name__)
CERT_DIR = "certificados"

@app.route("/", methods=["GET", "POST"])
def index():
    certificado = None
    if request.method == "POST":
        folio = request.form["folio"]
        codigo = request.form["codigo"]
        with open("certificados.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["folio"] == folio and row["codigo"] == codigo:
                    certificado = row["nombre_archivo"]
                    break
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Verificación de Certificados</title>
  <style>
    body {
      font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
      background: #fff;
    }
    .container {
      max-width: 500px;
      margin: 100px auto;
      padding: 30px;
      border: 1px solid #ddd;
      border-radius: 6px;
      background: white;
      box-shadow: 0 0 8px rgba(0,0,0,0.05);
    }
    h2 {
      font-size: 18px;
      color: #336699;
      font-weight: 400;
      margin-bottom: 25px;
      text-align: center;
    }
    label {
      display: block;
      margin-bottom: 5px;
      font-weight: 400;
      color: #333;
      text-align: left;
    }
    input[type="text"] {
      width: 100%;
      padding: 8px 10px;
      margin-bottom: 20px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
      font-family: inherit;
    }
    button {
      display: block;
      margin: 0 auto;
      margin-top: 15px;
      padding: 6px 16px;
      font-size: 14px;
      background: linear-gradient(#007bff, #0056b3);
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Verificación de Certificados</h2>
    <form method="POST">
      <label>Folio:</label>
      <input type="text" name="folio" placeholder="Ej: 500588087549" required>
      <label>Código de Verificación:</label>
      <input type="text" name="codigo" placeholder="Ej: 2d2d7b27e5c3" required>
      <button type="submit">Consultar</button>
    </form>
    {% if certificado %}
      <p style="margin-top: 20px; color: green;">Certificado encontrado:</p>
      <iframe src="/ver/{{ certificado }}" width="100%" height="500px"></iframe>
    {% endif %}
  </div>
</body>
</html>
""", certificado=certificado)

@app.route("/ver/<path:filename>")
def ver_pdf(filename):
    return send_from_directory(CERT_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)


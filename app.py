from flask import Flask, request, jsonify, render_template_string, send_from_directory
import os
import csv

app = Flask(__name__)

pagina_html = """
<!DOCTYPE html>
<html lang='es'>
<head>
  <meta charset='UTF-8'>
  <title>Verificación de Certificados</title>
  <style>
    body {
      background-color: #fff;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 500px;
      margin: 100px auto;
      padding: 30px;
      border: 1px solid #ddd;
      border-radius: 10px;
      text-align: center;
    }
    h2 {
      font-size: 24px;
      color: #336699;
      background-color: #f5f5f5;
      padding: 10px;
      border-radius: 6px;
    }
    label {
      display: block;
      text-align: left;
      margin-top: 20px;
      font-weight: bold;
    }
    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      box-sizing: border-box;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    button {
      background-color: #007bff;
      color: white;
      border: none;
      padding: 10px 20px;
      margin-top: 20px;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
    }
    button:hover {
      background-color: #0056b3;
    }
    #respuesta {
      margin-top: 20px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Verificación de Certificados</h2>
    <label for="folio">Folio:</label>
    <input type="text" id="folio" placeholder="Ej: 500004443232">
    
    <label for="codigo">Código de Verificación:</label>
    <input type="text" id="codigo" placeholder="Ej: ABC123">
    
    <button onclick="verificar()">Consultar</button>
    <div id="respuesta"></div>
  </div>

  <script>
    function verificar() {
      const folio = document.getElementById('folio').value.trim();
      const codigo = document.getElementById('codigo').value.trim();
      const respuesta = document.getElementById('respuesta');

      if (!folio || !codigo) {
        respuesta.innerText = 'Debe ingresar el folio y el código.';
        respuesta.style.color = 'red';
        return;
      }

      fetch('/verificar?folio=' + folio + '&codigo=' + codigo)
        .then(res => res.json())
        .then(data => {
          if (data.valido) {
            respuesta.innerHTML = "✅ " + data.mensaje + "<br><a href='" + data.pdf + "' target='_blank'>Descargar certificado PDF</a>";
            respuesta.style.color = 'green';
          } else {
            respuesta.innerText = "❌ " + data.mensaje;
            respuesta.style.color = 'red';
          }
        });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(pagina_html)

@app.route('/verificar')
def verificar():
    folio = request.args.get('folio', '').strip()
    codigo = request.args.get('codigo', '').strip()
    valido = False

    with open('certificados.csv', newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            if fila['folio'] == folio and fila['codigo'] == codigo:
                valido = True
                break

    if valido:
        pdf_path = f'/certificados/{codigo}.pdf'
        if os.path.exists(f'certificados/{codigo}.pdf'):
            return jsonify({"valido": True, "mensaje": f"Folio y código válidos", "pdf": pdf_path})
        else:
            return jsonify({"valido": True, "mensaje": f"Datos válidos, pero no hay PDF disponible", "pdf": "#"})
    else:
        return jsonify({"valido": False, "mensaje": "Folio y/o código no válidos"})

@app.route('/certificados/<path:filename>')
def descargar_pdf(filename):
    return send_from_directory('certificados', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

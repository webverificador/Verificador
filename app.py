from flask import Flask, request, jsonify, render_template_string, send_from_directory
import os

app = Flask(__name__)

pagina_html = """
<!DOCTYPE html>
<html lang='es'>
<head>
  <meta charset='UTF-8'>
  <title>Verificación de Certificados</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #ffffff;
    }
    .contenedor {
      margin: 80px auto;
      max-width: 500px;
      padding: 30px;
      border: 1px solid #ddd;
      border-radius: 10px;
      box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
      text-align: center;
    }
    h2 {
      background-color: #e7f0fa;
      color: #3a6ea5;
      padding: 10px;
      border-radius: 6px;
      font-size: 20px;
    }
    input {
      width: 90%;
      padding: 10px;
      margin: 10px 0;
      font-size: 14px;
    }
    button {
      background-color: #007bff;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 5px;
      font-size: 14px;
      cursor: pointer;
    }
    button:hover {
      background-color: #0056b3;
    }
    #respuesta {
      margin-top: 15px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="contenedor">
    <h2>Verificación de Certificados</h2>
    <div style="text-align: left;">
      <label>Folio:</label><br>
      <input type="text" id="folio" placeholder="Ej: 500004443232"><br>
      <label>Código de Verificación:</label><br>
      <input type="text" id="codigo" placeholder="Ej: 2rR4t56Cv332"><br>
    </div>
    <button onclick="verificar()">Consultar</button>
    <div id="respuesta"></div>
  </div>

  <script>
    function verificar() {
      const codigo = document.getElementById("codigo").value.trim();
      const folio = document.getElementById("folio").value.trim();
      if (!codigo || !folio) {
        document.getElementById("respuesta").innerText = "Debe ingresar folio y código.";
        document.getElementById("respuesta").style.color = "red";
        return;
      }
      fetch(`/verificar?codigo=${codigo}`)
        .then(res => res.json())
        .then(data => {
          const div = document.getElementById("respuesta");
          if (data.valido) {
            div.innerHTML = "✅ " + data.mensaje + "<br><a href='" + data.pdf + "' target='_blank'>Descargar certificado PDF</a>";
            div.style.color = 'green';
          } else {
            div.innerText = "❌ " + data.mensaje;
            div.style.color = 'red';
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
    codigo = request.args.get('codigo', '').strip()
    with open('codigos.txt', 'r') as f:
        codigos_validos = [line.strip() for line in f.readlines()]
    if codigo in codigos_validos:
        pdf_path = f'/certificados/{codigo}.pdf'
        if os.path.exists(f'certificados/{codigo}.pdf'):
            return jsonify({"valido": True, "mensaje": f"Código {codigo} válido", "pdf": pdf_path})
        else:
            return jsonify({"valido": True, "mensaje": f"Código {codigo} válido, pero no hay PDF disponible", "pdf": "#"})
    else:
        return jsonify({"valido": False, "mensaje": f"Código {codigo} no encontrado"})

@app.route('/certificados/<path:filename>')
def descargar_pdf(filename):
    return send_from_directory('certificados', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

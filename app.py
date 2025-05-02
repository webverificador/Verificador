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
    body { background-color: #fff; font-family: Arial, sans-serif; margin: 0; padding: 0; }
    .container {
      max-width: 500px;
      margin: 100px auto;
      padding: 20px 30px;
      border: 1px solid #ddd;
      border-radius: 6px;
      text-align: center;
      background: white;
      box-shadow: 0 0 8px rgba(0,0,0,0.05);
    }
      max-width: 500px;
      margin: 100px auto;
      padding: 30px;
      border: 1px solid #ddd;
      border-radius: 10px;
      text-align: center;
    }
    h2 {
      font-size: 18px;
      color: #336699;
      font-weight: 400;
      margin-bottom: 20px;
    }
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
    button:hover { background-color: #0056b3; }

    #modal {
      display: none;
      position: fixed;
      z-index: 999;
      left: 0; top: 0;
      width: 100%; height: 100%;
      background: rgba(0,0,0,0.5);
    }
    .modal-content {
      background: white;
      margin: 3% 0 3% 3%;
      padding: 0;
      width: 45%;
      max-width: 950px;
      border-radius: 10px;
      overflow: hidden;
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: white;
      padding: 8px 16px;
      border-bottom: 1px solid #ccc;
      font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
      font-size: 14px;
      font-weight: 400;
      color: #0066cc;
      box-shadow: none;
    }
    .mensaje-validacion {
      flex: 1;
      text-align: left;
      font-size: 14px;
      font-weight: 400;
      color: #0066cc;
    }
    .check {
      font-size: 12px;
      color: #999;
      margin-left: 4px;
    }
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #ccc;
      padding: 10px 16px;
    }
    .mensaje-validacion {
      font-size: 15px;
      font-weight: 400;
      color: #0066cc;
    }
    .check {
      font-size: 13px;
      color: #888;
      margin-left: 6px;
    }
      background-color: white;
      color: #0066cc;
      font-weight: bold;
      padding: 15px;
      font-size: 16px;
      border-bottom: 1px solid #ccc;
      text-align: center;
    }
    .close {
      float: right;
      font-size: 24px;
      cursor: pointer;
      margin-right: 10px;
      color: #666;
    }
    iframe {
      width: 100%;
      height: 600px;
      border: none;
    }
  
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
</head>
<body>
  <div class="container">
    <h2>Verificación de Certificados</h2>
    <label for="folio">Folio:</label>
    <input type="text" id="folio" placeholder="Ej: 500588087549">
    <label for="codigo">Código de Verificación:</label>
    <input type="text" id="codigo" placeholder="Ej: 2d2d7b27e5c3">
    <button onclick="verificar()">Consultar</button>
    <div id="respuesta"></div>
  </div>

  <!-- Modal -->
  <div id="modal">
    <div class="modal-content">
      <div class="modal-header">
        <span class="close" onclick="cerrarModal()">&times;</span>
        <span class="mensaje-validacion">El certificado es válido, verifique los datos en el documento generado.</span><span class="check">✔</span> ✔
      </div>
      <iframe id="visor-pdf" src=""></iframe>
    </div>
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
            document.getElementById('visor-pdf').src = data.pdf;
            document.getElementById('modal').style.display = 'block';
          } else {
            respuesta.innerText = "❌ " + data.mensaje;
            respuesta.style.color = 'red';
          }
        });
    }

    function cerrarModal() {
      document.getElementById('modal').style.display = 'none';
      document.getElementById('visor-pdf').src = "";
    }

    window.onclick = function(event) {
      const modal = document.getElementById('modal');
      if (event.target === modal) cerrarModal();
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
            return jsonify({"valido": True, "mensaje": "Datos válidos", "pdf": pdf_path})
        else:
            return jsonify({"valido": True, "mensaje": "Datos válidos, pero no hay PDF", "pdf": "#"})
    else:
        return jsonify({"valido": False, "mensaje": "Folio y/o código incorrectos"})

@app.route('/certificados/<path:filename>')
def descargar_pdf(filename):
    return send_from_directory('certificados', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

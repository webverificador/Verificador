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
    body { margin: 0; font-family: 'Helvetica', 'Arial', sans-serif; background-color: #f4f4f4; }
    header { background-color: #0033a0; color: white; padding: 20px; text-align: center; }
    .contenedor {
      background-color: white; max-width: 500px; margin: 50px auto; padding: 30px;
      border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); text-align: center;
    }
    h2 { color: #0033a0; }
    input { padding: 10px; width: 100%; margin-bottom: 10px; font-size: 16px; }
    button {
      background-color: #0033a0; color: white; border: none; padding: 10px 20px;
      font-size: 16px; cursor: pointer; border-radius: 5px;
    }
    button:hover { background-color: #002070; }
    #respuesta { margin-top: 20px; font-weight: bold; font-size: 16px; }
  </style>
</head>
<body>
  <header><h1>Gobierno de Chile – Registro de Verificación</h1></header>
  <div class='contenedor'>
    <h2>Verificación de Certificados</h2>
    <input type='text' id='codigo' placeholder='Ingrese código del certificado'>
    <button onclick='verificar()'>Verificar</button>
    <div id='respuesta'></div>
  </div>
  <script>
    function verificar() {
      const codigo = document.getElementById('codigo').value.trim();
      if (!codigo) {
        document.getElementById('respuesta').innerText = 'Debe ingresar un código.';
        document.getElementById('respuesta').style.color = 'red';
        return;
      }
      fetch('/verificar?codigo=' + codigo)
        .then(res => res.json())
        .then(data => {
          const div = document.getElementById('respuesta');
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
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

pagina_html = '''
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Verificador</title>
  <style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
    input { padding: 10px; width: 250px; }
    button { padding: 10px 20px; margin-top: 10px; }
    #respuesta { margin-top: 20px; font-weight: bold; }
  </style>
</head>
<body>
  <h2>Verificación de Certificados</h2>
  <input type="text" id="codigo" placeholder="Ingrese código">
  <br>
  <button onclick="verificar()">Verificar</button>
  <div id="respuesta"></div>

  <script>
    function verificar() {
      const codigo = document.getElementById("codigo").value;
      fetch("/verificar?codigo=" + codigo)
        .then(res => res.json())
        .then(data => {
          const div = document.getElementById("respuesta");
          div.innerText = data.mensaje;
          div.style.color = data.valido ? "green" : "red";
        });
    }
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(pagina_html)

@app.route('/verificar')
def verificar():
    codigo = request.args.get('codigo', '').strip()
    with open('codigos.txt', 'r') as f:
        codigos_validos = [line.strip() for line in f.readlines()]
    if codigo in codigos_validos:
        return jsonify({"valido": True, "mensaje": f"✅ Código {codigo} válido"})
    else:
        return jsonify({"valido": False, "mensaje": f"❌ Código {codigo} no encontrado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

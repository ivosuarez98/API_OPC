from flask import Flask, send_file

app = Flask(__name__)

@app.route('/descargar_texto')
def descargar_texto():
    ruta_archivo = 'C:\\Users\\isuarez\\Documents\\TRABAJO PY\\API_OPC\\HolaMundo.txt'
    nombre_archivo_descarga = 'texto_descargado.txt'
    return send_file(ruta_archivo, as_attachment=True, download_name=nombre_archivo_descarga)

if __name__ == '__main__':

    # Escucha en todas las interfaces de red
    app.run(host='192.168.0.81', port=5000, debug=True)
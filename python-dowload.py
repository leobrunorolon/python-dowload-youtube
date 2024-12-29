from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__)

# Definir la ruta de la carpeta de descargas
downloads_folder = os.path.join(os.getcwd(), 'descargas')

# Crear la carpeta de descargas si no existe
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

@app.route('/')
def home():
    # Esto servirá el archivo index.html desde la carpeta 'templates'
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    link = data.get('link')
    
    if not link:
        return jsonify({"success": False, "message": "No se proporcionó ningún enlace."}), 400

    # Establecer la ruta de salida en la carpeta 'descargas'
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return jsonify({"success": True, "message": "Descarga completa"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

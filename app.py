from flask import Flask, jsonify, request, render_template, send_from_directory
import chromadb
from chromadb.config import Settings
import librosa 
import os  
import json

app = Flask(__name__)


# salvar arquivos de áudio
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def iniciaDB():

    '''
    precisa configurar a collection
    https://docs.trychroma.com/docs/collections/configure
    '''
    client = chromadb.PersistentClient(path="./chromadb")
    try:
        collection = client.create_collection(name="teste")
    except chromadb.errors.InternalError as e:
        if "already exists" in str(e):
            collection = client.get_collection(name="teste")
        else:
            raise e  
    
    return collection
    
def processa_audio(arquivo_audio):
    
    try:
        y, sr = librosa.load(arquivo_audio, sr=None)

        #tom  médio
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = float(pitches[magnitudes > 0].mean()) if magnitudes.any() else 0.0

        #frequência média
        spectral_centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())

        document = {
            "frequencia_media": spectral_centroid,
            "tom_medio": pitch,
            "sample_rate": sr,
            "duracao": float(librosa.get_duration(y=y, sr=sr))
        }
        return document
    except Exception as e:
        print(f"Erro ao processar o áudio: {e}")
        return None
   



collection = iniciaDB()

@app.route('/processa_dados', methods=['POST'])
def processa_dados():
    nome = request.form.get('nome')
    if not nome:
        return "Erro: Nome não fornecido!", 400

    print(f'Nome: {nome}')

    audio = request.files.get('audio')
    if not audio:
        return "Erro: Áudio não fornecido!", 400

    # Salva o arquivo  
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
    audio.save(audio_path)

    audio_carac = processa_audio(audio_path)
    audio_carac_json = json.dumps(audio_carac)
    collection.add(
        documents=[audio_carac_json],  
        metadatas=[{"source": "formulario", "nome": nome, "audio_path": audio_path.replace("\\", "/")}],
        ids=["id_" + nome]
    )
    print(collection.get(include=["documents", "metadatas"]))
    return "Dados e áudio inseridos com sucesso no ChromaDB!"

@app.route('/recuperar_dados')
def recuperar_dados():
    resultados = collection.get(include=["documents", "metadatas"])

    documentos = [json.loads(doc) for doc in resultados['documents']]
    return render_template('recupera.html', resultados=resultados, documentos=documentos, zip=zip)

@app.route('/uploads/<path:filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/excluir', methods=['POST'])
def excluir():
    data = request.get_json()
    audio_path = data.get('audio_path')

    if not audio_path:
        return jsonify({'erro': 'audio_path não fornecido'}), 400

    return jsonify({'mensagem': 'Exclusão realizada com sucesso'})

@app.route('/')
def formulario():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
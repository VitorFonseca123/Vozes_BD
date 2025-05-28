from flask import Flask, jsonify, request, render_template, send_from_directory
import chromadb
from chromadb.config import Settings
import os  
import json
import operacoesDB
import processamento

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
    
collection = iniciaDB()
#operacoesDB.insere_audios(collection)

@app.route('/processa_dados', methods=['POST'])
def processa_dados():
    nome = request.form.get('nome')
    if not nome:
        return "Erro: Nome não fornecido!", 400

    #print(f'Nome: {nome}')

    audio = request.files.get('audio')
    if not audio:
        return "Erro: Áudio não fornecido!", 400

    # Salva o arquivo  
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
    audio.save(audio_path)

    audio_carac, embeddings = processamento.processa_audio(audio_path, collection)
    audio_carac_json = json.dumps(audio_carac)
    operacoesDB.insertion(collection, audio_path, audio_carac_json, nome, embeddings)
    return "Dados processados com sucesso!", 200

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

    print(audio_path)
    if not audio_path:
        return jsonify({'erro': 'audio_path não fornecido'}), 400

    print(audio_path)

    collection.delete(
        where = {"audio_path": audio_path }
    )
    os.remove(audio_path)

    return jsonify({'mensagem': 'Exclusão realizada com sucesso'})

@app.route('/')
def formulario():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
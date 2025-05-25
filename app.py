from flask import Flask, jsonify, request, render_template, send_from_directory
import chromadb
from chromadb.config import Settings
import librosa 
import os  
import json
import operacoesDB
import processamento

app = Flask(__name__)


# salvar arquivos de áudio
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def iniciaDB(collection_name):
    '''
    Configura a collection
    https://docs.trychroma.com/docs/collections/configure
    '''
    client = chromadb.PersistentClient(path="./chromadb")
    try:
        collection = client.create_collection(name=collection_name)
    except chromadb.errors.InternalError as e:
        if "already exists" in str(e):
            collection = client.get_collection(name=collection_name)
        else:
            raise e  

    return collection

#Inicializa collections 
collection_dub = iniciaDB("dub")
collection_carac_dub = iniciaDB("carac_dub")
collection_per = iniciaDB("per")
collection_carac_per = iniciaDB("carac_per")
collection_carac = iniciaDB("carac")

operacoesDB.insere_caracs(collection_carac)
operacoesDB.insere_audios(collection_dub, collection_carac_dub, collection_carac)
    
@app.route('/processa_dados', methods=['POST'])
def processa_novo_audio():
    nome_per = request.form.get('nome')
    nome_dub = request.form.get('dublador')
    per_genero = request.form.get('genero')
    per_idade = request.form.get('faixa etaria')
    if not nome_per or not per_genero or not per_idade or not nome_dub:
        return "Erro: Dado não fornecido!", 400

    audio = request.files.get('audio')
    if not audio:
        return "Erro: Áudio não fornecido!", 400
    nome_audio = audio.filename
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
    audio.save(audio_path)

    #Insere novo personagem e caracteristicas (depois chama a busca de similaridade tb)
    operacoesDB.insertionPersonagem(collection_per, nome_per, per_genero, per_idade)
    operacoesDB.insertionCarac(collection_carac_per, collection_carac, collection_dub, audio_path, nome_audio, nome_dub)


@app.route('/recuperar_dados')
def recuperar_dados():
    resultados = collection_carac_dub.get(include=["documents", "metadatas"])

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
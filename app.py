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
    
Audios_Collection = iniciaDB()
Dubladores_Collection = iniciaDB()
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

    audio_carac, embeddings = processamento.processa_audio(audio_path, Audios_Collection)
    audio_carac_json = json.dumps(audio_carac)
    operacoesDB.insertion(Audios_Collection, audio_path, audio_carac_json, nome, embeddings)
    busca= Audios_Collection.query(
        embeddings,
        n_results= 2,

    )
    print ("IDs similares encontrados", busca['ids'])
    print ("Distâncias: ", busca['distances'])
    return "Dados processados com sucesso!", 200

@app.route('/recuperar_dados')
def recuperar_dados():
    resultados = Audios_Collection.get(include=["documents", "metadatas"])
    print(resultados['documents'])
    documentos = [json.loads(doc) for doc in resultados['documents']]
    #print(documentos)
    return render_template('recupera.html', resultados=resultados, documentos=documentos, zip=zip)

@app.route('/uploads/<path:filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/excluir', methods=['POST'])
def excluir():
    data = request.get_json()
    audio_path = data.get('audio_path')

    #print(audio_path)
    if not audio_path:
        return jsonify({'erro': 'audio_path não fornecido'}), 400

    #print(audio_path)

    operacoesDB.Excluir_audio(Audios_Collection, audio_path)
    os.remove(audio_path)

    return jsonify({'mensagem': 'Exclusão realizada com sucesso'})

@app.route('/busca')
def formulario_busca():
    return render_template('busca.html')

@app.route('/similares', methods=['POST'])
def busca():
    qtd = int(request.form.get('qtd'))
    audio = request.files.get('audio')
    audio_carac, embed = processamento.processa_audio(audio, Audios_Collection)

    resultado = Audios_Collection.query(
        query_embeddings=[embed],
        n_results=qtd,
        include=["documents", "metadatas"]
    )
    #print(resultado['documents'])
    

    documents = [json.loads(doc) for doc in resultado['documents'][0]]
    #print(resultado['documents'][0])
    
    return  render_template('similares.html',  resultados = resultado, documentos=documents, zip=zip)
@app.route('/')
def formulario():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
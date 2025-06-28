from flask import Flask, jsonify, request, render_template, send_from_directory
import chromadb
from chromadb.config import Settings
import os  
import json
import operacoesDB
from collections import defaultdict

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
    
Audios_Collection = iniciaDB('Audios')
Dubladores_Collection = iniciaDB('Dubladores')
dub = Dubladores_Collection.get(include=["documents", "metadatas"])
if not dub['documents']:
    print("Nenhuma característica encontrada, inserindo as características padrão...")
    operacoesDB.insere_EDM(Dubladores_Collection, Audios_Collection)
    operacoesDB.insere_lol(Dubladores_Collection, Audios_Collection)
#operacoesDB.insere_audios(collection)

@app.route('/processa_dados', methods=['POST'])
def processa_dados():
    nome = request.form.get('nome')
    if not nome:
        return "Erro: Nome não fornecido!", 400
    dublador = request.form.get('dublador').lower()
    #print(f'Nome: {nome}')

    audio = request.files.get('audio')
    if not audio:
        return "Erro: Áudio não fornecido!", 400
    nome_audio = audio.filename
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], nome_audio)
    audio.save(audio_path)

    
    operacoesDB.insertion(Audios_Collection, audio_path, nome, dublador)

    
    return "Dados processados com sucesso!", 200

@app.route('/recuperar_dados')
def recuperar_dados():
    resultados = Audios_Collection.get(include=["documents", "metadatas"])
    #print(resultados['documents'])
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
    audio = request.files.get('audio')
    if not audio:
        return "Erro: Áudio não fornecido!", 400

    # Salva o arquivo  
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
    audio.save(audio_path)

    audio_carac, embed = processamento.processa_audio(audio_path, Audios_Collection)

    resultado = Audios_Collection.query(
        query_embeddings=[embed],
        n_results=qtd,
        include=["documents", "metadatas", 'distances']
    )
    #print(resultado['documents'])
    
    

    docs_para_template = [json.loads(doc) for doc in resultado['documents'][0]]
    metas_para_template = resultado['metadatas'][0]
    raw_dists_para_template = resultado['distances'][0]
    #print(resultado['documents'][0])
    D_max = 1
    similaridades_para_template = []
    for dist in raw_dists_para_template:
        
        
        if D_max == 0: 
            similarity_percentage = 100.0
        else:
            similarity_percentage = (1 - (dist / D_max)) * 100
        
        
        similarity_percentage = max(0.0, min(100.0, similarity_percentage))
        
        similaridades_para_template.append(similarity_percentage) 

    
    return render_template(
        'similares.html', 
        resultados_combinados=zip(metas_para_template, docs_para_template, similaridades_para_template), 
        audio_path=audio_path
    )

@app.route('/dublador/<dublador_id>')
def mostrar_detalhes_dublador(dublador_id):

    audios = Audios_Collection.get(include=['documents', 'metadatas'], where= {"dublador": dublador_id})
    
    dublador_id = dublador_id.replace(' ', '_')
    #print(f"ID do dublador recebido: {dublador_id}")

    dublador = Dubladores_Collection.get(ids=[dublador_id], include=["documents", "metadatas"])
    #print(dublador)
    
    nome = dublador['metadatas'][0].get('nome')
    faixa_etaria = dublador['metadatas'][0].get('dub_idade')
    genero = dublador['metadatas'][0].get('dub_genero')
    
    
    documentos = [json.loads(doc) for doc in audios['documents']]
    

    
    #print(faixa_etaria)
    return render_template('dublador.html', nome = nome, faixa_etaria=faixa_etaria, genero=genero,resultados = audios, documentos=documentos, audios=audios, zip=zip)
@app.route('/')
def formulario():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

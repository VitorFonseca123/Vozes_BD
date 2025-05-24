import processamento
import json


def insertion(collection, audio_path, audio_carac_json, nome, embeddings):
    if not embeddings:
        collection.add(
            documents=[audio_carac_json], 
            embeddings=[[0,0]],  #  ele não deixa iniciar sem embeddings
            metadatas=[{"source": "formulario", "nome": nome, "audio_path": audio_path.replace("\\", "/")}],
            ids=["id_" + nome]
        )
    else:
        collection.add(
            documents=[audio_carac_json],  
            embeddings=[embeddings],
            metadatas=[{"source": "formulario", "nome": nome, "audio_path": audio_path.replace("\\", "/")}],
            ids=["id_" + nome]
        )
    #print(collection.get(include=["documents", "metadatas"]))
    return "Dados e áudio inseridos com sucesso no ChromaDB!"
    
def insere_audios(collection):
    folder = "audios"
    for item in folder:
        nome = item
        audio_carac = processamento.processa_audio(item)
        audio_carac_json = json.dumps(audio_carac)
        insertion(collection, item, audio_carac_json, nome)
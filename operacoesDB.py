import processamento
import json


def insertion(collection, audio_path, audio_carac_json, nome, embeddings, dublador):
    collection.add(
            documents=[audio_carac_json],  
            embeddings=embeddings,
            metadatas=[{"dublador": "id_"+dublador, "nome": nome, "audio_path": audio_path.replace("\\", "/")}],
            ids=["id_" + audio_path]
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

def Excluir_audio(Audios_Collection, audio_path):
     Audios_Collection.delete(
        where = {"audio_path": audio_path }
    )
   

def insertion_dublador(collection, nome, dublador, dub_genero, dub_idade):
    collection.add(
        documents=[nome],  
        metadatas=[{
            "nome": nome,
            "dub_genero": dub_genero,
            "dub_idade": dub_idade
        }],
        ids=["id_" + nome.replace(" ", "_").lower()]
    )
    return "Dublador inserido com sucesso no ChromaDB!"
    
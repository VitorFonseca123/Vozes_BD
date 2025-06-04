import json
import processamento
import os
from pydub import AudioSegment


def insertion(collection, audio_path, nome, dublador):
    audio_carac, embeddings = processamento.processa_audio(audio_path, collection)
    audio_carac_json = json.dumps(audio_carac)
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
   

def insertion_dublador(collection, nome, dub_genero, dub_idade):
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

def insere_massa(dubladores_collection, audios_collection):
    dubladores= [
        ["Agatha", "Karen Padrão", "Feminino", "Adulto"],
        ["Jaser", "Raphael Rossatto", "Masculino", "Adulto"],
        ["Lupi", "Lobinho", "Masculino", "Adulto"],
        ["Mia", "Pamella Rodrigues", "Feminino", "Adulto"],
        ["Samuel", "Fred Mascarenhas", "Masculino", "Adulto"],
        ["Verissimo", "Guilherme Briggs", "Masculino", "Adulto"]
    ]
    
    for dublador in dubladores:
        personagem, nome, dub_genero, dub_idade = dublador
        dub_idade = dub_idade.lower()
        insertion_dublador(dubladores_collection, nome, dub_genero, dub_idade)
        audio_path = f"audios/{personagem}.mp3"
        audio = AudioSegment.from_mp3(audio_path)


        
        
    return "Dados de dublador inseridos com sucesso no ChromaDB!"




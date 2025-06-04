import json
import processamento
import os
import shutil


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




def insere_EDM(dubladores_collection, audios_collection):
    
    dubladores = [
        ["Agatha", "Karen Padrão", "Feminino", "Adulto"],
        ["Jaser", "Raphael Rossatto", "Masculino", "Adulto"],
        ["Lupi", "Lobinho", "Masculino", "Adulto"],
        ["Mia", "Pamella Rodrigues", "Feminino", "Adulto"],
        ["Samuel", "Fred Mascarenhas", "Masculino", "Adulto"],
        ["Verissimo", "Guilherme Briggs", "Masculino", "Adulto"]
    ]

    os.makedirs('./uploads', exist_ok=True)

    for dublador in dubladores:
        personagem, nome, dub_genero, dub_idade = dublador
        dub_idade = dub_idade.lower()
        
        insertion_dublador(dubladores_collection, nome, dub_genero, dub_idade)
        
        personagem_audio_dir = f"audios/enigma do medo/{personagem}/"
        
        if not os.path.isdir(personagem_audio_dir):
            print(f"Diretório não encontrado: {personagem_audio_dir}. Pulando este personagem.")
            continue

        for filename in os.listdir(personagem_audio_dir):
            
            if filename.endswith(".wav"):
                origem_audio_path = os.path.join(personagem_audio_dir, filename)
                destino_audio_path = os.path.join('./uploads', filename) 

                try:
                    
                    shutil.copy(origem_audio_path, destino_audio_path)
                    insertion(audios_collection, destino_audio_path, personagem, dublador[1].lower())
                    #print(f"Áudio copiado: {origem_audio_path} -> {destino_audio_path}")
                except FileNotFoundError:
                    print(f"Erro: Arquivo não encontrado para copiar: {origem_audio_path}")
                except Exception as e:
                    print(f"Erro inesperado ao copiar o áudio {filename}: {e}")

    return "Dados de dublador inseridos e áudios .wav copiados com sucesso!"

 
        
        
    return "Dados de dublador inseridos com sucesso no ChromaDB!"




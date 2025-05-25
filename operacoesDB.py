import processamento
import json
import os

def insertionCarac(collection_audio_feature, collection_features, collection_actor, audio_path, nome_audio, nome_dub):
    # Process audio to extract features
    audio_carac = processamento.processa_audio(audio_path)
    
    # Loop through extracted features and insert each as a reference
    for feature_name, feature_value in audio_carac.items():
        collection_audio_feature.add(
            documents=[str(feature_value)],  # Store feature value
            metadatas=[{
                "source": "processamento",
                "nome_audio": nome_audio,
                "audio_path": audio_path.replace("\\", "/"),
                "feature_ref": collection_features.get(ids=["id_" + feature_name]),  # Reference the feature
                "actor_ref": collection_actor.get(ids=["id_" + nome_dub])  # Reference the actor
            }],
            ids=["id_" + nome_audio + "_" + feature_name]
        )
    
    print(collection_audio_feature.get(include=["documents", "metadatas"]))
    return "Dados de características do áudio inseridos com sucesso no ChromaDB!"

def insertionDublador(collection_dub, nome, dub_genero, dub_idade):
    collection_dub.add(
        documents=[nome],  # Store the voice actor's name
        metadatas=[{
            "source": "formulario",
            "nome": nome,
            "dub_genero": dub_genero,
            "dub_idade": dub_idade
        }],
        ids=["id_" + nome.replace(" ", "_").lower()]
    )
    
    print(collection_dub.get(include=["documents", "metadatas"]))
    return "Dados de dublador inseridos com sucesso no ChromaDB!"

def insertionPersonagem(collection_per, nome, per_genero, per_idade):
    collection_per.add(
        documents=[nome],  # Store the voice actor's name
        metadatas=[{
            "source": "formulario",
            "nome": nome,
            "dub_genero": per_genero,
            "dub_idade": per_idade
        }],
        ids=["id_" + nome.replace(" ", "_").lower()]
    )
    
    print(collection_per.get(include=["documents", "metadatas"]))
    return "Dados de dublador inseridos com sucesso no ChromaDB!"

def insere_caracs(collection_carac):
    caracs = [
        {"nome": "frequencia_media", "unidade": "Hz"},
        {"nome": "tom_medio", "unidade": "Hz"},
        {"nome": "sample_rate", "unidade": "Hz"},
        {"nome": "duracao", "unidade": "seconds"}
    ]
    
    for i, item in enumerate(caracs):
        collection_carac.add(
            documents=[item["nome"]],
            metadatas=[{
                "unidade": item["unidade"]
            }],
            ids=["id_" + str(i)]
        )
    
    print(collection_carac.get(include=["documents", "metadatas"]))
    return "Características inseridas com sucesso no ChromaDB!"

def insere_audios(collection_dub, collection_carac_dub, collection_carac):
    audios = [[folder_name, ator, genero_ator, idade_ator]]
    for audio_data in audios:
        folder_name, ator, genero_ator, idade_ator = audio_data  # Unpack the values
        
        # Insert actor into the collection
        insertionDublador(collection_dub, ator, genero_ator, idade_ator)
        
        # Get first audio file in the folder
        audio_files = [f for f in os.listdir(folder_name) if f.endswith((".wav", ".mp3", ".flac"))]
        if audio_files:
            first_audio_path = os.path.join(folder_name, audio_files[0])
            insertionCarac(collection_carac_dub, collection_carac, collection_dub, first_audio_path, folder_name, ator)
    
    return "Processamento de pastas de áudio concluído!"
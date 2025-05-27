import processamento
import json
import os

def insertionCarac(collection_audio_feature, collection_features, audio_path, nome_audio, id_dub):
    audio_carac = processamento.processa_audio(audio_path)
    
    # If the function failed to process audio, skip insertion
    if audio_carac is None:
        print(f"⚠️ Erro ao processar o áudio: {audio_path}, pulando...")
        return "Erro no processamento do áudio, não foi inserido."

    for feature_name, feature_value in audio_carac.items():
        # Ensure feature_value is valid (convert None to a default value)
        if feature_value is None:
            feature_value = -1.0  # Default invalid value

        # Retrieve only the **feature and actor IDs**, avoiding dicts
        feature_entry = collection_features.get(ids=["id_" + feature_name])
        print(collection_features.get(include=["documents", "metadatas"]))
        print(feature_entry)
        feature_id = feature_entry["ids"][0]

        # ChromaDB requires metadatas to be **primitive types**
        collection_audio_feature.add(
            documents=[str(feature_value)],  # Store feature value
            metadatas=[{
                "source": "processamento",
                "nome_audio": nome_audio,
                "audio_path": audio_path.replace("\\", "/"),
                "feature_ref": str(feature_id),  # Ensure **string type**
                "dub_ref": id_dub  # Ensure **string type**
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
    print("Dados de personagem inseridos com sucesso no ChromaDB!")

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
            ids=["id_" + item["nome"]]
        )
    
    #print(collection_carac.get(include=["documents", "metadatas"]))
    print("Características inseridas com sucesso no ChromaDB!")
    return collection_carac

def insere_audios(collection_dub, collection_carac_dub, collection_carac):
    audios = [
        ["Agatha", "Karen Padrão", "Feminino", "Adulto"],
        ["Jaser", "Raphael Rossatto", "Masculino", "Adulto"],
        ["Lupi", "Lobinho", "Masculino", "Adulto"],
        ["Mia", "Pamella Rodrigues", "Feminino", "Adulto"],
        ["Samuel", "Fred Mascarenhas", "Masculino", "Adulto"],
        ["Verissimo", "Guilherme Briggs", "Masculino", "Adulto"]
    ]

    for audio_data in audios:
        folder_name, dublador, genero_dublador, idade_dublador = audio_data  # Unpack the values
        
        insertionDublador(collection_dub, dublador, genero_dublador, idade_dublador)
        
        audio_files = [f for f in os.listdir(folder_name) if f.endswith((".wav", ".mp3", ".flac"))]
        if audio_files:
            first_audio_path = os.path.join(folder_name, audio_files[0])
            id_dub = "id_" + dublador.replace(" ", "_").lower()
            insertionCarac(collection_carac_dub, collection_carac, first_audio_path, folder_name, id_dub)
    print(collection_carac_dub.get(include=["documents", "metadatas"]))
    print("Processamento de pastas de áudio concluído!")


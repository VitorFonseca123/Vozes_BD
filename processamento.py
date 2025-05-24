import json
import librosa
import numpy as np



def min_max_normalize(v, min_v, max_v):
    return (v - min_v) / (max_v - min_v) if max_v != min_v else 0.0


def processa_audio(arquivo_audio, collection):
    try:
        y, sr = librosa.load(arquivo_audio, sr=None)

        #tom  médio
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = float(pitches[magnitudes > 0].mean()) if magnitudes.any() else 0.0

        #frequência média
        spectral_centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())


        document = {
            "frequencia_media": spectral_centroid, 
            "tom_medio": pitch,
            #retirei Sample rate, pois todos os audios tem a mesma taxa de amostragem
        
        }
        
        resultados = collection.get(include=["documents"])
        
        if not resultados["documents"]:
            return document, []
        

        documentos = [json.loads(doc) for doc in resultados["documents"]]
        embeddings = []
        for doc in documentos:
            freq = doc["frequencia_media"]
            tom = doc["tom_medio"] 
            embeddings.append([freq, tom])  
        #print(embeddings)
        #print(valores)
        embeddings= np.array(embeddings)
        minimos = embeddings.min(axis=0)
        maximos = embeddings.max(axis=0)

        embeddings_norm = []

        for embedding in embeddings:
            normalized_embedding = []
            for i, val in enumerate(embedding):
                normalized_val = min_max_normalize(val, minimos[i], maximos[i])
                normalized_embedding.append(normalized_val)
            embeddings_norm.append(normalized_embedding)
        

        
        
        
        result = collection.get(include=["documents"])
        ids = result["ids"]
        print(ids)
        if len(ids) != len(embeddings_norm):
            raise ValueError("Número de IDs e embeddings não bate.")

        collection.update(
            ids=ids,
            embeddings=embeddings_norm
        )
        print(collection.get(include=["embeddings"]))

        embedding = [ #normalizados
            min_max_normalize(spectral_centroid, minimos[0], maximos[0]),
            min_max_normalize(pitch, minimos[1], maximos[1]),                   
            #retirei Sample rate, pois todos os audios tem a mesma taxa de amostragem
        ]
        
        return document, embedding
    except Exception as e:
        print(f"Erro ao processar o áudio: {e}")
        return None


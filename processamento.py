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

        resultados = collection.get(include=["embeddings", "metadatas"])
        embeddings = np.array(resultados["embeddings"])
        
        minimos = embeddings.min(axis=0)  
        maximos = embeddings.max(axis=0)  

        embeddings_norm = np.array([
            [min_max_normalize(val, minimos[i], maximos[i]) for i, val in enumerate(embedding)]
            for embedding in embeddings
            ])

        print(embeddings_norm)


        document = {
            "frequencia_media": spectral_centroid, 
            "tom_medio": pitch,
            #retirei Sample rate, pois todos os audios tem a mesma taxa de amostragem
        
        }
        embedding = [ #normalizados
            spectral_centroid / sr, #talvez?
            pitch/sr,                   
            #retirei Sample rate, pois todos os audios tem a mesma taxa de amostragem
]
        return document, embedding
    except Exception as e:
        print(f"Erro ao processar o áudio: {e}")
        return None


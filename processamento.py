import json
import math
import librosa
import numpy as np



def min_max_normalize(v, min_v, max_v):
    return (v - min_v) / (max_v - min_v) if max_v != min_v else 0.0


def processa_audio(arquivo_audio, collection):
    try:
        y, sr = librosa.load(arquivo_audio, sr=None)


        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        
        pitch = float(pitches[magnitudes > 0].mean()) if magnitudes.any() and pitches[magnitudes > 0].size > 0 else 0.0


        spectral_centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())

        '''Calcula a variante "Chroma Energy Normalized Statistical" (CENS)
        do cromagrama. CENS é projetado para ser robusto a variações de timbre e dinâmica,
        tornando-o ideal para tarefas como recuperação de informações musicais 
        e alinhamento de áudio.'''
        chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
        chroma_cens_medio = float(chroma_cens.mean())
       
        '''Calcula os Coeficientes Cepstrais de Frequência Mel.
        Os MFCCs são uma representação compacta e eficaz do envelope 
        espectral de um sinal de áudio. Eles são amplamente usados em
        reconhecimento de fala e identificação de locutor devido à sua 
        capacidade de capturar o timbre da voz.
       '''
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        mfccs_medios = mfccs.mean(axis=1).tolist()
        

        document = {
            "frequencia_media": spectral_centroid,
            "tom_medio": pitch,
            "croma_medio": chroma_cens_medio,
            "mfcc_medios": mfccs_medios
        }

       
        resultados = collection.get(include=["documents"])

        
        if not resultados["documents"]:
            
            return document, [0.0] * 23


        documentos = [json.loads(doc) for doc in resultados["documents"]]
        embeddings = []
        embeddings = []
        for doc in documentos:
            freq = doc.get("frequencia_media", 0.0) 
            tom = doc.get("tom_medio", 0.0)
            croma = doc.get("croma_medio", 0.0) 
            mfcc_existing = doc.get("mfcc_medios", [0.0] * len(mfccs_medios)) 
            
            embeddings.append([freq, tom, croma] + mfcc_existing) 

        embeddings = np.array(embeddings)

        minimos = embeddings.min(axis=0)
        maximos = embeddings.max(axis=0)

        embeddings_norm = []
        for embedding_val in embeddings:
            normalized_embedding = []
            for i, val in enumerate(embedding_val):
                normalized_val = min_max_normalize(val, minimos[i], maximos[i])
                normalized_embedding.append(normalized_val)
            embeddings_norm.append(normalized_embedding)
        
        ids = resultados["ids"]

        if len(ids) != len(embeddings_norm):
            raise ValueError("Número de IDs e embeddings não corresponde.")

        MAX_BATCH_SIZE = 5461 
        num_embeddings = len(embeddings_norm)
        num_batches = math.ceil(num_embeddings / MAX_BATCH_SIZE)

        for i in range(num_batches):
            start_idx = i * MAX_BATCH_SIZE
            end_idx = min((i + 1) * MAX_BATCH_SIZE, num_embeddings)

            batch_ids = ids[start_idx:end_idx]
            batch_embeddings = embeddings_norm[start_idx:end_idx]

            collection.update(
                ids=batch_ids,
                embeddings=batch_embeddings
            )
        #print("Todas as atualizações de embeddings existentes foram concluídas.")
       
        new_audio_embedding_norm = [
            min_max_normalize(spectral_centroid, minimos[0], maximos[0]),
            min_max_normalize(pitch, minimos[1], maximos[1]),
            min_max_normalize(chroma_cens_medio, minimos[2], maximos[2]),
                 
        ]
        for i, mfcc_val in enumerate(mfccs_medios):
            new_audio_embedding_norm.append(min_max_normalize(mfcc_val, minimos[3 + i], maximos[3 + i]))
        return document, new_audio_embedding_norm

    except Exception as e:
        print(f"Erro ao processar o áudio: {e}")
        return None

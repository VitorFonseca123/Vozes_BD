import librosa

def processa_audio(arquivo_audio):
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
            "sample_rate": sr,
            "duracao": float(librosa.get_duration(y=y, sr=sr))
        }
        return document
    except Exception as e:
        print(f"Erro ao processar o áudio: {e}")
        return None


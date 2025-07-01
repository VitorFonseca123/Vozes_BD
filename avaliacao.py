from app import Audios_Collection

def precisao(resultados_similaridade):
    metadatas = resultados_similaridade['metadatas'][0]

    if not metadatas:
        return 0.0

    # Get the dublador of the first result
    dublador_id = metadatas[0]['dublador']

    # Count how many results have the same dublador
    recuperadas_relevantes = sum(1 for r in metadatas if r['dublador'] == dublador_id)

    return recuperadas_relevantes / len(metadatas)

def revocacao(resultados_similaridade):

    
    metadatas = resultados_similaridade['metadatas'][0]
    if not metadatas:
        return 0

    # Get the reference dublador from the first result
    dublador_id = metadatas[0]['dublador']
    # Count how many times it appears in the retrieved results
    recuperadas_relevantes = sum(1 for r in metadatas if r['dublador'] == dublador_id)
    audios = Audios_Collection.get(include=["metadatas"])
    metadatas = audios['metadatas']
    relevantes =  sum(1 for entry in metadatas if entry['dublador'] == dublador_id)
    print(relevantes)
    if relevantes == 0:
        return 0.0

    return recuperadas_relevantes/relevantes

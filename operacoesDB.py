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
            metadatas=[{"dublador": "id_" + dublador.replace(" ", "_").lower(), "nome": nome, "audio_path": audio_path.replace("\\", "/")}],
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
            "dub_idade": dub_idade #realmente necessário? Maioria vai ser adulto
        }],
        ids=["id_" + nome.replace(" ", "_").lower()]
    )
    return "Dublador inserido com sucesso no ChromaDB!"


def coleta_audios(dubladores_data, audios_collection, dubladores_collection,base_audio_path):

    os.makedirs('./uploads', exist_ok=True)
    
    for dublador_info in dubladores_data:
        personagem, nome, dub_genero, dub_idade = dublador_info
        dub_idade = dub_idade.lower()

        insertion_dublador(dubladores_collection, nome, dub_genero, dub_idade)

        personagem_audio_dir = os.path.join(base_audio_path, personagem)

        if not os.path.isdir(personagem_audio_dir):
            print(f"Diretório não encontrado: {personagem_audio_dir}. Pulando este personagem.")
            continue

        for filename in os.listdir(personagem_audio_dir):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                origem_audio_path = os.path.join(personagem_audio_dir, filename)
                destino_audio_path = os.path.join('./uploads', filename)

                try:
                    shutil.copy(origem_audio_path, destino_audio_path)
                    insertion(audios_collection, destino_audio_path, personagem, dublador_info[1].lower())
                except FileNotFoundError:
                    print(f"Erro: Arquivo não encontrado para copiar: {origem_audio_path}")
                except Exception as e:
                    print(f"Erro inesperado ao copiar o áudio {filename}: {e}")

    return "Dados inseridos e áudios copiados com sucesso!"

def insere_EDM(dubladores_collection, audios_collection):
    dubladores = [
        ["Agatha", "Karen Padrão", "Feminino", "Adulto"],
        ["Jaser", "Raphael Rossatto", "Masculino", "Adulto"],
        ["Mia", "Pamella Rodrigues", "Feminino", "Adulto"],
        ["Samuel", "Fred Mascarenhas", "Masculino", "Adulto"],
        ["Verissimo", "Guilherme Briggs", "Masculino", "Adulto"]
    ]
    return coleta_audios(
        dubladores,
        audios_collection,
        dubladores_collection,
        "audios/enigma do medo/"
    )


def insere_lol(dubladores_collection, audios_collection):

    dubladores = [
        ["Aatrox", "Hércules Franco	", "Masculino", "Adulto"],
        ["Ahri","Miriam Ficher", "Feminino", "Adulto"],
        ["Akali", "Adriana Torres", "Feminino", "Adulto"],
        ["Akshan", "Fábio Azevedo", "Masculino", "Adulto"],
        ["Alistar", "Leo Rabelo", "Masculino", "Adulto"],
        ["Ambessa", "Marilza Batista", "Feminino", "Adulto"],
        ["Amumu", "Luiz Sergio Vieira", "Masculino", "Adulto"],
        ["Anivia", "Lucia Helena", "Feminino", "Adulto"],
        ["Annie", "Helena Palomanes", "Feminino", "Adulto"],
        ["Ashe", "Marcia Morelli", "Feminino", "Adulto"],
        ["Aurelion Sol", "Gilberto Barolli", "Masculino", "Adulto"],
        ["Aurora","Mari Haruno", "Feminino", "Adulto"],
        ["Azir", "Fabio de Castro", "Masculino", "Adulto"],
        ["BelVeth", "Marlene Costa", "Feminino", "Adulto"],
        ["Blitzcrank", "Leonardo Santhos", "Masculino", "Adulto"],
        ["Brand", "Eduardo Dascar", "Masculino", "Adulto"],
        ["Braum", "Jonas Mello", "Masculino", "Adulto"],
        ["Briar", "Fernanda Barone", "Feminino", "Adulto"],
        ["Caitlyn", "Mabel Cezar", "Feminino", "Adulto"],
        ["Camille", "Roseli Silva", "Feminino", "Adulto"],
        ["Cassiopeia", "Luciana Baroli", "Feminino", "Adulto"],
        ["Corki", "Isaac Bardavid", "Masculino", "Idoso"],
        ["Darius", "Ricardo Telles", "Masculino", "Adulto"],
        ["Diana", "Rosa Maria Baroli", "Feminino", "Adulto"],
        ["DrMundo", "Nardo Sierpe", "Masculino", "Adulto"],
        ["Draven", "Ricardo Juarez", "Masculino", "Adulto"],
        ["Ekko", "Marcelo Campos", "Masculino", "Adulto"],
        ["Evelyn", "Luisa Palomanes", "Feminino", "Adulto"],
        ["Ezreal", "Anderson Oliveira", "Masculino", "Adulto"],
        ["Fiora", "Marli Bortoletto", "Feminino", "Adulto"],
        ["Fizz", "Rodrigo Antas", "Masculino", "Adulto"],
        ["Galio", "Élcio Romar", "Masculino", "Adulto"],
        ["Gangplank", "Luiz Carlos Persy", "Masculino", "Adulto"],
        ["Garen", "Gutemberg Barros", "Masculino", "Adulto"],
        ["Gnar", "Úrsula Bezerra", "Feminino", "Infantil"],
        ["Gragas", "Flávio Back", "Masculino", "Adulto"],
        ["Graves", "Élcio Romar", "Masculino", "Adulto"],
        ["Heimerdinger", "André Belizar", "Masculino", "Adulto"],
        ["Illaoi", "Luísa Viegas", "Feminino", "Adulto"],
        ["Irelia", "Mariana Torres", "Feminino", "Adulto"],
        ["Janna", "Jullie Vasconcelos", "Feminino", "Adulto"],
        ["JarvanIV", "Christiano Torreão", "Masculino", "Adulto"],
        ["Jax", "Waldyr Sant'anna", "Masculino", "Adulto"],
        ["Jayce", "Malta Júnior", "Masculino", "Adulto"],
        ["Jinx", "Fernanda Bullara", "Feminino", "Adulto"],
        ["Kalista", "Calista Helena", "Feminino", "Adulto"],
        ["Karma", "Marize Motta", "Feminino", "Adulto"],
        ["Karthus", "Isaac Bardavid", "Masculino", "Idoso"],
        ["Kassadin", "Júlio Chaves", "Masculino", "Adulto"],
        ["Katarina", "Silvia Goiabeira", "Feminino", "Adulto"],
        ["Kayle", "Carla Pompílio", "Feminino", "Adulto"],
        ["Kennen", "Luisa Palomanes", "Masculino", "Infantil"],
        ["Kindred", "Rebeca Zadra", "Feminino", "Adulto"],
        ["KogMaw", "Leonardo Santhos", "Masculino", "Infantil"],
        ["LeBlanc", "Carol Crespo", "Feminino", "Adulto"],
        ["LeeSin", "Wendel Bezerra", "Masculino", "Adulto"],
        ["Leona", "Angélica Borges", "Feminino", "Adulto"],
        ["Lissandra", "Alessandra Araújo", "Feminino", "Adulto"],
        ["Lucian", "Marco Antônio Abreu", "Masculino", "Adulto"],
        ["Lulu", "Pamella Rodrigues", "Feminino", "Infantil"],
        ["Lux", "Cristiane Monteiro", "Feminino", "Adulto"],
        ["Malphite", "Rodrigo Oliveira", "Masculino", "Adulto"],
        ["Malzahar", "Renato Rosenberg", "Masculino", "Adulto"],
        ["Maokai", "Waldyr Sant'anna", "Masculino", "Adulto"],
        ["MasterYi", "Dário de Castro", "Masculino", "Adulto"],
        ["MissFortune", "Maíra Góes", "Feminino", "Adulto"],
        ["Mordekaiser", "José Santa Cruz", "Masculino", "Adulto"],
        ["Morgana", "Marisa Leal", "Feminino", "Adulto"],
        ["Nami", "Michelle Giudice", "Feminino", "Adulto"],
        ["Nasus", "Renato Rosenberg", "Masculino", "Adulto"],
        ["Nautilus", "Sérgio Fortuna", "Masculino", "Adulto"],
        ["Nidalee", "Rita Lopes", "Feminino", "Adulto"],
        ["Nunu", "Matheus Caliano", "Masculino", "Infantil"],
        ["Olaf", "Mauro Ramos", "Masculino", "Adulto"],
        ["Pantheon", "Mário Tupinambá", "Masculino", "Adulto"],
        ["Poppy", "Marisa Leal", "Feminino", "Infantil"],
        ["Quinn", "Jussara Marques", "Feminino", "Adulto"],
        ["Renekton", "Jorge Vasconcellos", "Masculino", "Adulto"],
        ["Riven", "Melissa Garcia", "Feminino", "Adulto"],
        ["Rumble", "Renan Freitas", "Masculino", "Adulto"],
        ["Ryze", "Jorge Vasconcellos", "Masculino", "Adulto"],
        ["Sejuani", "Mônica Rossi", "Feminino", "Adulto"],
        ["Shaco", "Márcio Simões", "Masculino", "Adulto"],
        ["Shen", "Ettore Zuim", "Masculino", "Adulto"],
        ["Shyvana", "Carmen Sheila", "Feminino", "Adulto"],
        ["Singed", "Francisco José", "Masculino", "Adulto"],
        ["Sion", "Gutemberg Barros", "Masculino", "Adulto"],
        ["Sivir", "Christiane Louise", "Feminino", "Adulto"],
        ["Skarner", "Márcio Simões", "Masculino", "Adulto"],
        ["Sona", "Aline Ghezzi", "Feminino", "Adulto"],
        ["Soraka", "Izabel Lira", "Feminino", "Adulto"],
        ["Swain", "Carlos Seidl", "Masculino", "Adulto"],
        ["Syndra", "Raquel Marinho", "Feminino", "Adulto"],
        ["TahmKench", "Mauro Castro", "Masculino", "Adulto"],
        ["Talon", "Leo Rabelo", "Masculino", "Adulto"],
        ["Taric", "Duda Espinoza", "Masculino", "Adulto"],
        ["Teemo", "Eduardo Drummond", "Masculino", "Infantil"],
        ["Thresh", "César Marchetti", "Masculino", "Adulto"],
        ["Tristana", "Carol Kapfer", "Feminino", "Infantil"],
        ["Trundle", "Ronaldo Júlio", "Masculino", "Adulto"],
        ["Tryndamere", "Maurício Berger", "Masculino", "Adulto"],
        ["Twisted Fate", "Eduardo Dascar", "Masculino", "Adulto"],
        ["Twitch", "José Leonardo", "Masculino", "Adulto"],
        ["Udyr", "Walmir Barbosa", "Masculino", "Adulto"],
        ["Urgot", "Flávio Back", "Masculino", "Adulto"],
        ["Varus", "Paulo Vignolo", "Masculino", "Adulto"],
        ["Vayne", "Priscila Amorim", "Feminino", "Adulto"],
        ["Veigar", "Pedro Lopes", "Masculino", "Infantil"],
        ["VelKoz", "Leonardo Santhos", "Masculino", "Adulto"],
        ["Vi", "Tatiane Keplmair", "Feminino", "Adulto"],
        ["Viktor", "Francisco José", "Masculino", "Adulto"],
        ["Vladimir", "Ricardo Schnetzer", "Masculino", "Adulto"],
        ["Volibear", "José Santa Cruz", "Masculino", "Adulto"],
        ["Warwick", "Luiz Carlos Persy", "Masculino", "Adulto"],
        ["Wukong", "Leonardo Santhos", "Masculino", "Adulto"],
        ["Xerath", "Pietro Mário", "Masculino", "Adulto"],
        ["XinZhao", "Júlio Chaves", "Masculino", "Adulto"],
        ["Yasuo", "Marco Antônio Abreu", "Masculino", "Adulto"],
        ["Yorick", "Mauro Ramos", "Masculino", "Adulto"],
        ["Zac", "Affonso Amajones", "Masculino", "Adulto"],
        ["Zed", "Zeca Rodrigues", "Masculino", "Adulto"],
        ["Ziggs", "Pedro Eugênio", "Masculino", "Adulto"],
        ["Zilean", "Pietro Mário", "Masculino", "Idoso"],
        ["Zyra", "Fernanda Crispim", "Feminino", "Adulto"]
        ]

    return coleta_audios(
        dubladores,
        audios_collection,
        dubladores_collection,
        "audios/lol/"
    )




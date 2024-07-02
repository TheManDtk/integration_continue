from pathlib import Path
import shutil
import csv
import re

# Définir les chemins de base
path1 = Path("S3/silver/persistent/metrics/aer34/be54i/AR/")
path2 = Path("S3/silver/labelled/travail/aer34/be54i/AR/")
path3 = Path("S3/data/hacks/")  # Nouveau chemin pour les correspondances

# Fonction pour lister les fichiers dans chaque dossier
def lister_fichiers(path, dossiers_cibles):
    """
    Liste les fichiers dans les dossiers cibles spécifiés.

    Args:
    path (Path): Le chemin de base à parcourir.
    dossiers_cibles (list): Liste des noms de dossiers cibles à inclure.

    Returns:
    dict: Un dictionnaire avec les noms des dossiers comme clés et les listes de fichiers comme valeurs.
    """
    dossiers = {}
    for dossier in path.iterdir():
        if dossier.is_dir() and dossier.name in dossiers_cibles:
            dossiers[dossier.name] = list(dossier.iterdir())
    return dossiers

# Fonction pour extraire le nom de base des fichiers JSON ou vidéo
def extraire_nom_base(fichier, type_fichier):
    if type_fichier == "json":
        return re.sub(r'_54c\.json$', '', fichier.name)
    elif type_fichier == "video":
        return re.sub(r'_cropped_.*\.mp4$', '', fichier.name)
    else:
        raise ValueError("Type de fichier non reconnu")

# Fonction pour matcher les fichiers JSON avec les fichiers vidéo
def matcher_fichiers(fichiers_json, fichiers_video):
    correspondances = {}
    for dossier, fichiers in fichiers_json.items():
        if dossier in fichiers_video:
            correspondances[dossier] = []
            fichiers_json_bases = {extraire_nom_base(f, "json"): f for f in fichiers}
            fichiers_video_bases = {extraire_nom_base(f, "video"): f for f in fichiers_video[dossier]}
            
            for base, fichier_json in fichiers_json_bases.items():
                if base in fichiers_video_bases:
                    correspondances[dossier].append((fichier_json, fichiers_video_bases[base]))
    
    return correspondances

# Fonction pour trouver les fichiers sans correspondance
def fichiers_sans_correspondance(fichiers_json, fichiers_video):
    sans_correspondance = {"json": {}, "video": {}}
    
    for dossier, fichiers in fichiers_json.items():
        if dossier in fichiers_video:
            fichiers_json_bases = {extraire_nom_base(f, "json"): f for f in fichiers}
            fichiers_video_bases = {extraire_nom_base(f, "video"): f for f in fichiers_video[dossier]}
            
            sans_correspondance["json"][dossier] = [f for base, f in fichiers_json_bases.items() if base not in fichiers_video_bases]
            sans_correspondance["video"][dossier] = [f for base, f in fichiers_video_bases.items() if base not in fichiers_json_bases]
    
    return sans_correspondance

# Fonction pour copier les fichiers vidéo correspondants dans un nouveau répertoire
def copier_fichiers_correspondants(correspondances, source_path, destination_path):
    for dossier, fichiers in correspondances.items():
        destination_dossier = destination_path / dossier
        destination_dossier.mkdir(parents=True, exist_ok=True)
        
        for json_file, video_file in fichiers:
            source_fichier = source_path / dossier / video_file.name
            destination_fichier = destination_dossier / video_file.name
            shutil.copy2(source_fichier, destination_fichier)

# Fonction pour écrire les correspondances dans un fichier CSV
def ecrire_correspondances_csv(correspondances, path1, path2, csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Dossier', 'Fichier JSON', 'Chemin JSON', 'Fichier Vidéo', 'Chemin Vidéo'])
        
        for dossier, fichiers in correspondances.items():
            for json_file, video_file in fichiers:
                writer.writerow([dossier,
                                 json_file.name, path1 / dossier / json_file.name,
                                 video_file.name, path2 / dossier / video_file.name])

# Fonction pour écrire les fichiers vidéo sans correspondance dans un fichier CSV
def ecrire_videos_sans_correspondance_csv(sans_correspondance, path2, csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Dossier', 'Fichier Vidéo', 'Chemin Vidéo'])
        
        for dossier, fichiers in sans_correspondance["video"].items():
            for video_file in fichiers:
                writer.writerow([dossier, video_file.name, path2 / dossier / video_file.name])

# Dossiers cibles spécifiques
dossiers_cibles = ['1', '2', '4', '5']  # Liste des noms de dossiers cibles

# Lister les fichiers dans chaque chemin pour les dossiers cibles
fichiers_json = lister_fichiers(path1, dossiers_cibles)
fichiers_video = lister_fichiers(path2, dossiers_cibles)

# Trouver les correspondances
correspondances = matcher_fichiers(fichiers_json, fichiers_video)

# Trouver les fichiers sans correspondance
sans_correspondance = fichiers_sans_correspondance(fichiers_json, fichiers_video)

# Copier les fichiers vidéo correspondants dans le nouveau chemin
copier_fichiers_correspondants(correspondances, path2, path3)

# Chemins des fichiers CSV
csv_correspondances_path = "correspondances.csv"
csv_videos_sans_correspondance_path = "videos_sans_correspondance.csv"

# Écrire les correspondances et les vidéos sans correspondance dans des fichiers CSV
ecrire_correspondances_csv(correspondances, path1, path2, csv_correspondances_path)
ecrire_videos_sans_correspondance_csv(sans_correspondance, path2, csv_videos_sans_correspondance_path)

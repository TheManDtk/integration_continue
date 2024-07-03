import os
import shutil

# Liste des sous-dossiers à ignorer
ignored_subdirs = ['subdir_to_ignore1', 'subdir_to_ignore2']

def create_directories(cropped_dir, no_cropped_dir):
    try:
        if not os.path.exists(cropped_dir):
            os.makedirs(cropped_dir)
        if not os.path.exists(no_cropped_dir):
            os.makedirs(no_cropped_dir)
    except OSError as e:
        print(f"Erreur lors de la création des répertoires: {e}")
        raise

def process_files_in_directory(subdir, files):
    cropped_dir = os.path.join(subdir, 'cropped')
    no_cropped_dir = os.path.join(subdir, 'no-cropped')

    create_directories(cropped_dir, no_cropped_dir)

    alpha_files = {}
    resolu_files = {}

    for file in files:
        try:
            if file.endswith('_alpha_pos01.mp4'):
                continue

            file_path = os.path.join(subdir, file)

            if file.endswith('-cropped_48_frames.mp4'):
                move_file(file_path, cropped_dir)
            elif file.endswith('_alpha_00.mp4'):
                handle_alpha_00_file(file, file_path, alpha_files)
            else:
                handle_resolu_file(file, file_path, resolu_files)
        except Exception as e:
            print(f"Erreur lors du traitement du fichier {file}: {e}")

    move_selected_files(alpha_files, cropped_dir)
    move_selected_files(resolu_files, no_cropped_dir)

def handle_alpha_00_file(file, file_path, alpha_files):
    try:
        base_name = file.rsplit('_', 1)[0]
        num_part = int(base_name.split('_')[-1])
        base_key = '_'.join(base_name.split('_')[:-1])

        if base_key not in alpha_files:
            alpha_files[base_key] = (num_part, file_path)
        else:
            if num_part > alpha_files[base_key][0]:
                alpha_files[base_key] = (num_part, file_path)
    except ValueError as e:
        print(f"Erreur lors de la gestion du fichier alpha_00 {file}: {e}")

def handle_resolu_file(file, file_path, resolu_files):
    try:
        parts = file.rsplit('_', 1)
        if len(parts) == 2 and parts[1].endswith('.mp4'):
            uuid = parts[0]
            resolu_value = int(parts[1].split('.')[0])

            if uuid not in resolu_files:
                resolu_files[uuid] = (resolu_value, file_path)
            else:
                if resolu_value > resolu_files[uuid][0]:
                    resolu_files[uuid] = (resolu_value, file_path)
    except ValueError as e:
        print(f"Erreur lors de la gestion du fichier resolu {file}: {e}")

def move_selected_files(files_dict, target_dir):
    for _, file_info in files_dict.items():
        try:
            _, file_path = file_info
            move_file(file_path, target_dir)
        except Exception as e:
            print(f"Erreur lors du déplacement du fichier {file_path}: {e}")

def move_file(file_path, target_dir):
    try:
        shutil.move(file_path, os.path.join(target_dir, os.path.basename(file_path)))
    except OSError as e:
        print(f"Erreur lors du déplacement du fichier {file_path} vers {target_dir}: {e}")

def process_directory(root_dir):
    for subdir, _, files in os.walk(root_dir):
        if any(ignored in subdir for ignored in ignored_subdirs):
            continue
        process_files_in_directory(subdir, files)

# Spécifier le répertoire racine
root_directory = '/path/to/your/root_directory'

# Traiter le répertoire
process_directory(root_directory)

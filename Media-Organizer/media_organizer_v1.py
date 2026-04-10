import os
import re
import shutil

# === CONFIGURATION ===
base_folder = "/storage/emulated/0/movie box"
movies_folder = os.path.join(base_folder, "Movies")
subtitles_folder = os.path.join(base_folder, "Subtitles")
subtitle_extension = ".srt"

def clean_name(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'(480P|720P|1080P|360P|English)', '', name, flags=re.IGNORECASE)
    name = name.replace("_", " ").strip()
    return name

def extract_show_info(filename):
    name = clean_name(filename)
    match = re.search(r'[Ss](\d+)[ _-]?[Ee](\d+)', name)
    if match:
        season, episode = match.groups()
        show_name = re.split(r'[Ss]\d+[ _-]?[Ee]\d+', name)[0].strip(" -_")
        return show_name.strip(), season.lstrip("0") or "0", episode.lstrip("0") or "0"
    else:
        return name.strip(), None, None

def normalize_show_name(name):
    return re.sub(r'[\s_-]+', '', name.lower())

movie_files = [os.path.join(r, f) for r, _, fs in os.walk(movies_folder) for f in fs if f.lower().endswith(".mp4")]
subtitle_files = [os.path.join(r, f) for r, _, fs in os.walk(subtitles_folder) for f in fs if f.lower().endswith((".srt", ".sub", ".ass"))]

for movie_path in movie_files:
    movie = os.path.basename(movie_path)
    m_show, m_season, m_episode = extract_show_info(movie)

    if m_season and m_episode:
        movie_newname = f"{m_show} S{int(m_season):02d} E{int(m_episode):02d}.mp4"
    else:
        movie_newname = f"{m_show}.mp4"

    new_movie_path = os.path.join(os.path.dirname(movie_path), movie_newname)

    if movie_path != new_movie_path:
        os.rename(movie_path, new_movie_path)

    best_sub = None
    for sub_path in subtitle_files:
        sub = os.path.basename(sub_path)
        s_show, s_season, s_episode = extract_show_info(sub)

        if m_season and m_episode: 
            if s_show and normalize_show_name(s_show) == normalize_show_name(m_show) and s_season == m_season and s_episode == m_episode:
                best_sub = sub_path
                break
        else: 
            if normalize_show_name(s_show) == normalize_show_name(m_show):
                best_sub = sub_path
                break

    if best_sub:
        subtitle_newname = f"{m_show} S{int(m_season):02d} E{int(m_episode):02d}{subtitle_extension}" if m_season else f"{m_show}{subtitle_extension}"
        dst_sub = os.path.join(os.path.dirname(new_movie_path), subtitle_newname)
        shutil.copy(best_sub, dst_sub)

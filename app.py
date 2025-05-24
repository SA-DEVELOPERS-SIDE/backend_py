from flask import Flask, request, jsonify
import yt_dlp
import os


app = Flask(__name__)

def ytdlp_options(flat=True, search_count=10):
    return {
        'quiet': True,
        'extract_flat': flat,
        'skip_download': True,
        'default_search': f'ytsearch{search_count}'
    }

@app.route('/artists')
def fetch_artists():
    query = request.args.get('q', None)
    if not query:
        query = 'ytsearch10:tamil music artists'
    elif not query.startswith('ytsearch'):
        query = 'ytsearch10:' + query

    try:
        with yt_dlp.YoutubeDL(ytdlp_options(flat=True, search_count=20)) as ydl:
            result = ydl.extract_info(query, download=False)
            print("DEBUG artists result:", result)
            return jsonify(result.get('entries', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/songs')
def fetch_songs():
    query = request.args.get('q', None)
    if not query:
        query = 'ytsearch10:latest tamil songs 2025'
    elif not query.startswith('ytsearch'):
        query = 'ytsearch10:' + query

    with yt_dlp.YoutubeDL(ytdlp_options(flat=True, search_count=20)) as ydl:
        result = ydl.extract_info(query, download=False)
        print("DEBUG result:", result)
        return jsonify(result.get('entries', []))


@app.route('/playlists')
def fetch_playlists():
    query = request.args.get('q', None)
    if not query:
        query = 'ytsearch10:tamil songs playlist'
    elif not query.startswith('ytsearch'):
        query = 'ytsearch10:' + query

    try:
        with yt_dlp.YoutubeDL(ytdlp_options(flat=True, search_count=20)) as ydl:
            result = ydl.extract_info(query, download=False)
            print("DEBUG playlists result:", result)
            return jsonify(result.get('entries', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/playlistId/songs')
def fetch_playlist_songs():
    playlist_url = request.args.get('url')
    if not playlist_url:
        return jsonify({'error': 'Missing playlist URL'}), 400

    try:
        with yt_dlp.YoutubeDL(ytdlp_options()) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            print("DEBUG playlist songs result:", result)
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/artist/songs')
def fetch_artist_songs():
    artist_name = request.args.get('q')
    if not artist_name:
        return jsonify({'error': 'Missing artist name'}), 400

    query = artist_name.strip()
    if not query.startswith('ytsearch'):
        query = f'ytsearch10:{query} tamil songs'

    try:
        with yt_dlp.YoutubeDL(ytdlp_options(flat=True, search_count=20)) as ydl:
            result = ydl.extract_info(query, download=False)
            print("DEBUG artist songs result:", result)
            return jsonify(result.get('entries', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/searchsinglesong')
def fetch_single_song():
    song_name = request.args.get('q')
    if not song_name:
        return jsonify({'error': 'Missing song name'}), 400

    query = song_name.strip()
    if not query.startswith('ytsearch'):
        query = f'ytsearch1:{query} tamil song'

    try:
        with yt_dlp.YoutubeDL(ytdlp_options(search_count=1, flat=True)) as ydl:
            result = ydl.extract_info(query, download=False)
            print("DEBUG single song result:", result)
            # return the first entry if available
            entries = result.get('entries', [])
            return jsonify(entries[0] if entries else {})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/shorts')
def fetch_shorts():
    query = request.args.get('q', 'tamil shorts songs')
    opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'default_search': f'ytsearch20:{query}'
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            result = ydl.extract_info(f"ytsearch20:{query}", download=False)
            shorts = []
            for video in result.get('entries', []):
                duration = video.get('duration')
                if duration is not None and duration <= 60:
                    shorts.append(video)
            return jsonify(shorts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
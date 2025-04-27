from flask import Flask, render_template, request

app = Flask(__name__)

# Expanded song database with vocal ranges
SONGS_DB = {
    "My Heart Will Go On": {"artist": "Celine Dion", "range": "E3-E5"},
    "Sweet Caroline": {"artist": "Neil Diamond", "range": "B2-G4"},
    "I Will Always Love You": {"artist": "Whitney Houston", "range": "C3-B5"},
    "Bohemian Rhapsody": {"artist": "Queen", "range": "F3-G5"},
    "Let It Go": {"artist": "Idina Menzel", "range": "F3-D5"},
    "I Want It That Way": {"artist": "Backstreet Boys", "range": "D3-A4"},
    "Don't Stop Believin'": {"artist": "Journey", "range": "E3-B4"},
    "Wonderwall": {"artist": "Oasis", "range": "C3-G4"},
    "Sweet Home Alabama": {"artist": "Lynyrd Skynyrd", "range": "D3-A4"},
    "Hey Jude": {"artist": "The Beatles", "range": "C3-C5"},
    "Sweet Dreams": {"artist": "Eurythmics", "range": "F3-C5"},
    "Hotel California": {"artist": "Eagles", "range": "E3-A4"},
    "Sweet Child O' Mine": {"artist": "Guns N' Roses", "range": "D3-B4"},
    "Yesterday": {"artist": "The Beatles", "range": "C3-G4"},
    "Let It Be": {"artist": "The Beatles", "range": "C3-C5"},
    "Imagine": {"artist": "John Lennon", "range": "E3-F4"},
    "Stand By Me": {"artist": "Ben E. King", "range": "C3-A4"},
    "Can't Help Falling in Love": {"artist": "Elvis Presley", "range": "D3-B4"}
}

# Define the order of musical notes for comparison
NOTES_ORDER = [
    "C2", "D2", "E2", "F2", "G2", "A2", "B2",
    "C3", "D3", "E3", "F3", "G3", "A3", "B3",
    "C4", "D4", "E4", "F4", "G4", "A4", "B4",
    "C5", "D5", "E5", "F5", "G5", "A5", "B5"
]
# Create a mapping for quick index lookup
NOTE_INDEX = {note: index for index, note in enumerate(NOTES_ORDER)}

# Define the notes available for selection in the dropdowns
LOW_NOTES = [n for n in NOTES_ORDER if n[1] in ('2', '3')]
HIGH_NOTES = [n for n in NOTES_ORDER if n[1] in ('4', '5')]

def is_song_in_range(song_range, user_low, user_high):
    """Checks if a song's range is within the user's selected range."""
    try:
        song_low_str, song_high_str = song_range.split('-')

        # Get the index (numerical representation) of each note
        song_low_idx = NOTE_INDEX.get(song_low_str)
        song_high_idx = NOTE_INDEX.get(song_high_str)
        user_low_idx = NOTE_INDEX.get(user_low)
        user_high_idx = NOTE_INDEX.get(user_high)

        # Check if any note wasn't found in our defined order (error handling)
        if None in [song_low_idx, song_high_idx, user_low_idx, user_high_idx]:
            print(f"Warning: Could not compare range for song range '{song_range}' "
                  f"with user range '{user_low}-{user_high}'. Skipping.")
            return False

        # The song's lowest note must be >= user's lowest note
        # The song's highest note must be <= user's highest note
        return song_low_idx >= user_low_idx and song_high_idx <= user_high_idx

    except ValueError:
        print(f"Warning: Invalid range format for song: '{song_range}'. Skipping.")
        return False
    except Exception as e:
        print(f"An error occurred during range check: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    suitable_songs = None
    selected_low = "C3"  # Default value
    selected_high = "C5" # Default value
    error_message = None

    if request.method == 'POST':
        selected_low = request.form.get('lowest_note')
        selected_high = request.form.get('highest_note')

        if not selected_low or not selected_high:
            error_message = "Please select both lowest and highest notes."
        # Optional: Add check to ensure highest >= lowest
        elif NOTE_INDEX.get(selected_low, -1) > NOTE_INDEX.get(selected_high, -1):
             error_message = "Highest note cannot be lower than the lowest note."
        else:
            suitable_songs = []
            for song, details in SONGS_DB.items():
                if is_song_in_range(details["range"], selected_low, selected_high):
                    suitable_songs.append({
                        "title": song,
                        "artist": details["artist"],
                        "range": details["range"]
                    })

    # Pass data to the template
    return render_template(
        'index.html',
        low_notes=LOW_NOTES,
        high_notes=HIGH_NOTES,
        selected_low=selected_low,
        selected_high=selected_high,
        songs=suitable_songs,
        error=error_message
    )

if __name__ == "__main__":
    app.run(debug=True) # debug=True is helpful during development
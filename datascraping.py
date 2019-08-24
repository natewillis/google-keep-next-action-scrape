import gkeepapi
import json
from decouple import config

if __name__ == '__main__':

    # Login to keep
    keep = gkeepapi.Keep()
    keep.login(config('GOOGLE_USERNAME'), config('GOOGLE_APP_PASSWORD'))  #

    # Get Notes
    gnotes = keep.find(labels=[keep.findLabel('!Next actions')], archived=False)

    # Store data
    note_titles_by_label = {}
    for note in gnotes:
        title = note.title if note.title else note.text
        note_labels = [label.name for label in note.labels.all() if label.name != '!Next actions']
        dict_key = '-'.join(note_labels) if len(note_labels)>0 else 'Other'
        if not dict_key in note_titles_by_label:
            note_titles_by_label[dict_key] = []
        note_titles_by_label[dict_key].append(title)

    # Save to disk
    f = open(config('JSON_SAVE_PATH'), 'w')
    f.write(json.dumps(note_titles_by_label))
    f.close()


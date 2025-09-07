def get_changed_sentences(original: dict, updated: dict):
    changed = {"sentences": []}

    original_map = {s["id"]: s["text"] for s in original["sentences"]}

    for upd in updated["sentences"]:
        orig_text = original_map.get(upd["id"])
        if orig_text != upd["text"]: 
            changed["sentences"].append({
                "id": upd["id"],
                "from_sentence": orig_text,
                "to_sentence": upd["text"],
                "bold_words": upd.get("bold_words", []),
                "italic_words": upd.get("italic_words", [])
            })

    return changed

from palette.ranking import Entry, rank, score


def entry(label, path="", shortcut=""):
    return Entry(name=label.lower().replace(" ", "_"), label=label, path=path, shortcut=shortcut)


def test_empty_query_scores_zero():
    assert score("", "Anything") == 0


def test_non_subsequence_does_not_match():
    assert score("zq", "Brush Settings") is None


def test_matching_is_case_insensitive_and_ignores_spaces():
    assert score("NEW LAY", "New Layer") is not None


def test_word_start_beats_scattered_match():
    assert score("nl", "New Layer") > score("nl", "Insert Colorless")


def test_contiguous_beats_gapped():
    assert score("lay", "Layer") > score("lay", "Lock All Yellow")


def test_rank_orders_by_score_then_label():
    entries = [entry("Brush Settings"), entry("Brush Size Up"), entry("Rotate Canvas")]
    ranked = rank("brush", entries)
    assert [item.label for item in ranked] == ["Brush Settings", "Brush Size Up"]


def test_empty_query_lists_everything_alphabetically():
    entries = [entry("Zoom In"), entry("Add Layer"), entry("Mirror")]
    assert [item.label for item in rank("", entries)] == ["Add Layer", "Mirror", "Zoom In"]


def test_path_is_searched_too():
    entries = [entry("Gaussian Blur", path="Filter > Blur"), entry("Rotate", path="Image")]
    assert [item.label for item in rank("filter blur", entries)] == ["Gaussian Blur"]


def test_label_matches_beat_path_only_matches():
    entries = [entry("Flatten image", path="Layer"), entry("Add Layer", path="Layer > New")]
    assert [item.label for item in rank("layer", entries)] == ["Add Layer", "Flatten image"]


def test_limit_caps_the_results():
    entries = [entry(f"Item {i}") for i in range(50)]
    assert len(rank("item", entries, limit=10)) == 10

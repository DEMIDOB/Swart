IGNORED_WORDS = {"with", "and"}
IGNORED_SYMBOLS = {";"}

NEW_LEVEL_SYMBOLS = {
    # "\"": "\"",
    # "'": "'",
    "[": "]",
    # "{": "}",
    "(": ")"
}


def split_on_current_level(src, global_offsets, capture_offsets=False, inverse=True):
    levels_stack = []
    levels_start_idx = []

    current_local_symbol_offset_idx = -1
    split = []
    split_offsets = []

    current_word = ""
    everything_is_a_word = False

    def _l_add_word():
        nonlocal split, split_offsets, current_word

        if current_word not in IGNORED_WORDS:
            split_offsets.append(global_offsets[current_local_symbol_offset_idx])
            split.append(current_word.strip())

        current_word = ""

    for c in src:
        current_local_symbol_offset_idx += 1

        if not everything_is_a_word and c in IGNORED_SYMBOLS and not levels_stack:
            continue

        if c == "\"" and not everything_is_a_word and not levels_stack:
            everything_is_a_word = True
            continue

        if c == "\"" and everything_is_a_word:
            everything_is_a_word = False
            _l_add_word()
            continue

        if everything_is_a_word:
            current_word += c
            continue

        if c == " " and not levels_stack and current_word and not everything_is_a_word:
            _l_add_word()
        else:
            current_word += c

        if c in NEW_LEVEL_SYMBOLS:
            levels_stack.append(NEW_LEVEL_SYMBOLS[c])
            levels_start_idx.append(global_offsets[current_local_symbol_offset_idx])
        elif levels_stack and c == levels_stack[-1]:
            levels_stack.pop()
            levels_start_idx.pop()

    if current_word:
        _l_add_word()

    assert not levels_stack, f"Error in symbol #{levels_start_idx[-1]}"

    if inverse:
        split = split[::-1]
        split_offsets = split_offsets[::-1]

    if capture_offsets:
        return split, split_offsets
    else:
        return split

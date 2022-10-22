IGNORED_WORDS = {"with", "and"}
IGNORED_SYMBOLS = {";"}

NEW_SCOPE_SYMBOLS = {
    # "\"": "\"",
    # "'": "'",
    "[": "]",
    # "{": "}",
    "(": ")"
}


def split_for_current_scope(src, global_offsets, capture_offsets=False, inverse=True):
    scopes_stack = []
    scopes_start_idx = []

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

        if not everything_is_a_word and c in IGNORED_SYMBOLS and not scopes_stack:
            continue

        if c == "\"" and not everything_is_a_word and not scopes_stack:
            everything_is_a_word = True
            continue

        if c == "\"" and everything_is_a_word:
            everything_is_a_word = False
            _l_add_word()
            continue

        if everything_is_a_word:
            current_word += c
            continue

        if c == " " and not scopes_stack and current_word and not everything_is_a_word:
            _l_add_word()
        else:
            current_word += c

        if c in NEW_SCOPE_SYMBOLS:
            scopes_stack.append(NEW_SCOPE_SYMBOLS[c])
            scopes_start_idx.append(global_offsets[current_local_symbol_offset_idx])
        elif scopes_stack and c == scopes_stack[-1]:
            scopes_stack.pop()
            scopes_start_idx.pop()

    if current_word:
        _l_add_word()

    assert not scopes_stack, f"Error in symbol #{scopes_start_idx[-1]}"

    if inverse:
        split = split[::-1]
        split_offsets = split_offsets[::-1]

    if capture_offsets:
        return split, split_offsets
    else:
        return split

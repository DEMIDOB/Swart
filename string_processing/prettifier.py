NEW_LEVEL_SYMBOLS = {
    "[": "]",
    "{": "}",
    "(": ")"
}


def prettify(src: str, tab="    "):
    # return src
    level_stack = []
    pretty_src = ""

    level = 0

    for line in src.split("\n"):
        # print(line)
        for c in line:
            if c in NEW_LEVEL_SYMBOLS:
                level_stack.append(NEW_LEVEL_SYMBOLS[c])

            if level_stack and c == level_stack[-1]:
                level_stack.pop()

        if len(level_stack) < level:
            level = len(level_stack)

        pretty_src += tab * level + line + "\n"
        level = len(level_stack)

    assert not level_stack, level_stack

    return pretty_src

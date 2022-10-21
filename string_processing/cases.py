def snake_to_camel(string: str):
    out = ""
    for part in string.split("_"):
        if not part:
            continue
        out += part[0].capitalize() + part[1:].lower()
    return out[0].lower() + out[1:]


if __name__ == '__main__':
    print(snake_to_camel("dkjf_"))
    print(snake_to_camel("bottom_right"))

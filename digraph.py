# Drop this in .local/share/weechat/python/autoload/
import weechat

# Substrings surrounded by this will have replacement active
MODIFIER = "$"

weechat.register("digraph", "narodnik", "1.0", "GPL3",
                 "Digraphs like nvim for inputting math symbols",
                 "", "")

weechat.hook_modifier("input_text_display", "modifier_cb", "")

sup_vals = "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ⁺⁻⁼⁽⁾"
sup_keys = "0123456789abcdefghijklmnoprstuvwxyz+-=()"

sub_vals = "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
sub_keys = "0123456789+-=()"

symbols = [
    ("ZZ", "ℤ"),
    ("QQ", "ℚ"),
    ("FF", "𝔽"),
    ("a:", "𝔞"),
    ("b:", "𝔟"),
    ("c:", "𝔠"),
    ("p:", "𝔭"),
    ("in", "∈"),
    ("ni", "∉"),
    ("(_", "⊆"),
    ("(<", "⊊"),
    ("(!", "⊈"),
    (":.", "·"),
    (".,", "…"),
    (".3", "⋯"),
    ("**", "×"),
    ("i8", "∞"),
    ("</", "⟨"),
    ("/>", "⟩"),
    ("ff", "ϕ"),
    ("=>", "⇒"),
    ("==", "⇔"),
    ("->", "→"),
    ("TE", "∃"),
    ("!=", "≠"),
    ("=3", "≡"),
    ("=<", "≤"),
    ("<=", "≤"),
    (">=", "≥"),
    ("=?", "≌"),
    ("RT", "√"),
    ("(U", "∩"),
]

greek_key = "abcdefghiklmnopqrstuwxyz"
greek_cap = "ΑΒΞΔΕΦΓΘΙΚΛΜΝΟΠΨΡΣΤΥΩΧΗΖ"
greek_min = "αβξδεφγθικλμνοπψρστυωχηζ"

START_EXPR = 1
END_EXPR = 2

def build_replacement_table():
    table = []
    table.extend(symbols)
    # Superscript
    for key, val in zip(sup_keys, sup_vals):
        table.append((f"^{key}", val))
    # Subscript
    for key, val in zip(sub_keys, sub_vals):
        table.append((f"_{key}", val))
    # Greek letters
    assert greek_key == greek_key.lower()
    for key, cap, min in zip(greek_key, greek_cap, greek_min):
        table.append((f"{key.upper()}*", cap))
        table.append((f"{key}*", min))
    return table

replacement_table = build_replacement_table()

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def replace_symbols(a_str):
    for key, value in replacement_table:
        a_str = a_str.replace(key, value)
    return a_str

def lexer(string):
    tokens = []
    last_pos = 0
    for pos in find_all(string, MODIFIER):
        tokens.append(string[last_pos:pos - len(MODIFIER) + 1])
        tokens.append(MODIFIER)
        last_pos = pos + len(MODIFIER)
    if last_pos < len(string):
        tokens.append(string[last_pos:])

    active = False
    for i, token in enumerate(tokens):
        if token == MODIFIER:
            if not active:
                tokens[i] = START_EXPR
            else:
                tokens[i] = END_EXPR
            active = not active

    return tokens

def compile(tokens):
    state = END_EXPR
    result = ""
    current_word = None
    is_last = lambda i: i == len(tokens) - 1
    for i, token in enumerate(tokens):
        if token == START_EXPR:
            assert state == END_EXPR
            result += current_word
            current_word = None
            # When at the very last token, keep the unclosed MODIFIER
            if is_last(i):
                result += MODIFIER
            # Now change state to open expr
            state = START_EXPR
        elif token == END_EXPR:
            assert state == START_EXPR
            # Close the prev expr
            result += replace_symbols(current_word)
            current_word = None
            # Re-open normal mode
            state = END_EXPR
        else:
            assert state in (START_EXPR, END_EXPR)
            assert current_word is None
            current_word = token
    if current_word is not None:
        if state == START_EXPR:
            result += MODIFIER
            result += replace_symbols(current_word)
        else:
            assert state == END_EXPR
            result += current_word
    return result

def modifier_cb(data, modifier, modifier_data, string):
    tokens = lexer(string)
    result = compile(tokens)
    return result


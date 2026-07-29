from cost_estimator.tokenizer import count_tokens


def test_known_count_hello_world():
    assert count_tokens("Hello, world!") == 4


def test_empty_string_has_zero_tokens():
    assert count_tokens("") == 0


def test_single_word():
    assert count_tokens("tokens") == 1


def test_known_count_pangram():
    assert count_tokens("The quick brown fox jumps over the lazy dog.") == 10


def test_deterministic_repeat_calls():
    text = "Repeat this prompt twice and compare the token counts."
    assert count_tokens(text) == count_tokens(text)

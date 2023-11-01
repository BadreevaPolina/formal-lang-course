import os

from pyformlang.cfg import CFG

from project.weak_cnf import to_weak_cnf, weak_cnf_from_file


def are_equal(actual, expected):
    actual_set = {line.strip() for line in actual.splitlines() if line.strip() != ""}
    expected_set = {
        line.strip() for line in expected.splitlines() if line.strip() != ""
    }
    assert actual_set == expected_set


def test_to_weak_cnf_1():
    cfg_text = "S -> A B\nA -> a\nB -> b\n"
    cfg = CFG.from_text(cfg_text)
    weak_cnf = to_weak_cnf(cfg).to_text()
    are_equal(weak_cnf, cfg_text)


def test_to_weak_cnf_2():
    cfg_text = "S -> A B | C\nC -> A\nA -> a\nB -> b\n"
    expected = "S -> A B\nS -> a\nA -> a\nB -> b\n"
    actual = to_weak_cnf(CFG.from_text(cfg_text)).to_text()
    are_equal(actual, expected)


def test_to_weak_cnf_3():
    cfg_text = "S -> A | b\nA -> a\n"
    expected = "S -> a\nS -> b\n"
    actual = to_weak_cnf(CFG.from_text(cfg_text)).to_text()
    are_equal(actual, expected)


def test_to_weak_cnf_4():
    cfg_text = "S -> A B\nA -> a\nB -> b | eps\n"
    expected = "S -> A B\nA -> a\nB -> b\nB -> eps\n"
    actual = to_weak_cnf(CFG.from_text(cfg_text)).to_text()
    are_equal(actual, expected)


def test_weak_cnf_from_file_1():
    filename = "cnf.txt"
    expected = "S -> A B\nA -> a\nB -> b\n"
    with open(filename, "w") as f:
        f.write(expected)
    actual = weak_cnf_from_file(filename).to_text()
    os.remove(filename)
    are_equal(actual, expected)


def test_weak_cnf_from_file_2():
    filename = "cnf.txt"
    cfg_text = "S -> A B | C\nA -> a\nD -> C C\nD -> d A\nB -> b\n"
    expected = "S -> A B\nA -> a\nB -> b\n"
    with open(filename, "w") as f:
        f.write(cfg_text)
    actual = weak_cnf_from_file(filename).to_text()
    os.remove(filename)
    are_equal(actual, expected)

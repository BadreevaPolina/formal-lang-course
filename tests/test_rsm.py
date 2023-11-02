import os

from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex

from project.ecfg import ECFG
from project.rsm import RSM


def are_equal(actual, expected):
    assert set(actual).difference(set(expected)) == set()


def test_ecfg_cfg_1():
    example = "S -> A b C\nA -> a\nC -> c\n"
    cfg = CFG.from_text(example)
    actual_ecfg_cfg = ECFG().ecfg_from_cfg(cfg)

    expected_ecfg = {
        Variable("S"): Regex("A.b.C"),
        Variable("A"): Regex("a"),
        Variable("C"): Regex("c"),
    }
    are_equal(actual_ecfg_cfg.productions, expected_ecfg)


def test_ecfg_file_1():
    example = "S -> A b C\nA -> a\nC -> c\n"
    filename = "cnf.txt"
    with open(filename, "w") as f:
        f.write(example)
    actual_ecfg_file = ECFG().ecfg_from_file(filename)
    os.remove(filename)

    expected_ecfg = {
        Variable("S"): Regex("A.b.C"),
        Variable("A"): Regex("a"),
        Variable("C"): Regex("c"),
    }
    are_equal(actual_ecfg_file.productions, expected_ecfg)


def test_ecfg_text_1():
    example = "S -> A b C\nA -> a\nC -> c\n"
    actual_ecfg_text = ECFG().ecfg_from_text(example)

    expected_ecfg = {
        Variable("S"): Regex("A.b.C"),
        Variable("A"): Regex("a"),
        Variable("C"): Regex("c"),
    }
    are_equal(actual_ecfg_text.productions, expected_ecfg)


def test_rsm_from_ecfg_1():
    example = "S -> A b C\nA -> a\nC -> c\n"
    cfg = CFG.from_text(example)
    actual_ecfg_cfg = ECFG().ecfg_from_cfg(cfg)
    actual_rsm = RSM().rsm_from_ecfg(actual_ecfg_cfg)
    expected_ecfg = ECFG(
        Variable("S"),
        {
            Variable("S"): Regex("A.b.C"),
            Variable("A"): Regex("a"),
            Variable("C"): Regex("c"),
        },
    )
    expected_rsm = RSM().rsm_from_ecfg(expected_ecfg)
    assert actual_rsm.boxes == expected_rsm.boxes


def test_rsm_from_ecfg_minimize_1():
    example = "S -> A b C\nA -> a\nC -> c\n"
    cfg = CFG.from_text(example)
    actual_ecfg_cfg = ECFG().ecfg_from_cfg(cfg)
    actual_rsm = RSM().rsm_from_ecfg(actual_ecfg_cfg).minimize()
    expected_ecfg = ECFG(
        Variable("S"),
        {
            Variable("S"): Regex("A.b.C"),
            Variable("A"): Regex("a"),
            Variable("C"): Regex("c"),
        },
    )
    expected_rsm = RSM().rsm_from_ecfg(expected_ecfg).minimize()
    assert actual_rsm.boxes == expected_rsm.boxes


def test_ecfg_cfg_2():
    example = "S -> a B\nB -> C\nC -> D\nD -> a\n"
    cfg = CFG.from_text(example)
    actual_ecfg_cfg = ECFG().ecfg_from_cfg(cfg)

    expected_ecfg = {
        Variable("S"): Regex("a.B"),
        Variable("B"): Regex("C"),
        Variable("C"): Regex("D"),
        Variable("D"): Regex("a"),
    }
    are_equal(actual_ecfg_cfg.productions, expected_ecfg)


def test_ecfg_file_2():
    example = "S -> a B\nB -> C\nC -> D\nD -> a\n"
    filename = "cnf.txt"
    with open(filename, "w") as f:
        f.write(example)
    actual_ecfg_file = ECFG().ecfg_from_file(filename)
    os.remove(filename)

    expected_ecfg = {
        Variable("S"): Regex("a.B"),
        Variable("B"): Regex("C"),
        Variable("C"): Regex("D"),
        Variable("D"): Regex("a"),
    }
    are_equal(actual_ecfg_file.productions, expected_ecfg)


def test_ecfg_text_2():
    example = "S -> a B\nB -> C\nC -> D\nD -> a\n"
    actual_ecfg_text = ECFG().ecfg_from_text(example)

    expected_ecfg = {
        Variable("S"): Regex("a.B"),
        Variable("B"): Regex("C"),
        Variable("C"): Regex("D"),
        Variable("D"): Regex("a"),
    }
    are_equal(actual_ecfg_text.productions, expected_ecfg)


def test_rsm_from_ecfg_2():
    example = "S -> a B\nB -> C\nC -> D\nD -> a\n"
    cfg = CFG.from_text(example)
    actual_ecfg_cfg = ECFG().ecfg_from_cfg(cfg)
    actual_rsm = RSM().rsm_from_ecfg(actual_ecfg_cfg)
    expected_ecfg = ECFG(
        Variable("S"),
        {
            Variable("S"): Regex("a.B"),
            Variable("B"): Regex("C"),
            Variable("C"): Regex("D"),
            Variable("D"): Regex("a"),
        },
    )
    expected_rsm = RSM().rsm_from_ecfg(expected_ecfg)
    assert actual_rsm.boxes == expected_rsm.boxes


def test_rsm_from_ecfg_minimize_2():
    example = "S -> a B\nB -> C\nC -> D\nD -> a\n"
    cfg = CFG.from_text(example)
    actual_ecfg_cfg = ECFG().ecfg_from_cfg(cfg)
    actual_rsm = RSM().rsm_from_ecfg(actual_ecfg_cfg).minimize()
    expected_ecfg = ECFG(
        Variable("S"),
        {
            Variable("S"): Regex("a.B"),
            Variable("B"): Regex("C"),
            Variable("C"): Regex("D"),
            Variable("D"): Regex("a"),
        },
    )
    expected_rsm = RSM().rsm_from_ecfg(expected_ecfg).minimize()
    assert actual_rsm.boxes == expected_rsm.boxes

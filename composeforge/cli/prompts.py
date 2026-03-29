"""
composeforge.cli.prompts
~~~~~~~~~~~~~~~~~~~~~~~~~
Interactive CLI prompts for collecting user input.
"""

from typing import List, Optional

from composeforge.cli.colors import C, warn


def ask(question: str, default: Optional[str] = None) -> Optional[str]:
    """Pose une question avec une valeur par défaut optionnelle."""
    d = f" [{C.CY}{default}{C.RS}]" if default else ""
    ans = input(f"\n{C.Y}▶{C.RS} {question}{d}: ").strip()
    return ans if ans else default


def ask_choice(question: str, choices: List[str]) -> int:
    """Propose un choix unique parmi une liste. Retourne l'index (0-based)."""
    print(f"\n{C.Y}▶{C.RS} {question}")
    for i, c in enumerate(choices, 1):
        print(f"  {C.CY}{i}.{C.RS} {c}")
    while True:
        v = input(f"  Votre choix (1-{len(choices)}): ").strip()
        if v.isdigit() and 1 <= int(v) <= len(choices):
            return int(v) - 1
        warn("Choix invalide, réessayez.")


def ask_multi(question: str, choices: List[str]) -> List[int]:
    """Propose un choix multiple. Retourne la liste d'index (0-based, triés)."""
    print(f"\n{C.Y}▶{C.RS} {question}")
    for i, c in enumerate(choices, 1):
        print(f"  {C.CY}{i}.{C.RS} {c}")
    print(f"  {C.B}(ex: 1 3 4  |  'all' pour tout  |  '0' pour aucun){C.RS}")
    while True:
        v = input("  Vos choix: ").strip()
        if v == "0":
            return []
        if v == "all":
            return list(range(len(choices)))
        parts = v.split()
        if all(p.isdigit() and 1 <= int(p) <= len(choices) for p in parts):
            return sorted(set(int(p) - 1 for p in parts))
        warn("Choix invalide, réessayez.")

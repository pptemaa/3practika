#!/usr/bin/env python3
"""
Ассемблер для учебной виртуальной машины (УВМ), вариант 18.
Этап 1: перевод JSON-программы в промежуточное представление (A, B, C).

Поддерживаемые команды:
- load_const : A = 39, B = константа,      C = адрес
- read_mem   : A = 30, B = адрес источника, C = адрес назначения
- write_mem  : A = 22, B = адрес источника, C = адрес назначения
- popcnt     : A = 61, B = адрес источника, C = адрес результата
"""

import json
import sys


class Assembler:
    def __init__(self):
        self.instructions = []

    def parse(self, text):
        """Разобрать JSON-программу."""
        try:
            program = json.loads(text)
        except json.JSONDecodeError as e:
            raise SyntaxError("Ошибка JSON: " + str(e))

        if not isinstance(program, list):
            raise SyntaxError("Программа должна быть списком команд")

        self.instructions = []

        for i, cmd in enumerate(program):
            # допускаем комментарии вида { "_comment": "..." }
            if isinstance(cmd, dict) and "_comment" in cmd and len(cmd) == 1:
                continue

            self.instructions.append(self.parse_command(cmd, i))

        return self.instructions

    def parse_command(self, cmd, num):
        """Разобрать одну команду и вернуть A, B, C."""
        if not isinstance(cmd, dict):
            raise SyntaxError(f"Команда {num}: должна быть объектом JSON")

        if "op" not in cmd:
            raise SyntaxError(f"Команда {num}: отсутствует поле 'op'")

        op = str(cmd["op"]).lower()

        if op == "load_const":
            if "const" not in cmd or "addr" not in cmd:
                raise SyntaxError(f"Команда {num}: load_const требует 'const' и 'addr'")
            return {"A": 39, "B": cmd["const"], "C": cmd["addr"]}

        if op == "read_mem":
            if "src" not in cmd or "dst" not in cmd:
                raise SyntaxError(f"Команда {num}: read_mem требует 'src' и 'dst'")
            return {"A": 30, "B": cmd["src"], "C": cmd["dst"]}

        if op == "write_mem":
            if "src" not in cmd or "dst" not in cmd:
                raise SyntaxError(f"Команда {num}: write_mem требует 'src' и 'dst'")
            return {"A": 22, "B": cmd["src"], "C": cmd["dst"]}

        if op == "popcnt":
            if "src" not in cmd or "dst" not in cmd:
                raise SyntaxError(f"Команда {num}: popcnt требует 'src' и 'dst'")
            return {"A": 61, "B": cmd["src"], "C": cmd["dst"]}

        raise SyntaxError(f"Команда {num}: неизвестная операция '{op}'")

    def get_test_output(self):
        """Вывести внутреннее представление (режим тестирования)."""
        return "\n".join(
            f"A={i['A']} B={i['B']} C={i['C']}" for i in self.instructions
        )


def main():
    # python assembler.py input.json output.json [--test]
    if len(sys.argv) < 3:
        print("Использование: python assembler.py input.json output.json [--test]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    test_mode = len(sys.argv) > 3 and sys.argv[3] == "--test"

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_path}' не найден")
        sys.exit(1)

    asm = Assembler()

    try:
        instructions = asm.parse(text)
    except SyntaxError as e:
        print("Ошибка ассемблера:", e)
        sys.exit(1)

    if test_mode:
        print(asm.get_test_output())

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(instructions, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print("Ошибка записи выходного файла:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

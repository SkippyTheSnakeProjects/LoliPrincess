import difflib
import utils


def get_move_info(name: str, moves: list):
    move_info = []
    for char_move in get_all_character_move_data().get(name):
        if char_move.get('Command') in moves and char_move not in move_info:
            move_info.append(char_move)

    return move_info


def get_characters_move_commands(name: str) -> list:
    move_data = get_all_character_move_data().get(name)
    moves = [x.get('Command') for x in move_data]
    return moves


def match_character_name(name: str) -> str:
    characters = get_character_list()
    match = difflib.get_close_matches(name.lower(), characters, 1)
    match = match[0] if len(match) >= 1 else None

    return match


def match_move_command(name: str, move: str) -> list:
    character_moves = get_characters_move_commands(name)
    matches = difflib.get_close_matches(move, character_moves)

    return matches


def get_character_list() -> dict:
    return utils.load_json('data/tekken/characters.json')


def get_all_character_move_data() -> dict:
    return utils.load_json('data/tekken/move_data.json')

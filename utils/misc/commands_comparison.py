from config_data.config import DEFAULT_COMMANDS


def commands_comparison(mode: str) -> str:
    """
    Creating the full description of the search mode command, which user chose
    :param mode: search mode command
    :return: the full description of the search mode command, which user chose
    """
    for i_command in DEFAULT_COMMANDS[3:6]:
        if i_command[0] == mode:
            desc = i_command[1]
            return desc

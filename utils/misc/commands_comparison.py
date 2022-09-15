from config_data.config import DEFAULT_COMMANDS


def commands_comparison(mode):
    for i_command in DEFAULT_COMMANDS[3:6]:
        if i_command[0] == mode:
            desc = i_command[1]
            return desc
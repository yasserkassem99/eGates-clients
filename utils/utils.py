from pathlib import Path
def general_message_header(msg_size,formating_length):
    return f"{msg_size:<{formating_length}}"

def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent
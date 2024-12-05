import importlib.resources
import essaygenie.utils as U


def load_prompt(prompt):
    """
    Load the specified prompt text file by filename and return its content.
    """
    with importlib.resources.path("essaygenie.prompts", f"{prompt}.txt") as prompt_path:
        return U.load_text(str(prompt_path))

def load_prompt_from_folder(folder, filename):
    """
    Load the specified prompt text file by folder plus filename  and return its content.
    """
    prompt_path = f"{folder}/{filename}.txt"
    return U.load_text(prompt_path)

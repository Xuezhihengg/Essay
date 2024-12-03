import importlib.resources
import essaygenie.utils as U


def load_prompt(prompt):
    with importlib.resources.path("essaygenie.prompts", f"{prompt}.txt") as prompt_path:
        return U.load_text(str(prompt_path))

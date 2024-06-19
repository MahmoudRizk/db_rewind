def from_env(variable_name):
    import os
    from dotenv import load_dotenv

    load_dotenv()

    return os.environ[variable_name]

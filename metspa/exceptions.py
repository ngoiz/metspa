"""Custom Exceptions"""


class EnvironmentVariableNotFoundError(Exception):
    """
    Exception raised when the requested environment variable has not been found

    Args:
        api_env_var_name (str): Name of the environment variable being retrieved.
    """

    def __init__(self, api_env_var_name: str):
        self.message = (
            f"Unable to find '{api_env_var_name}' in environment variables, please "
            "ensure you have added it to the current session\n\t"
            f"export {api_env_var_name}=your_token\nor through an environment file."
        )
        super().__init__(self.message)
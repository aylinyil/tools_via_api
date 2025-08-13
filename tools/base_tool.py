class BaseTool:
    """
    Base class for all tools.
    """

    def __init__(self, name: str):
        self.name = name

    def run(self, *args, **kwargs):
        """
        Run the tool with the given arguments.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
#!/usr/bin/python
import uuid


class Dependency:
    """This is a conceptual class to represent each dependency.

        :param library_name: Name of a library.
        :type library_name: str

        :param version: Version range of a library.
        :type version: str
        """
    def __init__(self, library_name, version):
        """Constructor method
        """
        self.library_name = library_name
        self.version = version
        self.id = uuid.uuid4()

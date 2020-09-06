#!/usr/bin/python
import uuid


class Dependency:

    def __init__(self, library_name, version, is_vulnerable):
        self.library_name = library_name
        self.version = version
        self.is_vulnerable = is_vulnerable
        self.id = uuid.uuid4()

    def __str__(self):
        return self.library_name + " - " + self.version + " - " + self.is_vulnerable

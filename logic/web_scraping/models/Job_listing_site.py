class JobListingSite:
    """This class is a representation of a job search site"""

    def __init__(self, name: str, url: str, full_description_element_identifier: str,
                 full_description_element_type: str):
        self._name = None
        self._url = None
        self._full_description_element_identifier = None
        self._full_description_element_type = None

        self.name = name
        self.url = url
        self.full_description_element_identifier = full_description_element_identifier
        self.full_description_element_type = full_description_element_type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # TODO: add validation
        self._name = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        # TODO: add validation
        self._url = value

    @property
    def full_description_element_identifier(self):
        return self._full_description_element_identifier

    @full_description_element_identifier.setter
    def full_description_element_identifier(self, value):
        # TODO: add validation
        self._full_description_element_identifier = value

    @property
    def full_description_element_type(self):
        return self._full_description_element_type

    @full_description_element_type.setter
    def full_description_element_type(self, value):
        # TODO: add validation
        self._full_description_element_type = value

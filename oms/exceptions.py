class OmsApiFillNumberNotFound(Exception):
    """
    Raised when fill number was not found on OMSAPI
    """


class OmsApiRunNumberNotFound(Exception):
    """
    Raised when fill number was not found on OMSAPI
    """


class OmsApiDataInvalidError(Exception):
    """
    Raised when data from OMS violates a constraint in our DB,
    e.g. Colliding bunches < 0
    """


class RunRegistryNoAvailableDatasets(Exception):
    """
    Raised when no datasets were found in RunRegistry
    for specific run number
    """


class RunRegistryReconstructionNotFound(Exception):
    """
    Raised when trying to get a non-existant reconstruction
    for a run
    """

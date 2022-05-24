class OmsApiFillNumberNotFound(Exception):
    """
    Raised when fill number was not found on OMSAPI
    """


class OmsApiRunNumberNotFound(Exception):
    """
    Raised when fill number was not found on OMSAPI
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

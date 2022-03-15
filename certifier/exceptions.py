class RunReconstructionIsAlreadyReference(Exception):
    """
    Exception raised when trying to promote reconstruction that is
    already reference
    """


class RunReconstructionNotYetCertified(Exception):
    """
    Exception raised when trying to promote Run reconstruction
    that has not been certified yet
    """

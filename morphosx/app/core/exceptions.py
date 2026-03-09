from fastapi import HTTPException, status


class MorphosXError(Exception):
    """Base exception for all MorphosX errors."""
    pass


class StorageError(MorphosXError):
    """Errors related to storage operations."""
    pass


class ProcessingError(MorphosXError):
    """Errors related to media processing."""
    pass


class SignatureError(MorphosXError):
    """Errors related to signature verification."""
    pass


def handle_morphosx_error(err: MorphosXError):
    """
    Map internal MorphosX errors to FastAPI HTTPExceptions.
    """
    if isinstance(err, StorageError):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Storage error: {str(err)}"
        )
    if isinstance(err, ProcessingError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Processing error: {str(err)}"
        )
    if isinstance(err, SignatureError):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid signature: {str(err)}"
        )
    
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Internal error: {str(err)}"
    )

from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_ERROR = "File type is not allowed"
    FILE_SIZE_ERROR = "File size exceeds the limit"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_UPLOADED_FAILED = "File uploaded failed"
    FILE_VALIDATED_SUCCESSFULLY = "File validated successfully"
    FILE_VALIDATED_FAILED = "File validated failed"
    FILE_NOT_FOUND = "File not found"
    FILE_PROCESSING_SUCCESSFULLY = "File processing successfully"
    FILE_PROCESSING_FAILED = "File processing failed"
 
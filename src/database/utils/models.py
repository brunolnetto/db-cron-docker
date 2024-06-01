from datetime import datetime
from typing import List
from uuid import uuid4

from database.models import AuditDB

def create_new_audit(
    table_name:str, 
    filenames: List[str], 
    size_bytes:int, 
    update_at:datetime
) -> AuditDB:
    """
    Creates a new audit entry.

    Args:
        name (str): The name of the file.
        size_bytes (int): The size of the file in bytes.
        update_at (datetime): The datetime when the source was last updated.

    Returns:
        AuditDB: An audit entry object.
    """
    return AuditDB(
        audi_id=uuid4(),
        audi_created_at=datetime.now(),
        audi_table_name=table_name,
        audi_filenames=filenames,
        audi_file_size_bytes=size_bytes,
        audi_source_updated_at=update_at,
        audi_downloaded_at=None,
        audi_processed_at=None,
        audi_inserted_at=None,
    )


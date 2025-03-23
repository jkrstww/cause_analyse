from pymilvus.bulk_writer import LocalBulkWriter, BulkFileType

def get_local_bulk_writer(schema):
    writer = LocalBulkWriter(
        schema=schema,
        local_path='.',
        segment_size=512 * 1024 * 1024, # Default value
        file_type=BulkFileType.PARQUET
    )

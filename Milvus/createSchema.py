from pymilvus import MilvusClient, DataType

def create_schema():
    schema = MilvusClient.create_schema(
        auto_id=True,
        enable_dynamic_field=True
    )

    DIM = 512

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True),

    # schema.add_field(field_name="bool", datatype=DataType.BOOL),
    # schema.add_field(field_name="int8", datatype=DataType.INT8),
    # schema.add_field(field_name="int16", datatype=DataType.INT16),
    # schema.add_field(field_name="int32", datatype=DataType.INT32),
    # schema.add_field(field_name="int64", datatype=DataType.INT64),
    # schema.add_field(field_name="float", datatype=DataType.FLOAT),
    # schema.add_field(field_name="double", datatype=DataType.DOUBLE),
    # schema.add_field(field_name="varchar", datatype=DataType.VARCHAR, max_length=512),
    # schema.add_field(field_name="json", datatype=DataType.JSON),
    # schema.add_field(field_name="array_str", datatype=DataType.ARRAY, max_capacity=100, element_type=DataType.VARCHAR, max_length=128)
    # schema.add_field(field_name="array_int", datatype=DataType.ARRAY, max_capacity=100, element_type=DataType.INT64)
    schema.add_field(field_name="float_vector", datatype=DataType.FLOAT_VECTOR, dim=DIM),
    # schema.add_field(field_name="binary_vector", datatype=DataType.BINARY_VECTOR, dim=DIM),
    # schema.add_field(field_name="float16_vector", datatype=DataType.FLOAT16_VECTOR, dim=DIM),
    # schema.add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)

    schema.verify()

    return schema
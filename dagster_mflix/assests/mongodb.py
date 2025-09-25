from dagster import AssetExecutionContext
from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets

import dlt
from ..mongodb import mongodb

mflix = mongodb(
    database='sample_mflix'
).with_resources(
    "comments",
    "embedded_movies"
)

@dlt_assets(
    dlt_source = mflix,
    dlt_pipeline = dlt.pipeline(
        pipeline_name="local_mongo",
        destination='snowflake',
        dataset_name='mflix'
    )
)
def dlt_assest_factory(context:AssetExecutionContext, dlt:DagsterDltResource):
    yield from dlt.run(context=context, write_disposition='merge')
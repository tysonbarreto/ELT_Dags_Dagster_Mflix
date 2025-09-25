from dagster import Definitions, load_assets_from_modules, EnvVar
from dagster_mflix.assests import mongodb, movies, adhoc
from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_snowflake import SnowflakeResource
from .jobs import movies_job
from .schedules import movies_schedule
from .sensors import adhoc_sensor

mongodb_assets = load_assets_from_modules([mongodb],group_name="mongodb")
movies_assets = load_assets_from_modules([movies], group_name="movies")
adhoc_assets = load_assets_from_modules([adhoc], group_name="adhoc")

snowflake_resource = SnowflakeResource(
    account=EnvVar('SNOWFLAKE_ACCOUNT'),
    user=EnvVar('SNOWFLAKE_USER'),
    password=EnvVar('SNOWFLAKE_PASSWORD'),
    warehouse=EnvVar('DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE'),
    database=EnvVar('DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE'),
    schema=EnvVar('SNOWFLAKE_SCHEMA'),
    role=EnvVar('DESTINATION__SNOWFLAKE__CREDENTIALS__ROLE')
)

defs = Definitions(
    assets=[*mongodb_assets,*movies_assets,*adhoc_assets],
    resources={
        "dlt":DagsterDltResource(),
        "snowflake":snowflake_resource
    },
    jobs=[movies_job],
    schedules=[movies_schedule],
    sensors=[adhoc_sensor]
)

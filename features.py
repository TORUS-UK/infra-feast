import datetime as dt

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    Project,
    PushSource,
)
from feast.types import Float32, Int64
from feast.value_type import ValueType

project = Project(name="jc_project", description="A project that stores watch and camera data.")

watch = Entity(
    name='basic-smart-watch',
    join_keys=['watch_id'],
    description='watch id',
    value_type=ValueType.INT64,
)

#watch_data_source = FileSource(
#    name="watch_100Hz_data",
#    path="data/watch_data.parquet",
#    timestamp_field="event_ts",
#    created_timestamp_column="created",
#)

watch_data_push_source = PushSource(
    name='watch_100Hz_push_source',
#    batch_source=watch_data_source,
    batch_source=None,  # Use offline store as configured in the yaml file.
)

watch_data_fv = FeatureView(
    name='watch_stats',
    description='simple smart watch features',
    entities=[ watch ],
    ttl=dt.timedelta(days=1),
    schema=[
        Field(name = 'acc_x', dtype=Float32),
        Field(name = 'acc_y', dtype=Float32),
        Field(name = 'acc_z', dtype=Float32),
        Field(name = 'gyro_x', dtype=Float32),
        Field(name = 'gyro_y', dtype=Float32),
        Field(name = 'gyro_z', dtype=Float32),
    ],
    online=True,
    source=watch_data_push_source,
    tags={'owner': 'jc', 'watch-type': 'dummy watch'}
)

watch_activity = FeatureService(
    name="watch_activity",
    features=[watch_data_fv],
)

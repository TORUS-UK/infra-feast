# %%
import datetime as dt
import os

import pandas as pd


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


# %%
project = Project(name="jc_project", description="A project that stores watch and camera data.")

watch = Entity(
    name='basic-smart-watch',
    join_keys=['watch_id'],
    description='watch id',
    value_type=ValueType.INT64,
)

watch_data_source = FileSource(
   name="watch_100Hz_data",
   path="data/watch_data.parquet",
   timestamp_field="event_ts",
   created_timestamp_column="created",
)

watch_data_push_source = PushSource(
    name='watch_100Hz_push_source',
    batch_source=watch_data_source,
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


def _init_data_sources():
    #watch_data_filename = watch_data_source.path
    print(f'Data path: {watch_data_source.path}')

    # NOTE: Workaround to make an empty FileSource work as a PushSource.
    # Check if we need to add a line to create an nearly empty parquet file.
    add_a_line = False
    if not os.path.exists(watch_data_source.path):
        print('Creating the watch data source.')
        df = pd.DataFrame(columns=['event_ts', 'watch_id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'created'])
        add_a_line = True
    else:
        print('Watch data source already exists.')
        df = pd.read_parquet(watch_data_source.path)
        if len(df) == 0:
            add_a_line = True

    # Add a line to the parquet file.
    if add_a_line:
        print('Adding a single non-empty line to the data source.')
        #df[['event_ts', 'created']] = df[['event_ts', 'created']].astype('timestamp[ns][pyarrow]')
        df[['event_ts', 'watch_id', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'created']] = [pd.NaT, -1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, pd.NaT]
        #df[['event_ts', 'created']] = pd.to_datetime(df[['event_ts', 'created']])
        df.to_parquet(watch_data_source.path)


_init_data_sources()

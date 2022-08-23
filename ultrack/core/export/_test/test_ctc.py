import numpy as np
import pandas as pd
import pytest

from ultrack.core.database import NO_PARENT
from ultrack.core.export.ctc import add_paths_to_forest, ctc_compress_forest


@pytest.fixture
def dataframe_forest() -> pd.DataFrame:
    """
                  2
              --------
       1    /
    -------
            \\     3
              --------

            4
    ------------------
    """

    df = np.empty((40, 2), dtype=int)

    # track # 1
    df[:10, 0] = np.arange(1, 11)
    df[:10, 1] = df[:10, 0] - 1
    df[0, 1] = NO_PARENT

    # track # 2
    df[10:20, 0] = np.arange(11, 21)
    df[10:20, 1] = df[10:20, 0] - 1
    df[10, 1] = 10

    # track # 3
    df[20:30, 0] = np.arange(21, 31)
    df[20:30, 1] = df[20:30, 0] - 1
    df[20, 1] = 10

    df[30:40, 0] = np.arange(31, 41)
    df[30:40, 1] = df[30:40, 0] - 1
    df[30, 1] = NO_PARENT

    return pd.DataFrame(df[:, 1], index=df[:, 0], columns=["parent_id"])


@pytest.fixture
def dataframe_forest_with_time(dataframe_forest: pd.DataFrame) -> pd.DataFrame:
    df = dataframe_forest.copy()
    df["t"] = -1
    df["t"].values[:10] = np.arange(10)
    df["t"].values[10:20] = np.arange(10, 20)
    df["t"].values[20:30] = np.arange(10, 20)
    df["t"].values[30:40] = np.arange(5, 15)
    return df


def test_add_paths_to_forest(dataframe_forest: pd.DataFrame) -> None:
    df = add_paths_to_forest(dataframe_forest)

    assert np.all(df["track_id"].values[0:10] == 1)
    assert np.all(df["track_id"].values[10:20] == 2)
    assert np.all(df["track_id"].values[20:30] == 3)
    assert np.all(df["track_id"].values[30:40] == 4)

    assert np.all(df["parent_track_id"].values[0:10] == NO_PARENT)
    assert np.all(df["parent_track_id"].values[10:30] == 1)
    assert np.all(df["parent_track_id"].values[30:40] == NO_PARENT)


def test_ctc_compress_forest(dataframe_forest_with_time: pd.DataFrame) -> pd.DataFrame:
    df = ctc_compress_forest(add_paths_to_forest(dataframe_forest_with_time))

    expected_df = np.array(
        [[1, 0, 9, 0], [2, 10, 19, 1], [3, 10, 19, 1], [4, 5, 14, 0]]
    )

    assert np.all(df.columns == ["L", "B", "E", "P"])
    assert np.all(df.values == expected_df)

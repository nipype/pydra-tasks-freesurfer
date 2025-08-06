from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.mri_marching_cubes import MRIMarchingCubes
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrimarchingcubes_1():
    task = MRIMarchingCubes()
    task.in_file = File.sample(seed=0)
    task.connectivity_value = 1
    task.subjects_dir = Directory.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

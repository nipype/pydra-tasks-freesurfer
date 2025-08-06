from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.smooth_tessellation import SmoothTessellation
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smoothtessellation_1():
    task = SmoothTessellation()
    task.in_file = File.sample(seed=0)
    task.subjects_dir = Directory.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

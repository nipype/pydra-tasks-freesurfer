from fileformats.generic import Directory
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.remove_intersection import RemoveIntersection
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_removeintersection_1():
    task = RemoveIntersection()
    task.in_file = Pial.sample(seed=0)
    task.subjects_dir = Directory.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_removeintersection_2():
    task = RemoveIntersection()
    task.in_file = Pial.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

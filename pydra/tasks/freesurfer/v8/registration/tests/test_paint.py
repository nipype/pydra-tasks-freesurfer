from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.registration.paint import Paint
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_paint_1():
    task = Paint()
    task.in_surf = Pial.sample(seed=0)
    task.template = File.sample(seed=1)
    task.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_paint_2():
    task = Paint()
    task.in_surf = Pial.sample(seed=0)
    task.averages = 5
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

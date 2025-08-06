from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.jacobian import Jacobian
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_jacobian_1():
    task = Jacobian()
    task.in_origsurf = Pial.sample(seed=0)
    task.in_mappedsurf = File.sample(seed=1)
    task.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_jacobian_2():
    task = Jacobian()
    task.in_origsurf = Pial.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Nofix, Orig
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.fix_topology import FixTopology
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fixtopology_1():
    task = FixTopology()
    task.in_orig = Orig.sample(seed=0)
    task.in_inflated = File.sample(seed=1)
    task.in_brain = File.sample(seed=2)
    task.in_wm = File.sample(seed=3)
    task.subject_id = "subject_id"
    task.sphere = Nofix.sample(seed=10)
    task.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fixtopology_2():
    task = FixTopology()
    task.in_orig = Orig.sample(seed=0)
    task.subject_id = "10335"
    task.ga = True
    task.sphere = Nofix.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

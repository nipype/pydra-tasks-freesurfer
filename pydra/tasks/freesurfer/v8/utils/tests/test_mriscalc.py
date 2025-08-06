from fileformats.generic import Directory, File
from fileformats.medimage_freesurfer import Area
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.mr_is_calc import MRIsCalc
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mriscalc_1():
    task = MRIsCalc()
    task.in_file1 = Area.sample(seed=0)
    task.in_file2 = File.sample(seed=3)
    task.subjects_dir = Directory.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mriscalc_2():
    task = MRIsCalc()
    task.in_file1 = Area.sample(seed=0)
    task.action = "add"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

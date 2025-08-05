from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.remove_neck import RemoveNeck
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_removeneck_1():
    task = RemoveNeck()
    task.in_file = MghGz.sample(seed=0)
    task.transform = File.sample(seed=2)
    task.template = TextMatrix.sample(seed=3)
    task.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_removeneck_2():
    task = RemoveNeck()
    task.in_file = MghGz.sample(seed=0)
    task.template = TextMatrix.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

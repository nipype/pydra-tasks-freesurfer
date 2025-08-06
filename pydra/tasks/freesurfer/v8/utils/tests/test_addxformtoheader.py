from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.add_x_form_to_header import AddXFormToHeader
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_addxformtoheader_1():
    task = AddXFormToHeader()
    task.in_file = MghGz.sample(seed=0)
    task.transform = File.sample(seed=1)
    task.out_file = "output.mgz"
    task.subjects_dir = Directory.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_addxformtoheader_2():
    task = AddXFormToHeader()
    task.in_file = MghGz.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_addxformtoheader_3():
    task = AddXFormToHeader()
    task.copy_name = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

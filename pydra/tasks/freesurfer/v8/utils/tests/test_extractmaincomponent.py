from fileformats.medimage_freesurfer import Pial
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.extract_main_component import ExtractMainComponent
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_extractmaincomponent_1():
    task = ExtractMainComponent()
    task.in_file = Pial.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_extractmaincomponent_2():
    task = ExtractMainComponent()
    task.in_file = Pial.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

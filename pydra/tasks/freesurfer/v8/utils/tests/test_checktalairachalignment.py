from fileformats.datascience import TextMatrix
from fileformats.generic import Directory
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.check_talairach_alignment import (
    CheckTalairachAlignment,
)
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_checktalairachalignment_1():
    task = CheckTalairachAlignment()
    task.in_file = TextMatrix.sample(seed=0)
    task.threshold = 0.01
    task.subjects_dir = Directory.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_checktalairachalignment_2():
    task = CheckTalairachAlignment()
    task.in_file = TextMatrix.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

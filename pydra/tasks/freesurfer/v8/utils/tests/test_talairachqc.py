from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.talairach_qc import TalairachQC
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_talairachqc_1():
    task = TalairachQC()
    task.log_file = File.sample(seed=0)
    task.subjects_dir = Directory.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_talairachqc_2():
    task = TalairachQC()
    task.log_file = "dirs.txt"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

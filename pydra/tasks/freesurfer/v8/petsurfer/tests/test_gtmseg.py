from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.petsurfer.gtm_seg import GTMSeg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_gtmseg_1():
    task = GTMSeg()
    task.out_file = "gtmseg.mgz"
    task.colortable = File.sample(seed=15)
    task.subjects_dir = Directory.sample(seed=17)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_gtmseg_2():
    task = GTMSeg()
    task.subject_id = "subject_id"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

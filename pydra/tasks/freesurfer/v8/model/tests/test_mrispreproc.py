from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.mris_preproc import MRISPreproc
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrispreproc_1():
    task = MRISPreproc()
    task.fsgd_file = File.sample(seed=6)
    task.subject_file = File.sample(seed=7)
    task.surf_measure_file = [File.sample(seed=8)]
    task.subjects_dir = Directory.sample(seed=18)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrispreproc_2():
    task = MRISPreproc()
    task.target = "fsaverage"
    task.vol_measure_file = [
        ("cont1.nii", "register.dat"),
        ("cont1a.nii", "register.dat"),
    ]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

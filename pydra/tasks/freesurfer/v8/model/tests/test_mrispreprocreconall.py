from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.mris_preproc_recon_all import MRISPreprocReconAll
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrispreprocreconall_1():
    task = MRISPreprocReconAll()
    task.surf_measure_file = File.sample(seed=0)
    task.surfreg_files = [File.sample(seed=1)]
    task.lh_surfreg_target = File.sample(seed=2)
    task.rh_surfreg_target = File.sample(seed=3)
    task.subject_id = "subject_id"
    task.fsgd_file = File.sample(seed=12)
    task.subject_file = File.sample(seed=13)
    task.subjects_dir = Directory.sample(seed=23)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_mrispreprocreconall_2():
    task = MRISPreprocReconAll()
    task.target = "fsaverage"
    task.vol_measure_file = [
        ("cont1.nii", "register.dat"),
        ("cont1a.nii", "register.dat"),
    ]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

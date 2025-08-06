from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.preprocess.unpack_sdicom_dir import UnpackSDICOMDir
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_unpacksdicomdir_1():
    task = UnpackSDICOMDir()
    task.source_dir = Directory.sample(seed=0)
    task.output_dir = Directory.sample(seed=1)
    task.config = File.sample(seed=3)
    task.seq_config = File.sample(seed=4)
    task.scan_only = File.sample(seed=7)
    task.log_file = File.sample(seed=8)
    task.subjects_dir = Directory.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_unpacksdicomdir_2():
    task = UnpackSDICOMDir()
    task.source_dir = "."
    task.run_info = (5, "mprage", "nii", "struct")
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

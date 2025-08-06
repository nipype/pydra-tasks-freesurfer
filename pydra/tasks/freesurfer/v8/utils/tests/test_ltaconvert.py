from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.lta_convert import LTAConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ltaconvert_1():
    task = LTAConvert()
    task.in_fsl = File.sample(seed=1)
    task.in_mni = File.sample(seed=2)
    task.in_reg = File.sample(seed=3)
    task.in_niftyreg = File.sample(seed=4)
    task.in_itk = File.sample(seed=5)
    task.source_file = File.sample(seed=13)
    task.target_file = File.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

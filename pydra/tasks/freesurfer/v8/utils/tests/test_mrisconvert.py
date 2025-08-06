from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.utils.mr_is_convert import MRIsConvert
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mrisconvert_1():
    task = MRIsConvert()
    task.annot_file = File.sample(seed=0)
    task.parcstats_file = File.sample(seed=1)
    task.label_file = File.sample(seed=2)
    task.scalarcurv_file = File.sample(seed=3)
    task.functional_file = File.sample(seed=4)
    task.labelstats_outfile = File.sample(seed=5)
    task.in_file = File.sample(seed=15)
    task.subjects_dir = Directory.sample(seed=20)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

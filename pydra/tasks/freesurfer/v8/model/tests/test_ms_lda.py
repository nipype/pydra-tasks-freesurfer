from fileformats.generic import Directory, File
from fileformats.medimage import MghGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.freesurfer.v8.model.ms__lda import MS_LDA
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ms_lda_1():
    task = MS_LDA()
    task.label_file = MghGz.sample(seed=3)
    task.mask_file = File.sample(seed=4)
    task.images = [MghGz.sample(seed=8)]
    task.subjects_dir = Directory.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_ms_lda_2():
    task = MS_LDA()
    task.lda_labels = [grey_label, white_label]
    task.weight_file = "weights.txt"
    task.vol_synth_file = "synth_out.mgz"
    task.label_file = MghGz.sample(seed=3)
    task.shift = zero_value
    task.conform = True
    task.use_weights = True
    task.images = [MghGz.sample(seed=8)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)

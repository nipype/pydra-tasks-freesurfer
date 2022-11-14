import os, pytest
from pathlib import Path
from ..reconall import ReconAll


@pytest.mark.skip("Not convert.py needs work to generate tests")
@pytest.mark.parametrize("inputs, outputs", [])
def test_ReconAll(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {{}}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = {self.interface_name}(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )

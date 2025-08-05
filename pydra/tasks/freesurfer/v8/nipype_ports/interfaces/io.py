import glob
import logging
from pydra.tasks.freesurfer.v8.nipype_ports.utils.filemanip import (
    ensure_list,
    simplify_list,
)
import os


logger = logging.getLogger(__name__)


class FreeSurferSource(IOBase):
    """Generates freesurfer subject info from their directories.

    Examples
    --------
    >>> from nipype.interfaces.io import FreeSurferSource
    >>> fs = FreeSurferSource()
    >>> #fs.inputs.subjects_dir = '.'
    >>> fs.inputs.subject_id = 'PWS04'
    >>> res = fs.run() # doctest: +SKIP

    >>> fs.inputs.hemi = 'lh'
    >>> res = fs.run() # doctest: +SKIP

    """

    input_spec = FSSourceInputSpec
    output_spec = FSSourceOutputSpec
    _always_run = True
    _additional_metadata = ["loc", "altkey"]

    def _get_files(self, path, key, dirval, altkey=None):

        globsuffix = ""
        if dirval == "mri":
            globsuffix = ".mgz"
        elif dirval == "stats":
            globsuffix = ".stats"
        globprefix = ""
        if dirval in ("surf", "label", "stats"):
            if self.inputs.hemi != "both":
                globprefix = self.inputs.hemi + "."
            else:
                globprefix = "?h."
            if key in ("aseg_stats", "wmparc_stats"):
                globprefix = ""
        elif key == "ribbon":
            if self.inputs.hemi != "both":
                globprefix = self.inputs.hemi + "."
            else:
                globprefix = "*"
        keys = ensure_list(altkey) if altkey else [key]
        globfmt = os.path.join(path, dirval, f"{globprefix}{{}}{globsuffix}")
        return [
            os.path.abspath(f) for key in keys for f in glob.glob(globfmt.format(key))
        ]

    def _list_outputs(self):

        subjects_dir = self.inputs.subjects_dir
        subject_path = os.path.join(subjects_dir, self.inputs.subject_id)
        output_traits = self._outputs()
        outputs = output_traits.get()
        for k in list(outputs.keys()):
            val = self._get_files(
                subject_path,
                k,
                output_traits.traits()[k].loc,
                output_traits.traits()[k].altkey,
            )
            if val:
                outputs[k] = simplify_list(val)
        return outputs

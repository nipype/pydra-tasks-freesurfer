from fileformats.generic import Directory, File
import logging
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define(xor=[["config", "run_info", "seq_config"]])
class UnpackSDICOMDir(shell.Task["UnpackSDICOMDir.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.freesurfer.v8.preprocess.unpack_sdicom_dir import UnpackSDICOMDir

    >>> task = UnpackSDICOMDir()
    >>> task.source_dir = Directory.mock(".")
    >>> task.output_dir = Directory.mock()
    >>> task.run_info = (5, "mprage", "nii", "struct")
    >>> task.config = File.mock()
    >>> task.seq_config = File.mock()
    >>> task.scan_only = File.mock()
    >>> task.log_file = File.mock()
    >>> task.subjects_dir = Directory.mock()
    >>> task.cmdline
    'unpacksdcmdir -generic -targ . -run 5 mprage nii struct -src .'


    """

    executable = "unpacksdcmdir"
    source_dir: Directory = shell.arg(
        help="directory with the DICOM files", argstr="-src {source_dir}"
    )
    output_dir: Directory = shell.arg(
        help="top directory into which the files will be unpacked",
        argstr="-targ {output_dir}",
    )
    run_info: ty.Any | None = shell.arg(
        help="runno subdir format name : spec unpacking rules on cmdline",
        argstr="-run {run_info[0]} {run_info[1]} {run_info[2]} {run_info[3]}",
    )
    config: File | None = shell.arg(
        help="specify unpacking rules in file", argstr="-cfg {config}"
    )
    seq_config: File | None = shell.arg(
        help="specify unpacking rules based on sequence", argstr="-seqcfg {seq_config}"
    )
    dir_structure: ty.Any = shell.arg(
        help="unpack to specified directory structures", argstr="-{dir_structure}"
    )
    no_info_dump: bool = shell.arg(
        help="do not create infodump file", argstr="-noinfodump"
    )
    scan_only: File = shell.arg(
        help="only scan the directory and put result in file",
        argstr="-scanonly {scan_only}",
    )
    log_file: File = shell.arg(help="explicitly set log file", argstr="-log {log_file}")
    spm_zeropad: int = shell.arg(
        help="set frame number zero padding width for SPM",
        argstr="-nspmzeropad {spm_zeropad}",
    )
    no_unpack_err: bool = shell.arg(
        help="do not try to unpack runs with errors", argstr="-no-unpackerr"
    )
    subjects_dir: Directory = shell.arg(help="subjects directory")

    class Outputs(shell.Outputs):
        pass

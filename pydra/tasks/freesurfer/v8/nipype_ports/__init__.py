import attrs
from fileformats.generic import Directory, File
import json
import logging
from pathlib import Path
from pydra.compose import python, shell, workflow
from .interfaces import FreeSurferSource
from .utils import (
    _cifs_table,
    _generate_cifs_table,
    _parse_mount_table,
    copyfile,
    ensure_list,
    fmlogger,
    fname_presuffix,
    get_related_files,
    hash_infile,
    hash_timestamp,
    is_container,
    on_cifs,
    related_filetype_sets,
    simplify_list,
    split_filename,
)
from pydra.utils.typing import MultiInputObj
import typing as ty
import yaml


logger = logging.getLogger(__name__)

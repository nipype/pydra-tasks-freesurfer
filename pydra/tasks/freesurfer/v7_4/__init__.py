"""Pydra tasks for FreeSurfer.

1. Recon-All

The main task definition for recon-all can be imported directly from the root package.

>>> from pydra.tasks.freesurfer.v7_4 import ReconAll

Additional task definitions are available under the :mod:`recon_all` namespace
for more advanced use cases.

>>> from pydra.tasks.freesurfer.v7_4.recon_all import BaseReconAll, LongReconAll

2. Volume Utilities

Task definitions for volume processing utilities are available under the :mod:`mri` namespace.

>>> from pydra.tasks.freesurfer.v7_4 import mri

3. Surface Utilities

Task definitions for surface processing utilities are available under the :mod:`mris` namespace.

>>> from pydra.tasks.freesurfer.v7_4 import mris

.. automodule:: pydra.tasks.freesurfer.v7_4.gtmseg
.. automodule:: pydra.tasks.freesurfer.v7_4.mri
.. automodule:: pydra.tasks.freesurfer.v7_4.mris
.. automodule:: pydra.tasks.freesurfer.v7_4.recon_all
.. automodule:: pydra.tasks.freesurfer.v7_4.tkregister2
"""

from .gtmseg import GTMSeg
from .recon_all import ReconAll
from .tkregister2 import TkRegister2

__all__ = ["GTMSeg", "ReconAll", "TkRegister2"]

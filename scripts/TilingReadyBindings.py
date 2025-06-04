#
# Copyright (C) 2025, ETH Zurich and University of Bologna.
#
# Author: Luka Macan luka.macan@unibo.it
#
# ----------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from typing import Dict, List, Tuple, Union
from ortools.constraint_solver.pywrapcp import IntVar
from Deeploy.TilingExtension.MemoryConstraints import NodeMemoryConstraint
from Deeploy.TilingExtension.TileConstraint import TileConstraint
from Deeploy.TilingExtension.TilerModel import TilerModel, PerformanceHint
from Deeploy.TilingExtension.TilingCodegen import AbsoluteHyperRectangle, TilingSchedule, VariableReplacementScheme
from Deeploy.TilingExtension.TilerExtension import TilingReadyNodeBindings
from Deeploy.DeeployTypes import NetworkContext, OperatorRepresentation
from Deeploy.AbstractDataTypes import PointerClass
from Deeploy.CommonExtensions.DataTypes import uint32_t, int32_t

## Import the appropriate `Bindings` as previously defined in Task 3
from Bindings import PlaceholderBindings

class PlaceholderTileConstraint(TileConstraint):

    # TASK 5.1 - class properties
    dataName = 'boh!'  #: str: Name of input tensor as defined by the operator's parser

    @classmethod
    def addGeometricalConstraint(cls, tilerModel: TilerModel, parseDict: Dict, ctxt: NetworkContext) -> TilerModel:

        # TASK 5.2-6

        return tilerModel

    @classmethod
    def serializeTilingSolution(
            cls, tilingSolution: NodeMemoryConstraint, absoluteOutputCubes: List[AbsoluteHyperRectangle],
            targetMemLevel: str, ctxt: NetworkContext,
            operatorRepresentation: OperatorRepresentation) -> Tuple[VariableReplacementScheme, TilingSchedule]:
        
        ## get a list of tile sizes
        outputTiles = [tile.rectangle for tile in absoluteOutputCubes]

        ## TASK 6.1: get the NodeParser labels as defined previously
        addrNames = []

        ## TASK 6.2: extract base addresses
        inputBaseOffsets, outputBaseOffsets = None, None
        ## inputBaseOffsets, outputBaseOffsets = cls.extractBaseAddr(tilingSolution, targetMemLevel,
                                                                #   operatorRepresentation, addrNames)

        ## TASK 6.3: set replacements

        ## TASK 6.4: set replacementTypes

        ## TASK 6.5: set I/O load schedules

        ## TASK 6.6: tiling schedule

        ## TASK 6.7: variable replacement schedule
        tilingSchedule = None
        variableReplacementSchedule = None

        return variableReplacementSchedule, tilingSchedule

# TASK 6.8
placeholderTilingReadyBindings = None
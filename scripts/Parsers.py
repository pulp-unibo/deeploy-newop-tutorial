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

from typing import Tuple
import onnx_graphsurgeon as gs
from Deeploy.DeeployTypes import NetworkContext
import numpy as np

## NodeParsers are classes responsible for interpreting and extracting relevant information
## from computational graph nodes (represented as ONNX or other model nodes). They analyze
## node attributes, inputs, and outputs, and populate an internal representation
## (`operatorRepresentation`) with the necessary parameters and metadata. This information
## is then used for further processing, such as code generation or optimization. In summary,
## NodeParsers translate graph node definitions into a structured form that Deeploy can use.
##
## You can use the NodeParser for your particular operator as a starting point.
## For example, look in `Deeploy/Targets/Generic/Parsers.py` or `Deeploy/Targets/PULPOpen/Parsers.py`
## A NodeParser will expose __init__ plus two methods:
##  - `parseNode(self, node: gs.Node) -> bool`: this must check that the number of node inputs
##    and outputs are correct (and if so, return True)
##  - `parseNodeCtxt(self, ctxt: NetworkContext, node: gs.Node, channels_first: bool=True)
##       -> Tuple[NetworkContext, book]`: this associates names of the inputs/outputs in the
##       ONNX context with names in an internal operatorRepresentation.
##

## TASK 2.1
class PlaceholderParser(NodeParser):

    def __init__(self):
        super().__init__()

    def parseNode(self, node: gs.Node) -> bool:

        PLACEHOLDER_NB_INPUTS  = 2
        PLACEHOLDER_NB_OUTPUTS = 1

        # TASK 2.2: return True when the number of I/Os is correct
        return False

    def parseNodeCtxt(self,
                      ctxt: NetworkContext,
                      node: gs.Node,
                      channels_first: bool = True) -> Tuple[NetworkContext, bool]:
        
        # TASK 2.3-5: fill this with actual content

        return ctxt, True

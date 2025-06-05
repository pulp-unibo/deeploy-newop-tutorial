#
# Copyright (C) 2025, ETH Zurich and University of Bologna.
#
# Author: Luka Macan luka.macan@unibo.it
#         Francesco Conti f.conti@unibo.it
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

from Deeploy.AbstractDataTypes import PointerClass
from Deeploy.CommonExtensions.DataTypes import int8_t, uint8_t, float32_t
from Deeploy.DeeployTypes import NodeBinding
from Deeploy.Targets.PULPOpen.Bindings import ForkTransformer

## TASK 4.1
from Templates import SOMETHING

## `TypeCheckers` are classes used to verify that the input and output data types
## of computational nodes (such as layers or operations) match the expected types
## for a given template or binding. They ensure that the correct data types are used
## when generating code for different operations, helping to prevent type mismatches
## and errors during code generation or execution.
## 
## Import the appropriate `TypeChecker` from the Generic or PULPOpen sets.
## You can find them in `Deeploy/Targets/TARGET/TypeCheckers.py`
## Import with the following syntax:
##
##   from Deeploy.Targets.TARGET.TypeCheckers import OperatorChecker

# TASK 4.1
from Deeploy.Targets.PLACEHOLDER.TypeCheckers import PLACEHOLDER

## NodeBindings are objects that associate a specific operation (such as a neural
## network layer or function) with its type checker, code generation template, and
## code transformation logic. They define how a particular node (operation) should
## be recognized, validated for correct input/output types, and how code should be
## generated for it on a target platform. In summary, NodeBindings link the
## operation's type checking, template, and transformation steps together for code
## generation.
##
## To define your new operator implementation, add a binding with the following
## structure:
##
##   operatorBindings = [
##       NodeBinding(
##           OperatorChecker(
##               [
##                   PointerClass(input_0_type),
##                   PointerClass(input_1_type),
##                   ...
##               ],
##               [
##                   PointerClass(output_type)
##               ]
##           ),
##           template,
##           Transformer
##           ))
##   ]
##
## where OperatorChecker is the checker imported above, whose __init__ accepts three arguments:
##  1) list of types of inputs to the node (e.g., `PointerClass(uint8_t)`)
##  2) list of types of outputs of the node
##  3) a `Transformer` set of passes as defined, for example, in `Deeploy/Targets/PULPOpen/Bindings`

# TASK 4.2-5
operatorBindings = [
    NodeBinding(PLACEHOLDER)
]

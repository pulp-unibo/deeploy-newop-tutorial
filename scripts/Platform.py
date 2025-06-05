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

from Deeploy.DeeployTypes import NodeMapper
from Deeploy.MemoryLevelExtension.NetworkDeployers.MemoryLevelDeployer import MemoryDeployerWrapper
from Deeploy.MemoryLevelExtension.MemoryLevels import MemoryHierarchy, MemoryLevel
from Deeploy.Targets.Generic.Layers import SoftmaxLayer, AddLayer
from Deeploy.Targets.Neureka.Platform import MemoryNeurekaPlatform

## TASK 7.1, 7.2
from Parsers import SOMETHING
from TilingReadyBindings import SOMETHING

# TASK 9
L3 = MemoryLevel(name = "L3", neighbourNames = ["L2"], size = 4000000)
L2 = MemoryLevel(name = "L2", neighbourNames = ["L3", "L1"], size = 512000)
#L1 = MemoryLevel(name = "L1", neighbourNames = ["L2"], size = 128000)
L1 = MemoryLevel(name = "L1", neighbourNames = ["L2"], size = 16000)
#WMEM = MemoryLevel(name = "WeightMemory_SRAM", neighbourNames = [], size = 4 * 1024 * 1024)

#memoryHierarchy = MemoryHierarchy([L3, L2, L1, WMEM])
memoryHierarchy = MemoryHierarchy([L3, L2, L1])
memoryHierarchy.setDefaultMemoryLevel("L3")

platform = MemoryNeurekaPlatform(
    memoryHierarchy,
    defaultTargetMemoryLevel=L1,
    #weightMemoryLevel=WMEM,
)

platform.engines[1].includeList.remove("DeeployBasicMath.h")

# TASK 7.3, 7.4

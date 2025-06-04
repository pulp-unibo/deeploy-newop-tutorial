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

import onnx_graphsurgeon as gs
from typing import List, Union
from Platform import platform, memoryHierarchy
from Deeploy.DeeployTypes import NetworkContext, NetworkDeployer, SubGraph, TransientBuffer
from Deeploy.Targets.Neureka.Deployer import NeurekaDeployer
from Deeploy.Targets.Neureka.Platform import NeurekaOptimizer
from Deeploy.EngineExtension.NetworkDeployers.EngineColoringDeployer import EngineColoringDeployerWrapper
from Deeploy.MemoryLevelExtension.NetworkDeployers.MemoryLevelDeployer import MemoryDeployerWrapper
from Deeploy.MemoryLevelExtension.OptimizationPasses.MemoryLevelAnnotationPasses import AnnotateIOMemoryLevel, AnnotateDefaultMemoryLevel, AnnotateNeurekaWeightMemoryLevel
from Deeploy.TilingExtension.TilerExtension import Tiler, TilerDeployerWrapper
from Deeploy.TilingExtension.TilerModel import TilerModel
from ortools.constraint_solver.pywrapcp import IntVar
from NetworkInfo import NetworkInfo


def setup_deployer(networkInfo: NetworkInfo) -> NetworkDeployer:
    def scheduler(graph: gs.Graph):
        return [[node] for node in graph.nodes]

    loweringOptimizer = NeurekaOptimizer

    deployer = NeurekaDeployer(
        networkInfo.graph(),
        platform,
        networkInfo.inputTypes,
        loweringOptimizer,
        scheduler,
        "DeeployNetwork",
        default_channels_first=False,
        deeployStateDir="deeployState",
    )

    # Make the deployer engine-color-aware
    deployer = EngineColoringDeployerWrapper(deployer)

    memoryLevelAnnotationPasses = [
        AnnotateIOMemoryLevel("L3"),
        AnnotateDefaultMemoryLevel(memoryHierarchy),
    ]

    if platform.weightMemoryLevel is not None:
        memoryLevelAnnotationPasses.append(
            AnnotateNeurekaWeightMemoryLevel(neurekaEngineName=platform.engines[0].name,
                                             weightMemoryLevel=platform.weightMemoryLevel)
        )

    deployer = MemoryDeployerWrapper(deployer, memoryLevelAnnotationPasses)

    class MyTiler(Tiler):

        def multiBufferStrategy(self, tilerModel: TilerModel, ctxt: NetworkContext, pattern: SubGraph, path: List[str],
                                hop: str, tensorName: str) -> Union[int, IntVar]:
            buffer = ctxt.lookup(tensorName)

            if hop == "L1" or isinstance(buffer, TransientBuffer):
                return 1
            else:
                return 2

    deployer = TilerDeployerWrapper(deployer, MyTiler)

    # Tiler defaults
    deployer.tiler.visualizeMemoryAlloc = False
    deployer.tiler.memoryAllocStrategy = "TetrisRandom"
    deployer.tiler.searchStrategy = "random-max"

    _ = deployer.generateFunction()

    return deployer

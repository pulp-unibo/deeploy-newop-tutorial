/* =====================================================================
 * Title:        CycleCounter.c
 * Description:
 *
 * $Date:        26.07.2024
 *
 * ===================================================================== */
/*
 * Copyright (C) 2020 ETH Zurich and University of Bologna.
 *
 * Author: Moritz Scherer, ETH Zurich
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "CycleCounter.h"
#include "pmsis.h"

void ResetTimer() {
  pi_perf_conf(PI_PERF_CYCLES);
  pi_perf_cl_reset();
}

void StartTimer() { pi_perf_cl_start(); }

void StopTimer() { pi_perf_cl_stop(); }

unsigned int getCycles() { return pi_perf_cl_read(PI_PERF_CYCLES); }

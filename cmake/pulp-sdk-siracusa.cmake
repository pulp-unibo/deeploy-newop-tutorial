if (NOT DEFINED ENV{PULP_SDK_HOME})
  message(FATAL_ERROR "Environment variable PULP_SDK_HOME not defined.")
endif()

set(PULP_SDK_HOME $ENV{PULP_SDK_HOME})

set(PULP_SDK_BASE_C_SOURCE
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/ram/ram.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/ram/alloc_extern.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/ram/hyperram/hyperram.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/fs/read_fs/read_fs.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/fs/host_fs/semihost.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/fs/host_fs/host_fs.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/fs/fs.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/flash/hyperflash/hyperflash.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/flash/flash.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/partition/partition.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/partition/flash_partition.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/crc/md5.c
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/bsp/siracusa.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/init.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/kernel.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/device.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/task.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/alloc.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/alloc_pool.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/irq.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/soc_event.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/log.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/time.c
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/drivers/hyperbus/hyperbus-v3.c
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/drivers/uart/uart-v1.c
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/drivers/udma/udma-v3.c
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/drivers/cluster/cluster.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/lib/libc/minimal/io.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/lib/libc/minimal/fprintf.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/lib/libc/minimal/prf.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/lib/libc/minimal/sprintf.c
  ${PULP_SDK_HOME}/rtos/pulpos/common/lib/libc/minimal/semihost.c
)

set(PULP_SDK_BASE_ASM_SOURCE
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/crt0.S
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/irq_asm.S
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/task_asm.S
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/time_asm.S
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel/soc_event_v2_itc.S
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/drivers/cluster/pe-eu-v3.S
)

set(PULP_SDK_BASE_INCLUDE
  ${PULP_SDK_HOME}/rtos/pulpos/common/lib/libc/minimal/include
  ${PULP_SDK_HOME}/rtos/pulpos/common/include
  ${PULP_SDK_HOME}/rtos/pulpos/common/kernel
  ${PULP_SDK_HOME}/rtos/pulpos/pulp_archi/include
  ${PULP_SDK_HOME}/rtos/pulpos/pulp_hal/include
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_api/include
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/include
  ${PULP_SDK_HOME}/rtos/pmsis/pmsis_bsp/include
)

set(PULP_SDK_BASE_COMPILE_FLAGS
  -D__riscv__
  -D__CONFIG_UDMA__
  -D__PULPOS2__
  -D__PLATFORM__=ARCHI_PLATFORM_GVSOC
  -DARCHI_CLUSTER_NB_PE=8
  -DPOS_CONFIG_IO_UART=0
  -DPOS_CONFIG_IO_UART_BAUDRATE=115200
  -DPOS_CONFIG_IO_UART_ITF=0
  -D__TRACE_LEVEL__=3
  -DPI_LOG_LOCAL_LEVEL=2
)

set_source_files_properties(${PULP_SDK_BASE_ASM_SOURCE} PROPERTIES COMPILE_FLAGS -DLANGUAGE_ASSEMBLY)

set(SIRACUSA_COMPILE_FLAGS
  -include ${PULP_SDK_HOME}/rtos/pulpos/pulp/include/pos/chips/siracusa/config.h
  -DCONFIG_SIRACUSA
  -DCONFIG_BOARD_VERSION_SIRACUSA
  -DCONFIG_PROFILE_SIRACUSA
  -DSKIP_PLL_INIT
  -DUSE_HYPERFLASH
  -DUSE_HYPERRAM
  -DPULP_CHIP_STR=siracusa
)

set(SIRACUSA_INCLUDES
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/include/pos/chips/siracusa
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/drivers/siracusa_padmux/include
)

set(PULP_SDK_SIRACUSA_C_SOURCE
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/kernel/chips/siracusa/pll.c
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/kernel/chips/siracusa/soc.c
  ${PULP_SDK_HOME}/rtos/pulpos/pulp/drivers/siracusa_padmux/src/siracusa_padctrl.c
)

set_source_files_properties(${PULP_SDK_SIRACUSA_ASM_SOURCE} PROPERTIES COMPILE_FLAGS -DLANGUAGE_ASSEMBLY)

add_library(pulp-sdk OBJECT ${PULP_SDK_BASE_C_SOURCE} ${PULP_SDK_BASE_ASM_SOURCE} ${PULP_SDK_SIRACUSA_C_SOURCE} ${PULP_SDK_SIRACUSA_ASM_SOURCE})

set(PULP_SDK_COMPILE_FLAGS ${SIRACUSA_COMPILE_FLAGS} ${PULP_SDK_BASE_COMPILE_FLAGS})
set(PULP_SDK_INCLUDES ${SIRACUSA_INCLUDES} ${PULP_SDK_BASE_INCLUDE})

target_include_directories(pulp-sdk SYSTEM PUBLIC ${PULP_SDK_INCLUDES})
target_compile_options(pulp-sdk PUBLIC ${PULP_SDK_COMPILE_FLAGS})
target_compile_options(pulp-sdk PRIVATE
  -Wno-sign-conversion
  -Wno-unused-function
  -Wno-unused-parameter
  -Wno-conversion
  -Wno-sign-conversion
  -Wno-unused-variable
  -Wno-sign-compare
  -Wno-return-type
  -fno-inline-functions
)

target_compile_options(pulp-sdk INTERFACE
  -Wno-unused-function
)

target_link_options(pulp-sdk PUBLIC
  -Wl,--gc-sections
  -L${PULP_SDK_HOME}/rtos/pulpos/pulp/kernel
  -Tchips/siracusa/link.ld
)

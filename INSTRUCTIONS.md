# Tutorial: adding a new operator to Deeploy

## Introduction
This is a tutorial on how to add a new operator to Deeploy.
This setup works like an out-of-root development environment for Deeploy: you can think of most of these files as directly expanding the structure of Deeploy, like you would do when designing a new `Platform` or `Engine`. Being self-contained, it is a bit less intimidating than directly modifying Deeploy's codebase!

In this assignment, we'll add a new shiny kernel to Deeploy: a kernel to perform vector addition.
This will be written in C inside the `kernel` folder, which currently contains a complete example (`iSoftmax.c`/`iSoftmax.h`) and the stub for vector addition.
To extend Deeploy with this new kernel, we have to modify a few files in the `scripts` folder, which mimick what you would find inside one of the `Targets` folder:
```
scripts
├── Bindings.py            # defines binding between node-level type-checkers and kernels
|                            for Deeploy's frontend
├── Parsers.py             # defines how the information taken from a certain ONNX node
|                            should be used within Deeploy's internal _context_
├── Platform.py            # defines the memory hierarchy of the target platform
├── Templates.py           # defines how the internal transient buffers are treated in
|                            the midend and how the context information is used to generate
|                            output code in the backend
└── TilingReadyBindings.py # contains the definition of the tiling constraints, both
                             geometric and heuristic policies
```
The `scripts` folder also contains other files/utiles that are used to drive the simulation; some are user-modifiable within this assignment, as will be discussed in the following tasks.
We will proceed from the bottom up, starting from the kernel and ``making our way'' towards the ONNX representation.

## Task 1 - Write a kernel
As Deeploy works bottom up, the first task is to write an appropriate kernel for vector add, i.e., the operation:
```
for all i:
  c[i] = a[i] + b[i]
```
The stub for this operation is defined in `kernels/PULP_vectorAdd.c`. You can exploit your (now deep!) knowledge of PULP programming to define the kernel.
You can use (if appropriate) advanced features such as cluster-level parallelism, but do not care about data transfers or double buffering: these features will be inserted automatically by Deeploy.
We will support two versions of the kernel:
 - `PULP_vectorAdd_u8_u8_u8` with unsigned inputs/outputs
 - `PULP_vectorAdd_s8_s8_s8` with signed inputs/outputs
  
## Task 2 - Define a node parser
Let us now look into `Parsers.py` to define the node parser. The parser extracts relevant information from an ONNX node, which will then be used in Deeploy's flow.
The parser is a class extending `NodeParser`, with two methods `parseNode` and `parseNodeCtxt` that are used to check whether the node is compliant with expectations on number of I/Os and to actually extract information, respectively.

1. Adapt the name of the `PlaceholderParser`.
2. In `parseNode`, check that the number of inputs and outputs is correct and return `True` in that case.
3. In `parseNodeCtxt`, you associate ONNX input/output names with an internal `operatorRepresentation`. Start this by extracting the I/Os out of the `NetworkContext`:
```
data_ = ctxt.lookup(node.<IO>.name)
```
where `<IO>` is one of the inputs/outputs: `inputs[0], inputs[1]..., outputs[0]...`. You need to do this for all I/Os (adapting `data_`).
4. Add the extracted name to the `operatorRepresentation` for each I/O:
```
self.operatorRepresentation['DATA_LABEL'] = data_.name
```
The labels you define here are used also in other files, so keep track! 
5. Add also two other labels, one for the total vector size, the other for the last dimension:
```
self.operatorRepresentation['size'] = np.prod(data_.shape)
self.operatorRepresentation['lastDim'] = data_.shape[-1]
```

## Task 3 - Write a template
To make Deeploy able to call your custom kernel, you will need to define its related class inheriting `NodeTemplate`. You can find a stub for this operation in `Templates.py`.
You can leave `computeTransientBuffersSize` and `hoistTransientBuffers` unchanged -- these are used to make Deeploy aware of any transient (temporary) buffer that is defined and consumed within the kernel, e.g., im2col.
Most likely, your implementation of vector add written in Task 1 does not include a transient buffer; if it does, please go back and revise it!
The `alignToContext` method updates the `NetworkContext` and the operator representation (i.e., its C code template) depending on the specific type. You can use labels to represent internal data or the names of placeholders for the template.

1. Rename appropriately the `PlaceholderTemplate`, e.g., `PULPVectorAddTemplate` or similar.
2. `alignToContext` needs to lookup the internal information in the `NetworkContext` to infer the specific data types used (signed or unsigned version of the kernel). You can lookup this information with
```
signed_data = ctxt.lookup(operatorRepresentation['DATA_LABEL'])._type.referencedType.typeMin < 0
```
where `DATA_LABEL` is the label of the specific input or output of the vector add node as defined in `Parsers.py`.
3. After extracting sign information for each input output, we define new place placeholders in the `operatorRepresentation` for I/O signedness, e.g.:
```
operatorRepresentation['DATA_LABEL_S'] = signed_data
```
4. At the end of the file, we must implement the actual template for calling the vector add operator in C. This is done by instantiating a `PULPVectorAddTemplate` object with the template string as argument:
```
pulpVectorAddTemplate = PULPVectorAddTemplate("""
FUNCTION_SIGNATURE_${DATA_LABEL_S}... (${DATA_LABEL}, ...);
""")
```
Align the template to the signature of the function(s) you defined in the `kernels` folder. Use the same placeholders as in the previous steps as arguments; you will likely need other labels (hint: that's why we defined a `size` argument to the `Add` operator!). You can define this label freely, but need to keep track of it in the other changes we will make.

If you need inspiration, look for examples inside Deeploy: `Deeploy/Targets/Generic/Templates` is a good starting point.

## Task 4 - Define bindings
We will now bind the ONNX `Add` node to the Template we just defined, and link this to a set of transformations that will be performed in the Deeploy backend (code generation).
This is done in `Bindings.py`.
This is done by defining a `List` of `NodeBinding` objects; each in turn calls the `TypeChecker` for a specific ONNX node and a set of passes.

1. Look up in `Deeploy/Targets/<PLATFORM>/TypeCheckers.py` for a suitable `TypeChecker` for the `Add` node, then import it into `Bindings.py`.
2. Start defining a `NodeBinding` for the unsigned version of the operator. The `NodeBinding` is built with three arguments:
   1. an operator `TypeChecker`
   2. the template you defined in Task 3
   3. the set of passes
Define from the `TypeChecker` you just imported the appropriate node interface for an `Add` with unsigned I/O.
3. Use the template you instantiated in `Templates.py` as second argument.
4. Look up in `Deeploy/Targets/PULPOpen/Bindings.py` for a set of passes that is suitable. Most PULP operators use the same set, why not do the same?
5. Add a second `NodeBinding` for the signed version of the operator.

## Task 5 - Define tile constraints
We can now define a set of tile constraints. In most cases, you can use or adapt one of the ones available in `Deeploy/Targets/<PLATFORM>/TileConstraints`, but in this instance we'll define it from scratch for instruction purposes. You're very lucky!
This is done in `TilingReadyBindings.py`.

1. Let us start by defining the names of the data inputs and outputs as class properties. Keep these aligned with the one in the parser!
```
dataName = 'DATA_LABEL'
...
```
2. Let us start by geometrical constraints, which are managed in `addGeometricalConstraint`. As a first step, let us extract the names of the I/O buffers of the `Add` node as extracted by Deeploy's ONNX parser. These are stored in the `parseDict` with the keys defined in the parser (which you can retrieve with `cls.dataName`)
```
bufferName = parseDict[cls.dataName]
...
```
3. Still inside `addGeometricalConstraint`, add each of the kernel's I/O buffers to the `tilerModel`:
```
tilerModel.addTensorDimToModel(ctxt, bufferName)
```
This call adds a symbolic tensor with this name to the tiler model. This is necessary because at this point these sizes are not yet known, but we need to be able to get their properties "as if" they were already fixed.
4. Now, we'll add a very simple constraint - that whatever is the shape of the first input, the second input and the output have exactly the same shape. This is the only constraint we need for an `Add` node. Let us start by extracting the input shape:
```
inputShape = ctxt.lookup(bufferName).shape
```
This returns the symbolic shape of the tiled tensor defined in the previous step.
5. Get pointers to the specific variables needed by extracting them from the tiler model:
```
for dim in range(len(inputShape)):
  dim1Var = tilerModel.getTensorDimVar(tensorName=bufferName, dimIdx=dim)
  dim2Var = tilerModel.getTensorDimVar(tensorName=buffer2Name, dimIdx=dim)
  ...
```
6. Then impose the actual constraints that the dimensions are identical:
```
tilerModel.addConstraint(dim1Var == SOMETHING)
...
```
Constraints work like asserts, so the condition in the `addConstraint` function must be verified.
7. Work on this class has not finished yet! See the following Task 6.

## Task 6 - Define strategy to generate tiling code 
We'll continue working on `TilingReadyBindings.py`. Specifically, we'll now focus on the `serializeTilingSolution`, which is used to compute the post-tiling arguments to be used in the operator call in C. Contrary to `addGeometricalConstraint`, this method will be called by Deeploy *after* the tiling solution has already been found.

1. Extract the `NodeParser` labels (see Task 5.1) into the `addrNames` list:
```
addrNames = [ dataName, ... ]
```
2. For the `Add` operator we need to let the tiler know how to call the kernel function with the correct in/out pointers and the correct `size` argument. The extraction of the base address is performed by the `extractBaseAddr` method:
```
inputBaseOffsets, outputBaseOffsets = cls.extractBaseAddr(tilingSolution, targetMemLevels, addrNames)
```
3. Set up a dictionary with replacements. The argument we must replace is `size` (see the kernel prototype as defined way back in Task 1!). We can compute the new `size` as the product of the cube dimensions. For this purpose, `cube.dims` is available as a Numpy array:
```
replacements = { 'size': [] }
for tile in outputTiles:
  new_size = np.prod(tile.dims)
  replacement['size'].append(new_size)
```
4. Define the replacement types. In our case, `size` is of type `int` in our kernel. In Deeploy, all kernels are called through a closure with arguments passed *by reference*, therefore we have to replace `size` with a pointer to `int`:
```
replacementTypes = { "size": PointerClass(int32_t) }
```
5. Set up I/O load schedules. For each kind of output tile (body, border, etc.), set up the related schedules:
```
inputSchedule = []
for tile in outputTiles:
  inputSchedule.append({
    cls.dataName: tile, 
    ... # all inputs
  })
outputSchedule = [] # similar to input
```
For an `Add` kernel, the tile size is the same as for each input.
6. Create an object for the complete tiling schedule:
```
tilingSchedule = TilingSchedule(
  inputBaseOffsets,
  outputBaseOffsets,
  inputLoadSchedule,
  outputLoadSchedule
)
```
7. Create an object for the complete variable replacement schedule:
```
variableReplacementSchedule = VariableReplacementScheme(
  replacements,
  replacementTypes
)
```
8. Instantiate tiling-ready bindings. Outside of the `PlaceholderTileConstraint` class definition, instantiate an object of type `TilingReadyNodeBindings` which joins the bindings defined in `Bindings.py` with the `PlaceholderTileConstraint` you just defined:
```
placeholderTilingReadyBindings = TilingReadyNodeBindings(
  nodeBindings=nodeBindingDefinedInTask4,
  tileConstraint=PlaceholderTileConstraint()
)
```

## Task 7 - Link the parser and bindings into Deeploy
In `Platform.py`, we remap the default implementation for `Add` towards our own implementation:
1. Instantiate a `NodeMapper` object using the parser and tiling-ready bindings that have been defined:
```
    placeholderAddMapper = NodeMapper(
        PlaceholderParser(),
        placeholderTilingReadyBindings
    )
```
2. Remap the `Add` node to the new mapper:
```
platform.engines[1].Mapping['Add'] = AddLayer([placeholderAddMapper])
```

## Task 8 - Test and debug!
You can now test (and debug) your newly created node.
In terminal, type:
```
make codegen testgen test
```
FIXME: how to debug?

## Task 9 - challenge your design


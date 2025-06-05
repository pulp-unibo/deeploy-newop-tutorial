## Structure

- `cmake`: extra cmake files
- `gen`: all the generated files will go here - C and hex files
- `kernel`: custom C kernel implementations
- `networks`: onnx networks and test input/output files for code generation
- `scripts`: python scripts for code and test generation
- `test`: C files necessary to build a full test app
- `third_party`: third party libraries
- `util`: utility C files

## Deeploy

[Documentation](https://pulp-platform.github.io/Deeploy/branch/devel/)

Templating language used by Deeploy: [Mako](https://www.makotemplates.org/)

### Getting Deeploy

```
git clone https://github.com/pulp-platform/Deeploy.git --branch devel
pip install --editable Deeploy
```

If you decide that you'd like to contribute your changes back to upstream, just create a fork of Deeploy, push your changes there, and create a PR :)

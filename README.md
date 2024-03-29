# Configuration Management
This repo provides and example how you can combine user-configurable settings
into a simple environment-specific YAML file and use these to patch the base
configuration of multiple components. The "patching" process is implemented in
a simple Python script, using path-based access to data structures.

The example uses YAML Kubernetes manifests in components and generates patched 
Kubernetes manifests, but you can also use other data file formats supported by
Python. If you want, you can implement the data-file based patching process in
other languages.

## Environment configuration
The environment configuration defines the specific settings for one-or-more
stacks. It can look like this:
```yaml
stacks:
    my-stack-1:
      component-1:
        # component-1 settings here
    my-stack-2:
      component-2:
        # component-2 settings here
```

## Patching process
The Python code uses the [datapath](https://github.com/idsvandermolen/datapath)
module, which can be used to access the data in the structure via path-based keys.
The advantage is syntactic sugar. Instead of:
```python
data["spec"]["template"]["spec"]["replicas"] = config["stacks"]["my-stack-1"]["component-1"]["replicas"]
```
you can write this:
```python
data["spec.template.spec.replicas"] = config["stacks.my-stack-1.component-1.replicas"]
```
Which can also be very useful with some format strings, for example in:
```python
for stack_name in config["stacks"]:
    for component in config[f"stacks.{stack_name}"]:
        data = load_some_data_file()
        data["spec.template.spec.replicas"] = config[f"stacks.{stack_name}.{component}.replicas"]
        write_some_data_file(data, stack, component)
```

## Bootstrap
Run these commands to setup the python environment:
```bash
make bootstrap
```
## TODO
There are a couple of possible improvements:
* [x] move `DataPath`, `parse_path`, `find` from `generate.py` into a library
* [ ] implement dependency management in `Makefile` to only rebuild what is needed
* [x] make input/src (`components`) and output/dst (`manifests`) explicit
* [x] add examples for other data files
* [ ] add examples for using some global settings (all-env globals, per-env globals)
* [x] use `ruamel.yaml` instead of `PyYaml` to preserve comments and anchor names.
* [ ] describe using `jsonschema` module for JSON Schema / OpenAPI validation
* [ ] describe how to deal with (SOPS) secrets in YAML files

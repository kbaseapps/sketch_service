# KBase Sketch Service

A genome "sketch" is a set of preprocessed data that makes it fast to compare genomes and get a similarity score. This is useful for doing genome searches, where you can find a list of similar genomes from a query genome.

This is a KBase dynamic (persistent) service that takes [Workspace IDs]() pointing to assemblies or genomes and returns a list of similar assemblies/genomes.

## Development

### Running the server

Run the server locally with:

```sh
$ docker build . -t kbase_sketch_service
$ docker run -p 5000:5000 -v $(pwd):/kb/module -it kbase_sketch_service
```

### Testing

### Project anatomy

Important files:

* `kbase.yml` and `compile_report.json` are the main configuration files for KBase
* `entrypoint.sh` is the docker container's entrypoint script. The option with no arguments runs the python server.
* `Dockerfile` defines our container and `requirements.txt` defines our pip dependencies.
* The actual server code lives in `src/kbase/sketch`

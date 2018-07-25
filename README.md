# KBase Homology Service

This is a KBase dynamic (persistent) service that takes [Workspace IDs]() pointing to assemblies or genomes and returns a list of similar genomes.

## Development

### Running the server

Run the server with:

```sh
$ docker build . -t kbase_homology_service
$ docker run -p 5000:5000 -v /home/j/kbase/homology_service:/kb/module -it kbase_homology_service
```

TODO will need to make this compatible with kbase.

### Testing

### Project anatomy

Important files:

* `kbase.yml` and `compile_report.json` are the main configuration files for KBase
* `entrypoint.sh` is the docker container's entrypoint script. The option with no arguments runs the python server.
* `Dockerfile` defines our container and `requirements.txt` defines our pip dependencies.
* The actual server code lives in `src/kbase/homology`

# KBase Sketch Service

A genome "sketch" is a set of preprocessed data that makes it fast to compare genomes and get a similarity score. This is useful for doing genome searches, where you can find a list of similar genomes from a query genome.

This is a KBase dynamic (persistent) service that takes workspace IDs pointing to Assemblies, Genomes, or Reads and returns a list of similar genomes.

## Development

### Set up the environment

You can use the following env vars:

- `KBASE_ENDPOINT` - required - eg "https://ci.kbase.us/services/"
- `KBASE_SECURE_CONFIG_PARAM_service_token` - required - a KBase auth token that represents this service, used for making requests to the caching service
- `KBASE_SECURE_CONFIG_PARAM_CACHING_SERVICE_URL` - optional
- `KBASE_SECURE_CONFIG_PARAM_HOMOLOGY_URL` - optional - defaults to `https://homology.kbase.us`
- `KBASE_SECURE_CONFIG_PARAM_ID_MAPPER_URL` - optional - defaults to use `KBASE_ENDPOINT` with `/idmapper/api/v1`
- `KBASE_SECURE_CONFIG_PARAM_HOMOLOGY_NAMESPACE ` - optional - defaults to `NCBI_Refseq`

### Running and testing

Build and run locally with:

```sh
$ docker-compose up --build
```

Run tests with `python -m unittest discover src/test`

### Project anatomy

Important files:

* `kbase.yml` and `compile_report.json` are the main configuration required by KBase
* `entrypoint.sh` is the docker container's entrypoint script. The option with no arguments runs the python server.
* `Dockerfile` defines our container and `requirements.txt` defines our pip dependencies.
* The actual server code lives in `src/server.py`

## Using the Sketch Service

### Running Basic request

From the terminal you can use a `CURL` command to use the sketch service. Since the sketch serivce is dynamic, you will have to find its active URL by searching for it here: "https://ci.kbase.us/#catalog/services".

The service accepts a JSON payload with the following parameters:
```
{
	'params':list(workspace_references),
	'n_max_results': 1 < int < 100,
}
```

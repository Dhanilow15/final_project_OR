# otm-gemeo-laminadores

## Getting Started

This section will guide you through the initial setup and configuration of the repository. It covers the steps to install and update dependencies, run the code, perform testing, and introduces some useful functions.

### Requirements
Make sure you have the following software installed:

- Python 3.11+
- Pip 3.11+
- Poetry
- Docker

### Setting Up the Repository

1. (Optional) Configure the poetry environment to create the .venv file locally (must be done just the first time)
     ```sh
    $ poetry config virtualenvs.in-project true
    ```

2. Create a new Python virtual environment using Poetry:
    ```sh
    $ poetry shell
    ```

3. Poetry manages the project dependencies at [pyproject.toml](pyproject.toml). 
Install the project requirements in the newly created environment with:
    ```sh
    $ poetry install
    ```

### Configuring Docker

If you don't have Docker and Docker Compose installed, we recommend using the official Docker website for [Docker](https://docs.docker.com/engine/install/ubuntu/#set-up-the-repository) and [Docker Compose](https://docs.docker.com/compose/install/linux/).

To configure the Docker image for the project, you need to create a `.env` file and a `docker-compose.yml` file. You can use the provided example files as a starting point:

1. Copy the example `.env` file:
    ```sh
    $ cp .env.example .env
    ```

2. Copy the example `docker-compose.yml` file:
    ```sh
    $ cp docker-compose.yml.example docker-compose.yml
    ```

### Building the Docker Image

Use one of the following commands to build the Docker image:

- Using `docker-compose`:
    ```sh
    $ docker compose build
    ```

- Using `make`:
    ```sh
    $ make build
    ```

Once the Docker image is built, you can run and test the code.

***

## Running the Code and Checking the Response

After building the Docker image, you can run the code and check the response using the following steps:

1. Run the Docker container:

- Using `docker-compose`:
    ```sh
    $ docker compose run science
    ```

- Using `make`:
    ```sh
    $ make run
    ```

2. In a separate terminal, activate the virtual environment using `poetry shell`.

3. Use the script [queue_despatcher.py](scripts/queue_despatcher/queue_despatcher.py) to dispatch the [input_model.json](science_rolling_ob_twin/data/input_model.json) for processing by the Docker container. Run the following command:
    ```sh
    $ make despatcher
    ```

4. To view the optimization results, open the following URL in your browser and execute the queue:
    ```
    http://localhost:5000/
    ```

Note: Make sure the Docker container is running before executing the `queue_despatcher.py` script and accessing the optimization results in the browser.

### Debugging

For debugging the code inside the Docker container, please refer to the instructions provided in the [docker.md](docker.md) file.

## Testing

This project utilizes pytest for implementation, development, and testing purposes. To run the tests, execute the following command:

- Using `docker-compose`:
    ```sh
    $ docker compose run --service-ports science pytest tests
    ```

Alternatively, you can use the following command if available:

- Using `make`:
    ```sh
    $ make test
    ```

These commands will run the test suite and provide you with the test results.

***

## Adding New Packages

To include packages that are not listed in the [pyproject.toml](pyproject.toml) file, follow these steps:

1. Use the following command to add the desired package:
    ```sh
    poetry add package
    ```

## Adding Local Dependencies

To add local dependencies to your project, follow these steps:

1. Place the `.tar.gz` file of the dependency in the `dependencies/` directory. For example, let's add `depedencies/toolkit.tar.gz` as a local dependency.

2. Add the dependency using Poetry by running the following command:
    ```
    poetry add ./dependencies/toolkit.tar.gz
    ```

For more information on managing dependencies with Poetry, refer to the official documentation at [https://python-poetry.org/docs/cli/](https://python-poetry.org/docs/cli/).

***

## Adding new exceptions

- Create exception class, inherits from ExpectedException
- Import class properly 
``` python
from architecture_optimization_framework.utilities.expected_exception import ExpectedException
```
- Create new element in [exception_code.json](exception_code.json)
- Be careful to inform an erro code following the format "Error_XXXX"

***

## Useful methods

The following methods are useful to check results graphically or assemblying a presentation

- `coffin_to_csv`: saves all the demands of a coffin in a csv file locally
- `coffin_to_excel`: saves all the demands of a coffin in an excel file locally
- `plot_two_attribute_coffin`: generate a graph of the variation of two attributes along the coffin
- `plot_coffin_rough_dimensions`: generate a graph of the variation in width and temperature along the coffin
- `plot_buffer_graph`: plots a buffer graph for demands visualization per interval
- `plot_coffin_occupation_gantt`: plots a gantt chart for a coffin resource occupation
- `plot_coffin_object`: plots a coffin object, for demand visualization over time
- `save_coffin_time_data_csv`: saves all the demands of a coffin time data of each resource in a csv file locally
- `create_pm_schedule_list`: creates a json with pm_schedule from coffin and temporal simulation info

***

## Storing Password

If you don't want to be asked to type in the password every time you push or pull, you can store it using.
```sh
git config --global credential.helper store
```

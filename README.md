# URL Shortner

This project implements a simple command line utility to create Short URLs for a generic URL of any length

## Requirements

This project uses python so you need to have it installed on your machine.

(Optional) A `mise.toml` file is included for bootstrapping the local environment.
If you have [mise](https://mise.jdx.dev/) installed already, run `mise trust` in the project directory to use the provided `mise.toml` configuration file.

For python dependenceis, this project uses [uv](https://docs.astral.sh/uv/).
If you don't have it (and you don't use `mise`) please install it before using this project.

To install the required dependencies with `uv`, run the following command:
```bash
uv sync
```

The project also requires a MongoDB instance to store urls. 
You can provide the connection string for MongoDB, together with other application settings, with environment variables.
Copy the example `.env.example` file to `.env` and modify it with the required values

## Usage

To create a short URL from a given url run:
```bash
uv run url-shortner --minify=<YOUR_URL>
```
The application will print the short URL in the console output

To retrieve the original URL from a short URL run:
```bash
uv run url-shortner --expand=<SHORT_URL>
```

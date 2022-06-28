# PreClinVar
A ClinVar API submission helper written in FastAPI

## Installing the application on a local conda environment

Given a conda environment sontaining python 3.8 and [poetry](https://github.com/python-poetry/poetry), clone the repository from Github with the following command:

```
git clone https://github.com/Clinical-Genomics/preClinVar.git
```

The command will create a folder named `preClinVar` in your current working directory. Move inside this directory:

```
cd preClinVar
```

And install the software with poetry:

```
poetry install
```

You can run an instance of the server by typing:

```
uvicorn preClinVar.main:app --reload
```

The server will run on localhost and default port 8000 (http://127.0.0.1:8000)

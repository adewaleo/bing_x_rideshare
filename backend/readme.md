# Bing Project Python Backend

## Setting up the development environment (based on [azdev](https://github.com/Azure/azure-cli-dev-tools/blob/master/README.md))

1. Install Python 3 from http://python.org. Please note that the version of Python that comes preinstalled on OSX is 2.7.
2. Change directory to the root of the repo.
3. Create a new virtual environment for Python at the root of the repo. 
   Virtual environments allow you to isolate dependencies for each of your python project. You can do this by running:

    ```BatchFile
    python -m venv env
    ```
    or
    ```Shell
    python3 -m venv env
    ```

4. Activate the env virtual environment by running:

    Windows CMD.exe:
    ```BatchFile
    env\scripts\activate.bat
    ```

    Windows Powershell:
    ```
    env\scripts\activate.ps1
    ```

    OSX/Linux (bash):
    ```Shell
    source env/bin/activate
    ```

5. Install the backend's dependencies from the requirements.txt file:
   ```
   pip install -r requirements.txt

   ```
   
## Run the development server

1. Ensure that the virtual environment is activated, by running its activate script.
2. Start the Flask App. First ensure that you are at the root directory:
   ```bash
      python backend/app.py
   ```
3. Test the API using [postman](https://www.getpostman.com/products), [curl or requests](https://flask-restful.readthedocs.io/en/latest/quickstart.html#resourceful-routing).


## References
1. [Flask Docs - Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
2. [Flask Restful Docs - Quickstart](https://flask-restful.readthedocs.io/en/latest/quickstart.html#quickstart)
3. [Flask Restful Docs - Intermediate Usage](https://flask-restful.readthedocs.io/en/latest/intermediate-usage.html#intermediate-usage)



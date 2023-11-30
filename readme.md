## Case Goal: Developing Intelligent Document Management Endpoints.

In this case, the primary objective is to create robust endpoints that enhance the management and analysis of documents within a given folder. The endpoints will be designed to provide valuable insights into the folder's content and facilitate document classification analysis.

## How it works
Create a folder called ```rebelsai-data``` next to the root of this project. This volume will be linked with the docker container. This will be the data from which you can add filepaths to the endpoints.

### Endpoints
- ```127.0.0.1:8000/?path=path_to_folder``` --> Will return data about the folder in a JSON format.
- ```127.0.0.1:8000/classify?path=path_to_file``` --> If not already done so will label the file with ```urgent``` or ```not urgent``` and returns this information in JSON format.

## Development
1. Duplicate the .env-example file and rename to ```.env```. Fill in the needed environment variables
2. In the root of the project there are multiple Make commands (when using windows copy the commands from the make file in your terminal):
    - ```make up``` --> to start the app
    - ```make stop``` --> to stop the app
    - ```make down``` --> to delete the app (in docker)
    - ```make logs``` --> to view the app activity
    - ```make migrate``` --> to update the database with all the columns
3. When running ```make up``` the app is running on localhost port 8000 --> ```127.0.0.1:8000```
4. Only run ```make migrate``` when new database columns have been created
5. The following commands are only for development
    - ```make makemigrations``` --> to update mirgation files when changes have been made
    - ```make db-redeploy``` --> to reset the database to a previous state. You need a ```database.bak``` in the root of the project, which is a backup of the database. 
    - ```make install``` --> to install new added dependencies inside requirements.txt
    - To get a superuser first run ```make shell``` and then ```pyhton manage.py createsuperuser```

## Deployment
Deployment is not included in this repository. I reconmend to have the document classifier hosted in its own scaleble envoronment: azure functions or aws lambda. The django application can be hosted on any web server.
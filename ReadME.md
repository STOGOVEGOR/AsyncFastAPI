## Async data request API

Here is no `.env` file only because it's not necessary for exactly this task.


Endpoints:
- **/data** - return dictionary of sorted items from DB;
- **/check_connection** - just to be sure that DB is ready;

How to run:
1. docker-compose up --build


## Tests

To run tests (`pytest` in terminal) please comment and uncomment imports from *database* and *modules* in `main.py` and `models.py`. I can't deal with it, sorry.
# Capstone Agency API

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. It holds three important role.
- #### Casting Assistant
    Can view actors and movies
- #### Casting Director
    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies
- #### Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the database


# Features!

  - GET
    `https://capstone-agency.herokuapp.com/actors`
    ``` 
    content_type='application/json',
    headers={'Authorization': f'Bearer {assistant_token/director_token/executive_token}'}
    ```
    `https://capstone-agency.herokuapp.com/actors/1`
    ```
    content_type='application/json',
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
    
    `https://capstone-agency.herokuapp.com/movies`
    ```
    content_type='application/json',
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
    
    `https://capstone-agency.herokuapp.com/movies/1`
    ```
    content_type='application/json',
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
- POST
    `https://capstone-agency.herokuapp.com/movies`
    ```
    content_type='application/json',
    data={'release_date':'yyyy/mm/dd','title':'anything'},
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
    
    `https://capstone-agency.herokuapp.com/actors`
    ```
    content_type='application/json',
    data={'name':'anything','age':'20',gender:"malee/female"},
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
- PATCH
    `https://capstone-agency.herokuapp.com/movies/1/edit`
    ```
    content_type='application/json',
    data={'release_date':'yyyy/mm/dd' or 'title':'anything' or both},
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
    
    `https://capstone-agency.herokuapp.com/actors/1/edit`
    ```
    content_type='application/json',
    data={'name':'anything' or 'age':'20'or gender:"malee/female" or both},
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
- DELETE
    `https://capstone-agency.herokuapp.com/movie/1/delete`
    ```
    content_type='application/json',
    headers={'Authorization': f'Bearer {executive_token}'}
    ```
    
    `https://capstone-agency.herokuapp.com/actor/1/delete`
    ```
    content_type='application/json',
    headers={'Authorization': f'Bearer {executive_token}'}
    ```

>  Tests


Tests can be run using a python library Pytest. 

> clone the repository
> run `pip install -r requirements.txt`
> Create a database and add its path to environment variables.
> add environment variables to a local .env file and run `source .env`
> run `pytest`

Thank you !!!


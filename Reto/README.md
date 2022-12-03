
# Reto Movilidad Urbana

Code implementation using Python and C# for Unity, it creates a given amount 
of cars with a random choosed destination. They search for their designated 
destination and move according to the grid directions, they also follow the 
the traffic lights according to their indication (red = stop / green = go).
 

 Python:
 Creation of Agents, Model and Servers(Flask and Modular server for visualization with mesa). [Flask has not been implemented yet 28/11/22]

 Update[2/12/22]: Flask and Modular server have been implemented on the proyect 


 C#: Unity code for creation of Agents objects.  


## PDF Evidencias

[Revisión 3 - Avance al 60%](https://docs.google.com/document/d/1hMn1L58V69s3SMKBy_CovqNTdjIEl82z41kou12D--0/edit?usp=sharing)

[Evidencia 2. Documento](https://docs.google.com/document/d/1410A9130NnOKr4161wfeVJl0irlNftKyVbuUZ-Mvf_0/edit?usp=sharing)

## Relfexiones individuales

* [Carlos Alan Gallegos Espíndola ---- A01751117](https://docs.google.com/document/d/1cm1S3qipzg9TQA8DAmGJ9aHwsRqioQgcW3-VWe95d2o/edit)
* [Jorge Rojas Rivas ---- A01745334](https://docs.google.com/document/d/1j8-SZlDl8OG8ClCWr1VZV-7f5rz3xXZV/edit?usp=sharing&ouid=108466048207018234991&rtpof=true&sd=true)
* [Omar Rodrigo Talavera  ---- A01752221](https://docs.google.com/document/d/15gdy3zgNnz9glJkmew_eWF7RwBgEuJdko9a6SItwu6U/edit?usp=sharing)
* [Paulina Guadalupe Alva Martínez ---- A01750624](https://docs.google.com/document/d/13ofsOY7S3cuEgHku5t0i3M1D2QT5jUAo9rSpgGGDjTE/edit?usp=sharing)
## How to setup 

* [Setup for python](https://clipchamp.com/watch/4cYgZWiCIwU)
* [Setup for unity](https://clipchamp.com/watch/7OkkSoEfe8m)

## Run test on Modular server and Flask with Unity

* [Mesa Modular server run](https://clipchamp.com/watch/ISf74LASAyb)
* [Unity Flask server run](https://clipchamp.com/watch/W7lQI76Xmn2)

## Folder with videos

[Folder on Google Drive](https://drive.google.com/drive/folders/1QDMx5lPd0LGqwbSO6fIvhgnaXUfQppSW?usp=share_link)
## API Reference

#### Initiate the Model 

```http
  POST http://localhost:8585/init
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `MAXCARS` | `int` | **Required**. Max. number of cars in simulation |

#### Get cars data

```http
  GET http://localhost:8585/getCars
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | Id of Car |
| `x`      | `int` | X position of Car |
| `y`      | `int` | Y position of Car |
| `z`      | `int` | Z position of Car |
| `arrived`      | `bool` | True if car arrived else false |
| `status`      | `bool` | True if car has not crashed else false |
| `facing`      | `string` | What direction is car facing [North, South, East, North] |

#### Get roads data

```http
  GET http://localhost:8585/getRoads
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | Id of Road |
| `x`      | `int` | X position of Road |
| `y`      | `int` | Y position of Road |
| `z`      | `int` | Z position of Road |

#### Get destinations data

```http
  GET http://localhost:8585/getDestination
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | Id of Destination |
| `x`      | `int` | X position of Destination |
| `y`      | `int` | Y position of Destination |
| `z`      | `int` | Z position of Destination |

#### Get obstacles data

```http
  GET http://localhost:8585/getObstacles
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | Id of Obstacles |
| `x`      | `int` | X position of Obstacles |
| `y`      | `int` | Y position of Obstacles |
| `z`      | `int` | Z position of Obstacles |

#### Get traffic lights data

```http
  GET http://localhost:8585/getTraficlights
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | Id of Traffic light |
| `x`      | `int` | X position of Traffic light |
| `y`      | `int` | Y position of Traffic light |
| `z`      | `int` | Z position of Traffic light |
| `state`      | `bool` | Z position of Road |

#### Update the model

```http
  GET http://localhost:8585/getTraficlights
```




## Run Locally



Run python server

```bash
{path of current folder} & "{path of python.exe}" "{path of stored proyect}/Reto/Python/server.py"
```


## FAQ

#### Does it has a maximum number of cars that it can run?

Yes, we recommend 6 or less but can manage up to 10 (Best Scenario on 4 cars)

#### How do I install Flask or/and Mesa?
##### On windows 
```console
C: pip install Flask
C: pip install Mesa
``` 
##### On Linux 
```console
foo@foo:~$ pip install Flask
foo@foo:~$ pip install Mesa
``` 

#### What is the server port designated on the Server{F/M}.py?

Server port = 8585
## Authors


- [@AlanGallegosEsp](https://github.com/AlanGallegosEsp) Python and C# implementation 
- [@JeorgeReds78](https://github.com/JeorgeReds78) Diagram and documentation making
- [@GlitcherSoul](https://github.com/GlitcherSoul) C# implementation
- [@PatoAm10](https://github.com/AlanGallegosEsp) C# implementation and Diagram with documentation making
=======
- [@AlanGallegosEsp](https://github.com/AlanGallegosEsp) Python and C# implementation
- [@JeorgeReds78](https://github.com/JeorgeReds78) Documentation and Diagram maker
- [@GlitcherSoul](https://github.com/GlitcherSoul) Unity model creation
- [@PatoAm10](https://github.com/AlanGallegosEsp) Unity model creation



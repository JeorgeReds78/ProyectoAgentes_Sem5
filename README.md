
# Actividad integradora

Code implementation using Python and C# for Unity, it creates five robots that order boxes taking them to places that are designed.
 

 Python:
 Creation of Agents, Model and Servers(Flask and Modular server for visualization with mesa).

 C#: Unity code for creation of Agents objects .  


## PDF Evidencia 1. Actividad Integradora

[Evidencia 1. Actividad Integradora](https://docs.google.com/document/d/1P6cmY-huxJjncviCYMf9ys2l0nOaxpdLQtZs5J84VtE/edit?usp=sharing)


## API Reference

#### Initilize model

```http
  Post localhost:{port}/init
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `number_boxes` | `int` | **Required**. Number of boxes on simulation |
| `width` | `int` | **Required**. Width for the grid |
| `height` | `int` | **Required**. Height for the grid |

### Get bots info

```http
  GET localhost:{port}/getBots
```
### Get boxes info

```http
  GET localhost:{port}/getBoxes
```
### Get updates
```http
  GET localhost:{port}/update
```



## Run Locally



Run python server

```bash
{path of current folder} & "{path of python.exe}" "{path of stored proyect}/Integradora/ServerF.py"
```


## FAQ

#### Does it has a maximum number of boxes that it can run?

Yes, it has to be 20 less that the maximum grid (width * height) 

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

Server port = 8080
## Authors

- [@AlanGallegosEsp](https://github.com/AlanGallegosEsp) Python and C# implementation
- [@JeorgeReds78](https://github.com/JeorgeReds78) Python implementation
- [@GlitcherSoul](https://github.com/GlitcherSoul) C# implementation
- [@PatoAm10](https://github.com/AlanGallegosEsp) C# implementation


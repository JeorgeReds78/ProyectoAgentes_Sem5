
# Reto Movilidad Urbana

Code implementation using Python and C# for Unity, it creates a given amount 
of cars with a random choosed destination. They search for their designated 
destination and move according to the grid directions, they also follow the 
the traffic lights according to their indication (red = stop / green = go).
 

 Python:
 Creation of Agents, Model and Servers(Flask and Modular server for visualization with mesa). [Flask hasnt been implemented yet 28/11/22]


 C#: Unity code for creation of Agents objects.  


## PDF Revision 60%

[Revisión 3 - Avance al 60%](https://docs.google.com/document/d/1hMn1L58V69s3SMKBy_CovqNTdjIEl82z41kou12D--0/edit?usp=sharing)




## Run Locally



Run python server

```bash
{path of current folder} & "{path of python.exe}" "{path of stored proyect}/Reto/Python/server.py"
```


## FAQ

#### Does it has a maximum number of cars that it can run?

Yes, we recommend 10 or less 

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


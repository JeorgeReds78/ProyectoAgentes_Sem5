// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

// ? Json 
// * Json CarData
[Serializable]
public class CarData{
    public string id, facing;
    public float x, y, z;
    public bool arrived;

    public CarData(string id, float x, float y, float z, string facing, bool arrived)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.facing = facing;
        this.arrived = arrived;
    }
}
// * Json TrafficLightData
[Serializable]
public class TrafficLightData{
    public string id;
    public float x, y, z;
    public bool state;

    public TrafficLightData(string id, float x, float y, float z, bool state)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
    }
}
// * Json RoadData
[Serializable]
public class RoadData{
    public string id;
    public float x, y, z;

    public RoadData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    } 
}
// * Json DestinationData
[Serializable]
public class DestinationData{
    public string id;
    public float x, y, z;

    public DestinationData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}
// * Json ObstacleData
[Serializable]
public class ObstacleData{
    public string id;
    public float x, y, z;

    public ObstacleData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

// ? Json of json
// * Json CarDataList
[Serializable]
public class CarsData{
    public List<CarData> positions;

    public CarsData() => this.positions = new List<CarData>();
}

// * Json RoadDataList
[Serializable]
public class RoadsData{
    public List<RoadData> positions;

    public RoadsData() => this.positions = new List<RoadData>();
}

// * Json TrafficLightDataList
[Serializable]
public class TrafficLightsData{
    public List<TrafficLightData> positions;

    public TrafficLightsData() => this.positions = new List<TrafficLightData>();
}

// * Json DestinationDataList
[Serializable]
public class DestinationsData{
    public List<DestinationData> positions;

    public DestinationsData() => this.positions = new List<DestinationData>();
}

// * Json ObstacleDataList
[Serializable]
public class ObstaclesData{
    public List<ObstacleData> positions;

    public ObstaclesData() => this.positions = new List<ObstacleData>();
}

public class AgentController : MonoBehaviour
{
    // ? Urls to get data
    string serverUrl = "http://localhost:8585";
    string getCarsEndpoint = "/getCars";
    string getTraficlightsEndpoint = "/getTraficlights";
    string getDestinationEndpoint = "/getDestination";
    string getObstaclesEndpoint = "/getObstacles";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    // ? Dataclasses 
    CarsData carsData;
    RoadsData roadsData;
    TrafficLightsData trafficLightsData;
    DestinationsData destinationsData;
    ObstaclesData obstaclesData;
    // ? Gameobjects
    Dictionary<string, GameObject> cars,trafficLights;
    // ? Data dictionary
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false;

    public GameObject carPrefab, semsmafo, plane;
    public int MAXCARS;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        // ? Init dataclasses
        carsData = new CarsData();
        roadsData = new RoadsData();
        trafficLightsData = new TrafficLightsData();
        destinationsData = new DestinationsData();
        obstaclesData = new ObstaclesData();

        // ? Init gameobjects
        cars = new Dictionary<string, GameObject>();
        trafficLights = new Dictionary<string, GameObject>();

        // ? Init data dictionary
        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();


        plane.transform.localScale = new Vector3((float)24/10, 1, (float)24/10);
        plane.transform.localPosition = new Vector3((float)24/2-0.5f, 0, (float)24/2-0.5f);
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                cars[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) cars[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetCarsData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("MAXCARS", MAXCARS.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            // StartCoroutine(GetObstacleData());
        }
    }

    IEnumerator GetCarsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            carsData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

            foreach(CarData agent in carsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);

                    if(!started)
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        cars[agent.id] = Instantiate(carPrefab, newAgentPosition, Quaternion.identity);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(agent.id, out currentPosition))
                            prevPositions[agent.id] = currentPosition;
                        currPositions[agent.id] = newAgentPosition;

                    }
            }

            updated = true;
            if(!started) started = true;
        }
    }

    // IEnumerator GetObstacleData() 
    // {
    //     UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
    //     yield return www.SendWebRequest();

    //     if (www.result != UnityWebRequest.Result.Success)
    //         Debug.Log(www.error);
    //     else 
    //     {
    //         obstacleData = JsonUtility.FromJson<CarsData>(www.downloadHandler.text);

    //         Debug.Log(obstacleData.positions);

    //         foreach(CarData obstacle in obstacleData.positions)
    //         {
    //             Instantiate(obstaclePrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
    //         }
    //     }
    // }
}

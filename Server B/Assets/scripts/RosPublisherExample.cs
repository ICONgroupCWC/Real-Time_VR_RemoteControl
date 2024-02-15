using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosPos = RosMessageTypes.UnityRoboticsDemo.RbtPoseMsg;
using RosLdr = RosMessageTypes.UnityRoboticsDemo.PoseMsg;
using System.Collections;
using System.Collections.Generic;
using System;

/// <summary>
///
/// </summary>
public class RosPublisherExample : MonoBehaviour
{
    ROSConnection u_Ros;

    public string topic1Name = "/pos_robt";
    public string topic2Name = "/ldata";
    public string topic3Name = "/pathPlan";

    // The game object
    public GameObject Jetbot;
    public GameObject cube2;
    public GameObject cube;

    // Vector3 robot_location = new Vector3(20.0f,0.049f,-5.0f);
    Vector3 robot_location = new Vector3(0.0f,0.049f,0.0f);
    Vector3 initial_pos  = new Vector3(27.361f,0.0f,-6.181f);
    Vector3 actual_location = new Vector3(0.0f,0.0f,0.0f);

    Quaternion newRotation = new Quaternion(0.0f, 0.0f, 0.0f, 1.0f);


    Vector3 screen_Initialpose = new Vector3(20.291f,0.405f,-4.154f);
    Vector3 screen_location = new Vector3(0.0f,0.0f,0.0f);
    
    Vector3 cube2Offset;


    private LineRenderer[] lineRenderers; // Array of LineRenderers


    public Color lineColor;

    Vector3 SetPoint1 = new Vector3(10.0f,0.0f,10.0f);
    Vector3 SetPoint2 = new Vector3(10.0f,0.3f,10.0f);

    List<Vector3> vector3srtList = new List<Vector3>();
    List<Vector3> vector3stpList = new List<Vector3>();
    
    bool flag1 = true;
    bool flag2 = true;

    Vector3 target = new Vector3(0.0f,0.0f,0.0f);
    Vector3 initialPose;
    List<Vector3> trajectoryPoint = new List<Vector3>();

    private LineRenderer lineRenderer;
    public Color pathColor;

    public GameObject Flag;

    Vector3 FlaginitialPose = new Vector3(0.0f,0.0f,0.0f);
    int numCornerVertices = 10;

    List<Vector3> newtraPoint = new List<Vector3>();

    int index = 0;
    float speed = 0.1f;

    int k = 0;
    float rotationSpeed = 5.0f;
    Vector3 prvPos = new Vector3(0.0f,0.0f,0.0f);
    Quaternion prvRot = new Quaternion(0.0f,0.0f,0.0f,1.0f);

    void Start()
    {
        u_Ros = ROSConnection.GetOrCreateInstance();
        //Debug.Log(RosPo.type);
        u_Ros.Subscribe<RosPos>(topic1Name, get_pos);
        u_Ros.Subscribe<RosLdr>(topic2Name, get_scanData);
        u_Ros.Subscribe<RosLdr>(topic3Name, get_pathData);

        // cubeOffset = cube2.transform.position - cube.transform.position;
        
        cube2Offset = cube2.transform.position - Jetbot.transform.position;

        if (lineRenderers != null)
        {
            foreach (var lineRenderer1 in lineRenderers)
            {
                Destroy(lineRenderer1.gameObject);
            }
        }
            
        lineRenderers = new LineRenderer[1147];

           

        for(int i = 0; i <1147; i++){

            lineRenderers[i] = new GameObject().AddComponent<LineRenderer>();
    
        
            lineRenderers[i].positionCount = 2;
            lineRenderers[i].startWidth = 0.02f; 
            lineRenderers[i].endWidth = 0.02f;
            lineRenderers[i].material.color = lineColor;

            lineRenderers[i].SetPosition(0,SetPoint1);
            lineRenderers[i].SetPosition(1,SetPoint2);
        }
        
        initialPose = new Vector3(Jetbot.transform.position.x,0.01f,Jetbot.transform.position.z);
        lineRenderer = new GameObject().AddComponent<LineRenderer>();
        lineRenderer.positionCount = 2;
        lineRenderer.startWidth = 0.02f; 
        lineRenderer.endWidth = 0.01f;
        lineRenderer.material.color = pathColor;
        lineRenderer.loop = false;
        lineRenderer.numCornerVertices  = numCornerVertices;

        Flag.transform.position = FlaginitialPose;

    }

    public void get_pos(RosPos msg) {

        robot_location = new Vector3(-msg.pos_Y,0.049f,msg.pos_X);

        
        
        newRotation = new Quaternion(msg.rot_Y,-msg.rot_Z,msg.rot_X,msg.rot_W);
       
       

        // print(actual_location);

       

        // Update the position and rotation of 'cube2'
        // cube2.transform.position = actual_location + screen_Initialpose + ;
        // cube2.transform.rotation = newRotation;
        
        
        

    }

    public void get_scanData(RosLdr msg)
    {
        int num_points = msg.Xdata.Length;
       
        vector3srtList.Clear();
        vector3stpList.Clear();
        
        
        
         for (int i = 0; i < num_points; i++){

            vector3srtList.Add(new Vector3(-msg.Xdata[i],0.0f,msg.Zdata[i]));
            vector3stpList.Add(new Vector3(-msg.Xdata[i],0.3f,msg.Zdata[i]));
           

         }
            
        // print(target);
        // print("sdkgh");


    }


    public void get_pathData(RosLdr msg)
    {
        int num_points = msg.Xdata.Length;
       
        trajectoryPoint.Clear();
        target = initialPose + new Vector3(-msg.Xdata[num_points-1],0.0f,msg.Zdata[num_points-1]);
        
         for (int i = 0; i < num_points; i++){

            Vector3 Point = initialPose + new Vector3(-msg.Xdata[i],0.0f,msg.Zdata[i]);

            trajectoryPoint.Add(Point);
           

         }
            
        // print(target);
        // print("sdkgh");


    }

    public void Update(){

        bool connection = u_Ros.HasConnectionError;

        
        if(connection==false){
            actual_location = initial_pos + robot_location;

            Vector3 loc = new Vector3(0.0f,0.049f,0.0f);

            Jetbot.transform.position = actual_location;

            Jetbot.transform.rotation = newRotation;

            Vector3 rotatedOffset = newRotation * cube2Offset;
            cube2.transform.position = actual_location + rotatedOffset;
            cube2.transform.rotation = newRotation;



        

            Vector3 RobotPose = new Vector3(actual_location.x,0,actual_location.z); 
        
            if(vector3srtList.Count>0){

                int dataSize = vector3srtList.Count;
                for(int i = 0; i < dataSize; i++){

                    Vector3 pose1 = RobotPose + newRotation*vector3srtList[i];
                    Vector3 pose2 = RobotPose + newRotation*vector3stpList[i];

                    lineRenderers[i].SetPosition(0,pose1);
                    lineRenderers[i].SetPosition(1,pose2);

                }

                for(int i=dataSize; i<1147;i++){
                    lineRenderers[i].SetPosition(0,SetPoint1);
                    lineRenderers[i].SetPosition(1,SetPoint2);
                }

            }

            else{
                for(int i = 0; i <1147; i++){

                    lineRenderers[i].SetPosition(0,SetPoint1);
                    lineRenderers[i].SetPosition(1,SetPoint2);
                }
            }

            if(trajectoryPoint.Count>=2 &&flag1 == true){

                Flag.transform.position = new Vector3(target.x,0.3f,target.z);
                lineRenderer.positionCount = trajectoryPoint.Count;
                lineRenderer.SetPositions(trajectoryPoint.ToArray());
            
                
                // flag1 = false;
                // flag2 = true;
                // index = 0;

            
            }

            flag1 = false;
            flag2 = true;
            index = 0;

            
        }

        else{
            

            if(flag1==false){

                Vector3 rbtPose = actual_location;

                if(flag2 == true){
                    
                    
                    float min_val = 1000000000000.0f;
                    int minIndx = 0;
                    for (int i=0;i<trajectoryPoint.Count;i++){
                        float distance = Mathf.Sqrt((trajectoryPoint[i].x-rbtPose.x)*(trajectoryPoint[i].x-rbtPose.x)+(trajectoryPoint[i].z-rbtPose.z)*(trajectoryPoint[i].z-rbtPose.z));

                        if(distance < min_val){
                            minIndx = i;
                            min_val = distance;
                        }

                    }

                    newtraPoint.Clear();
                    newtraPoint.Add(new Vector3(rbtPose.x,0.01f,rbtPose.z));

                    for(int i=minIndx;i<trajectoryPoint.Count;i++){
                        newtraPoint.Add(trajectoryPoint[i]);
                    }

                    lineRenderer.positionCount = newtraPoint.Count;
                    lineRenderer.SetPositions(newtraPoint.ToArray());
                    flag2 = false;
                    prvPos = actual_location;
                    prvRot = newRotation;
                   
                
                }
                
                Vector3 destination = newtraPoint[index];
                destination = new Vector3(destination.x,0.049f,destination.z);

                Vector3 newPos = Vector3.MoveTowards(prvPos,destination,speed*Time.deltaTime);
                Quaternion targetRotation = Quaternion.LookRotation(newPos - prvPos);

                Jetbot.transform.rotation = Quaternion.Slerp(prvRot, targetRotation, Time.deltaTime * rotationSpeed);
                Jetbot.transform.position = new Vector3(newPos.x,0.049f,newPos.z);
                // cube.transform.position = newPos;

                float dis = Mathf.Sqrt((newPos.x-destination.x)*(newPos.x-destination.x)+(newPos.z-destination.z)*(newPos.z-destination.z));
                prvPos = newPos;
                prvRot = targetRotation;
              
                if(dis <=0.05f){

                    if(index <newtraPoint.Count-1){
                        index++;
                    }
                    else{
                        Jetbot.transform.position = newtraPoint[index];
                    }

                   
                
                }

            }



            
        }

    }

   
}

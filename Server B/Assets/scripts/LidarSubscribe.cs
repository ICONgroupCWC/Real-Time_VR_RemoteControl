using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosLdr = RosMessageTypes.UnityRoboticsDemo.PoseMsg;
            


public class LidarSubscribe : MonoBehaviour
{
    ROSConnection ros_con;

    public string topicName = "/ldata";
    public GameObject cube;
   
    
    
    private LineRenderer[] lineRenderers; // Array of LineRenderers


    public Color lineColor;

    Vector3 SetPoint1 = new Vector3(10.0f,0.0f,10.0f);
    Vector3 SetPoint2 = new Vector3(10.0f,0.3f,10.0f);

    List<Vector3> vector3srtList = new List<Vector3>();
    List<Vector3> vector3stpList = new List<Vector3>();

    void Start()
    {
        ros_con = ROSConnection.GetOrCreateInstance();

        ros_con.Subscribe<RosLdr>(topicName, get_scanData);

        if (lineRenderers != null)
        {
            foreach (var lineRenderer in lineRenderers)
            {
                Destroy(lineRenderer.gameObject);
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
   

    void Update()
    {
        Quaternion newRotation = cube.transform.rotation;
        print(newRotation);

        Vector3 RobotPose = new Vector3(cube.transform.position.x,0,cube.transform.position.z); 
        print(RobotPose);
        if(vector3srtList.Count>0){

            int dataSize = vector3srtList.Count;
            for(int i = 0; i < dataSize; i++){

                Vector3 pose1 = RobotPose + vector3srtList[i];
                Vector3 pose2 = RobotPose + vector3stpList[i];

                lineRenderers[i].SetPosition(0,newRotation*pose1);
                lineRenderers[i].SetPosition(1,newRotation*pose2);

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
        

        
    }


}

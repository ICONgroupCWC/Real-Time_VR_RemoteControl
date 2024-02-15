using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosPose = RosMessageTypes.UnityRoboticsDemo.PoseMsg;

public class pathPlan : MonoBehaviour
{
    ROSConnection ros_con;

    public string topicName = "/pathPlan";
    public GameObject Jetbot;
    List<Vector3> trajectoryPoint = new List<Vector3>();
    Vector3 target = new Vector3(0.0f,0.0f,0.0f);
    Vector3 initialPose;

    bool flag1 = true;
    bool flag2 = true;

    private LineRenderer lineRenderer;
    public Color lineColor;

    public GameObject Flag;
    

    Vector3 FlaginitialPose = new Vector3(0.0f,0.0f,0.0f);
    int numCornerVertices = 10;

    List<Vector3> newtraPoint = new List<Vector3>();
    int index = 1;
    float speed = 1.0f;

    void Start()
    {
        ros_con = ROSConnection.GetOrCreateInstance();

        ros_con.Subscribe<RosPose>(topicName, get_pathData);
        initialPose = new Vector3(Jetbot.transform.position.x,0.01f,Jetbot.transform.position.z);
        lineRenderer = new GameObject().AddComponent<LineRenderer>();
        lineRenderer.positionCount = 2;
        lineRenderer.startWidth = 0.02f; 
        lineRenderer.endWidth = 0.01f;
        lineRenderer.material.color = lineColor;
        lineRenderer.loop = false;
        lineRenderer.numCornerVertices  = numCornerVertices;

        Flag.transform.position = FlaginitialPose;
  
        
    }

    public void get_pathData(RosPose msg)
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
   
    void Update()
    {
        bool connct = ros_con.HasConnectionError;
        if(connct==false){

            if(trajectoryPoint.Count>=2 &&flag1 == true){



                Flag.transform.position = new Vector3(target.x,0.3f,target.z);

                // print(trajectoryPoint[0]);
                // print(trajectoryPoint[trajectoryPoint.Count-1]);
                lineRenderer.positionCount = trajectoryPoint.Count;
                lineRenderer.SetPositions(trajectoryPoint.ToArray());
            
                // for (int i = 0; i < trajectoryPoint.Count; i++)
                // {
                //     lineRenderer.SetPosition(i,trajectoryPoint[i]);
                    
                // }
                flag1 = false;

            
            }
        }

        else if(flag1==false && connct== true ){
            Vector3 rbtPose = Jetbot.transform.position;

            if(flag2 == true){
                print(trajectoryPoint.Count);
                float min_val = 1000000000000.0f;
                int minIndx = 0;
                for (int i=0;i<trajectoryPoint.Count;i++){
                    float distance = Mathf.Sqrt((trajectoryPoint[i].x-rbtPose.x)*(trajectoryPoint[i].x-rbtPose.x)+(trajectoryPoint[i].y-rbtPose.y)*(trajectoryPoint[i].y-rbtPose.y));

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
                Jetbot.transform.position = newtraPoint[0];
            }
            

            Vector3 destination = newtraPoint[index];
            Vector3 newPos = Vector3.MoveTowards(Jetbot.transform.position,destination,speed*Time.deltaTime);
            Jetbot.transform.position = newPos;

            float dis = Vector3.Distance(Jetbot.transform.position,destination);

            if(dis <=0.01f){

                if(index <newtraPoint.Count-1){
                    index++;
                }
                
            }

            // print(rbtPose);
        }
        
        
    }

   
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using Unity.Robotics.ROSTCPConnector;
using RosImg = RosMessageTypes.UnityRoboticsDemo.ImgMsg;
// using RosMessageTypes.UnityRoboticsDemo;
// using RosMessageTypes.Sensor;
// using RosMessageTypes.Std;
// using RosMessageTypes.BuiltinInterfaces;
using System;

public class CamScript : MonoBehaviour
{
    
    Texture2D texRos;
    Texture2D texture;
    
    ROSConnection m_Ros;
    // CompressedImageMsg img_msg;
    string imagetopic = "/img_pub";
    public RawImage display;
    // Start is called before the first frame update
    void Start()
    {
        texture = new Texture2D(640, 480, TextureFormat.RGB24, false);
        m_Ros = ROSConnection.GetOrCreateInstance();
        Debug.Log(m_Ros.RosIPAddress);
        m_Ros.Subscribe<RosImg>(imagetopic, get_img);
    }

  
    // Update is called once per frame
    public void get_img(RosImg img) {

        if (display == null)
        {
            Debug.LogError("RawImage (display) is not assigned.");
            return;
        }

        if (img.data == null || img.data.Length == 0)
        {
            Debug.LogError("Received empty image data.");
            return;
        }

        

        texRos = DecodeImage(img.data, 640, 480, texture);

        if (texRos != null)
        {
            // Optionally convert BGR to RGB (if needed)
            // BgrToRgb(texRos);

            // Update the RawImage texture
            display.texture = texRos;
        
        }
        
        
    }

    public Texture2D DecodeImage(byte[] imageData, int width, int height, Texture2D texture)
    {
        if (imageData == null || imageData.Length == 0)
        {
            Debug.LogError("Received empty image data.");
            return null;
        }

        // Texture2D texture = new Texture2D(width, height, TextureFormat.RGB24, false);
        texture.LoadImage(imageData);

        if (texture.width != width || texture.height != height)
        {
            Debug.LogError("Received image data with incorrect dimensions.");
            return null;
        }

        // Optionally convert BGR to RGB (if needed)
        // BgrToRgb(texture);

        return texture;
    }
  
}

//Do not edit! This file was generated by Unity-ROS MessageGeneration.
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using Unity.Robotics.ROSTCPConnector.MessageGeneration;
using RosMessageTypes.Std;

namespace RosMessageTypes.UnityRoboticsDemo
{
    [Serializable]
    public class ImgMsg : Message
    {
        public const string k_RosMessageName = "unity_robotics_demo_msgs/Img";
        public override string RosMessageName => k_RosMessageName;

        public HeaderMsg header;
        public string format;
        public byte[] data;

        public ImgMsg()
        {
            this.header = new HeaderMsg();
            this.format = "";
            this.data = new byte[0];
        }

        public ImgMsg(HeaderMsg header, string format, byte[] data)
        {
            this.header = header;
            this.format = format;
            this.data = data;
        }

        public static ImgMsg Deserialize(MessageDeserializer deserializer) => new ImgMsg(deserializer);

        private ImgMsg(MessageDeserializer deserializer)
        {
            this.header = HeaderMsg.Deserialize(deserializer);
            deserializer.Read(out this.format);
            deserializer.Read(out this.data, sizeof(byte), deserializer.ReadLength());
        }

        public override void SerializeTo(MessageSerializer serializer)
        {
            serializer.Write(this.header);
            serializer.Write(this.format);
            serializer.WriteLength(this.data);
            serializer.Write(this.data);
        }

        public override string ToString()
        {
            return "ImgMsg: " +
            "\nheader: " + header.ToString() +
            "\nformat: " + format.ToString() +
            "\ndata: " + System.String.Join(", ", data.ToList());
        }

#if UNITY_EDITOR
        [UnityEditor.InitializeOnLoadMethod]
#else
        [UnityEngine.RuntimeInitializeOnLoadMethod]
#endif
        public static void Register()
        {
            MessageRegistry.Register(k_RosMessageName, Deserialize);
        }
    }
}

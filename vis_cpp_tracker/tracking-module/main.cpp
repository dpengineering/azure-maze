// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

//Modified for DPEA Azure Maze by Andrew Xie, Feb 2020

#include <assert.h>
#include <iostream>

#include <math.h>

#include <k4a/k4a.hpp>
#include <k4abt.hpp>

//TCP Socket stuff
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define PORT 7266

//3dv viewer
#include <map>
#include <vector>
#include <BodyTrackingHelpers.h>
#include <Utilities.h>
#include <Window3dWrapper.h>

// 3d window functions
bool s_isRunning = true;
Visualization::Layout3d s_layoutMode = Visualization::Layout3d::OnlyMainView;
bool s_visualizeJointFrame = false;

int64_t CloseCallback(void* /*context*/)
{
    s_isRunning = false;
    return 1;
}

int main()
{
    //Global vars for socket
    int server_fd, client, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};

    std::cout << "Azure Maze started!" << std::endl;
    std::cout << "Creating socket..." << std::endl;
    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("Socket creation failed!");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 7266
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
    {
        perror("Setsockopt failed!");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );

    // Forcefully attaching socket to the port 7266
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0)
    {
        perror("Socket bind failed!");
        exit(EXIT_FAILURE);
    }
    std::cout << "Socket bound to port " << PORT << "!" << std::endl;

    if (listen(server_fd, 3) < 0)
    {
        perror("Socket listen failed!");
        exit(EXIT_FAILURE);
    }

    std::cout << "Listening for client..."<< std::endl;

    if ((client = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))<0)
    {
        perror("Socket accept failed!");
        exit(EXIT_FAILURE);
    }
    std::cout << "Client connected! Starting Kinect..."<< std::endl;


    try
    {
        k4a_device_t device = nullptr;
        k4a_device_open(0, &device);

        // Start camera. Make sure depth camera is enabled.
        k4a_device_configuration_t deviceConfig = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
        deviceConfig.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
        deviceConfig.color_resolution = K4A_COLOR_RESOLUTION_OFF;
        k4a_device_start_cameras(device, &deviceConfig);

        // Get calibration information
        k4a_calibration_t sensorCalibration;
        k4a_device_get_calibration(device, deviceConfig.depth_mode, deviceConfig.color_resolution, &sensorCalibration);
        int depthWidth = sensorCalibration.depth_camera_calibration.resolution_width;
        int depthHeight = sensorCalibration.depth_camera_calibration.resolution_height;

        // Create Body Tracker
        k4abt_tracker_t tracker = nullptr;
        k4abt_tracker_configuration_t tracker_config = K4ABT_TRACKER_CONFIG_DEFAULT;
        tracker_config.processing_mode = K4ABT_TRACKER_PROCESSING_MODE_GPU;
        k4abt_tracker_create(&sensorCalibration, tracker_config, &tracker);
        // Initialize the 3d window controller
        Window3dWrapper window3d;
        window3d.Create("3D Visualization", sensorCalibration);
        window3d.SetCloseCallback(CloseCallback);

        int frame_count = 0;
        while(true)
        {
          k4a_capture_t sensorCapture = nullptr;
          k4a_wait_result_t getCaptureResult = k4a_device_get_capture(device, &sensorCapture, 0); // timeout_in_ms is set to 0

          if (getCaptureResult == K4A_WAIT_RESULT_SUCCEEDED)
          {
              // timeout_in_ms is set to 0. Return immediately no matter whether the sensorCapture is successfully added
              // to the queue or not.
              k4a_wait_result_t queueCaptureResult = k4abt_tracker_enqueue_capture(tracker, sensorCapture, 0);

              // Release the sensor capture once it is no longer needed.
              k4a_capture_release(sensorCapture);

              if (queueCaptureResult == K4A_WAIT_RESULT_FAILED)
              {
                  std::cout << "Error! Add capture to tracker process queue failed!" << std::endl;
                  break;
              }
          }
          else if (getCaptureResult != K4A_WAIT_RESULT_TIMEOUT)
          {
              std::cout << "Get depth capture returned error: " << getCaptureResult << std::endl;
              break;
          }

          // Pop Result from Body Tracker
          k4abt_frame_t bodyFrame = nullptr;
          k4a_wait_result_t popFrameResult = k4abt_tracker_pop_result(tracker, &bodyFrame, 0); // timeout_in_ms is set to 0
          if (popFrameResult == K4A_WAIT_RESULT_SUCCEEDED)
          {
            //3d display follows

              // Obtain original capture that generates the body tracking result
              k4a_capture_t originalCapture = k4abt_frame_get_capture(bodyFrame);
              k4a_image_t depthImage = k4a_capture_get_depth_image(originalCapture);

              std::vector<Color> pointCloudColors(depthWidth * depthHeight, { 1.f, 1.f, 1.f, 1.f });

              // Read body index map and assign colors
              k4a_image_t bodyIndexMap = k4abt_frame_get_body_index_map(bodyFrame);
              const uint8_t* bodyIndexMapBuffer = k4a_image_get_buffer(bodyIndexMap);
              for (int i = 0; i < depthWidth * depthHeight; i++)
              {
                  uint8_t bodyIndex = bodyIndexMapBuffer[i];
                  if (bodyIndex != K4ABT_BODY_INDEX_MAP_BACKGROUND)
                  {
                      uint32_t bodyId = k4abt_frame_get_body_id(bodyFrame, bodyIndex);
                      pointCloudColors[i] = g_bodyColors[bodyId % g_bodyColors.size()];
                  }
              }
              k4a_image_release(bodyIndexMap);

              // Visualize point cloud
              window3d.UpdatePointClouds(depthImage, pointCloudColors);

              // Visualize the skeleton data
              window3d.CleanJointsAndBones();
              uint32_t numBodies = k4abt_frame_get_num_bodies(bodyFrame);
              for (uint32_t i = 0; i < numBodies; i++)
              {
                  k4abt_body_t body;
                  k4abt_frame_get_body_skeleton(bodyFrame, i, &body.skeleton);
                  body.id = k4abt_frame_get_body_id(bodyFrame, i);

                  // Assign the correct color based on the body id
                  Color color = g_bodyColors[body.id % g_bodyColors.size()];
                  color.a = 0.4f;
                  Color lowConfidenceColor = color;
                  lowConfidenceColor.a = 0.1f;

                  // Visualize joints
                  for (int joint = 0; joint < static_cast<int>(K4ABT_JOINT_COUNT); joint++)
                  {
                      if (body.skeleton.joints[joint].confidence_level >= K4ABT_JOINT_CONFIDENCE_LOW)
                      {
                          const k4a_float3_t& jointPosition = body.skeleton.joints[joint].position;
                          const k4a_quaternion_t& jointOrientation = body.skeleton.joints[joint].orientation;

                          window3d.AddJoint(
                              jointPosition,
                              jointOrientation,
                              body.skeleton.joints[joint].confidence_level >= K4ABT_JOINT_CONFIDENCE_MEDIUM ? color : lowConfidenceColor);
                      }
                  }

                  // Visualize bones
                  for (size_t boneIdx = 0; boneIdx < g_boneList.size(); boneIdx++)
                  {
                      k4abt_joint_id_t joint1 = g_boneList[boneIdx].first;
                      k4abt_joint_id_t joint2 = g_boneList[boneIdx].second;

                      if (body.skeleton.joints[joint1].confidence_level >= K4ABT_JOINT_CONFIDENCE_LOW &&
                          body.skeleton.joints[joint2].confidence_level >= K4ABT_JOINT_CONFIDENCE_LOW)
                      {
                          bool confidentBone = body.skeleton.joints[joint1].confidence_level >= K4ABT_JOINT_CONFIDENCE_MEDIUM &&
                                               body.skeleton.joints[joint2].confidence_level >= K4ABT_JOINT_CONFIDENCE_MEDIUM;
                          const k4a_float3_t& joint1Position = body.skeleton.joints[joint1].position;
                          const k4a_float3_t& joint2Position = body.skeleton.joints[joint2].position;

                          window3d.AddBone(joint1Position, joint2Position, confidentBone ? color : lowConfidenceColor);
                      }
                  }
              }


              //tracking data
              std::cout << numBodies << " bodies are detected!" << std::endl;

              if (numBodies > 0) {
              uint32_t c = 0; //closest user
              for (uint32_t i = 0; i < numBodies; i++) // Find the closest user and remember ID
              {
                  k4abt_body_t body;
                  k4abt_frame_get_body_skeleton(bodyFrame, i, &body.skeleton);

                  k4abt_body_t cbody;
                  k4abt_frame_get_body_skeleton(bodyFrame, c, &cbody.skeleton);

                  k4a_float3_t position = body.skeleton.joints[2].position;
                  k4a_float3_t cposition = cbody.skeleton.joints[2].position;

                  if (position.v[2] < cposition.v[2])
                  {
                    c = i;
                  }
              }


              k4abt_body_t final_body;
              k4abt_frame_get_body_skeleton(bodyFrame, c, &final_body.skeleton);
              float rad = atan2 (final_body.skeleton.joints[8].position.v[1] - final_body.skeleton.joints[15].position.v[1], final_body.skeleton.joints[8].position.v[0] - final_body.skeleton.joints[15].position.v[0]);
              int degree = rad * 180 / 3.14; //Python can only recive ints

              send(client, &degree, sizeof(degree), 0); //Does not send properly, likely due to python reading the wrong size?


              k4a_capture_release(originalCapture);
              k4a_image_release(depthImage);
              k4abt_frame_release(bodyFrame);


          }

          window3d.SetLayout3d(s_layoutMode);
          window3d.SetJointFrameVisualization(s_visualizeJointFrame);
          window3d.Render();
        }
      }
    }
    catch (const std::exception& e)
    {
        std::cerr << "Failed with exception:" << std::endl
            << "    " << e.what() << std::endl;
        return 1;
    }

    close(server_fd);
    return 0;
}

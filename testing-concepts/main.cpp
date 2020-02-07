// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

//Modified for DPEA Kinetic Maze by Andrew Xie, Feb. 2020

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

//Angle Calculation via atan2
#include <math.h>

#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

//Azure Kinect libraries
#include <k4a/k4a.h>
#include <k4abt.h>

//3D Visualization
#include <BodyTrackingHelpers.h>
#include <Utilities.h>
#include <Window3dWrapper.h>

#include <array>
#include <iostream>
#include <map>
#include <vector>

#define VERIFY(result, error)                                                                            \
    if(result != K4A_RESULT_SUCCEEDED)                                                                   \
    {                                                                                                    \
        printf("%s \n - (File: %s, Function: %s, Line: %d)\n", error, __FILE__, __FUNCTION__, __LINE__); \
        exit(1);                                                                                         \
    }

//Global State of 3d viewer
bool s_isRunning = true;
Visualization::Layout3d s_layoutMode = Visualization::Layout3d::OnlyMainView;
bool s_visualizeJointFrame = false;                                                                    \
    if(result != K4A_RESULT_SUCCEEDED)                                                                   \
    {                                                                                                    \
        printf("%s \n - (File: %s, Function: %s, Line: %d)\n", error, __FILE__, __FUNCTION__, __LINE__); \
        exit(1);                                                                                         \
    }                                                                                                    \

//for debugging the location of joints.
void print_joint_information(int i, k4abt_body_t body)
{
  k4a_float3_t position = body.skeleton.joints[i].position;
  k4abt_joint_confidence_level_t confidence_level = body.skeleton.joints[i].confidence_level;
  printf("Joint[%d]: Position[mm] ( %f, %f, %f ); Confidence Level (%d) \n",
      i, position.v[0], position.v[1], position.v[2], confidence_level);
}

int main()
{
    //Kinect setup
    k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED; //FOV

    //Start camera, enable deptch camera
    k4a_device_t device;
    VERIFY(k4a_device_open(0, &device), "Open K4A Device failed!");
    VERIFY(k4a_device_start_cameras(device, &device_config), "Start K4A cameras failed!");

    //Calibrate
    k4a_calibration_t sensor_calibration;
    VERIFY(k4a_device_get_calibration(device, device_config.depth_mode, K4A_COLOR_RESOLUTION_OFF, &sensor_calibration),
        "Get depth camera calibration failed!");

    //Init body tracker
    k4abt_tracker_t tracker = NULL;
    k4abt_tracker_configuration_t tracker_config = K4ABT_TRACKER_CONFIG_DEFAULT;
    VERIFY(k4abt_tracker_create(&sensor_calibration, tracker_config, &tracker), "Body tracker initialization failed!");

    // Initialize the 3d window controller
    Window3dWrapper window3d;
    window3d.Create("3D Visualization", sensorCalibration);

    //Left from simple_3d
    //window3d.SetCloseCallback(CloseCallback);
    //window3d.SetKeyCallback(ProcessKey);

    //Loop control vars
    bool is_running = true;
    int frame_count = 0;

    //Control loop
    while(is_running)
    {
        k4a_capture_t sensor_capture;
        k4a_wait_result_t get_capture_result = k4a_device_get_capture(device, &sensor_capture, K4A_WAIT_INFINITE);
        if (get_capture_result == K4A_WAIT_RESULT_SUCCEEDED)
        {
            frame_count++;

            //printf("Start processing frame %d\n", frame_count);

            k4a_wait_result_t queue_capture_result = k4abt_tracker_enqueue_capture(tracker, sensor_capture, K4A_WAIT_INFINITE);

            k4a_capture_release(sensor_capture);
            if (queue_capture_result == K4A_WAIT_RESULT_TIMEOUT)
            {
                // It should never hit timeout when K4A_WAIT_INFINITE is set.
                printf("Error! Add capture to tracker process queue timeout!\n");
                break;
            }
            else if (queue_capture_result == K4A_WAIT_RESULT_FAILED)
            {
                printf("Error! Add capture to tracker process queue failed!\n");
                break;
            }

            k4abt_frame_t body_frame = NULL;
            k4a_wait_result_t pop_frame_result = k4abt_tracker_pop_result(tracker, &body_frame, K4A_WAIT_INFINITE);
            if (pop_frame_result == K4A_WAIT_RESULT_SUCCEEDED)
            {
                uint32_t num_bodies = k4abt_frame_get_num_bodies(body_frame);
                //printf("%u bodies are detected!\n", num_bodies);

                uint32_t c = 0; //closest user
                for (uint32_t i = 0; i < num_bodies; i++) // Find the closest user and remember ID
                {
                    k4abt_body_t body;
                    k4abt_body_t cbody;
                    VERIFY(k4abt_frame_get_body_skeleton(body_frame, i, &body.skeleton), "Get body from body frame failed!");
                    body.id = k4abt_frame_get_body_id(body_frame, i);

                    VERIFY(k4abt_frame_get_body_skeleton(body_frame, c, &body.skeleton), "Get stored body from body frame failed!");
                    cbody.id = k4abt_frame_get_body_id(body_frame, c);

                    if (body.skeleton.joints[2].position.v[2] < cbody.skeleton.joints[2].position.v[2])
                    {
                      c = i;
                    }
                }

                if (num_bodies >= 1)
                {
                  k4abt_body_t final_body; //track closest user's chest distance and hand angle.

                  VERIFY(k4abt_frame_get_body_skeleton(body_frame, c, &final_body.skeleton), "Get body from body frame failed!");
                  final_body.id = k4abt_frame_get_body_id(body_frame, c);

                  //Parse hand angle data
                  float radangle = atan2 (final_body.skeleton.joints[8].position.v[1] - final_body.skeleton.joints[15].position.v[1], final_body.skeleton.joints[8].position.v[0] - final_body.skeleton.joints[15].position.v[0]);
                  int angle = radangle * 180 / 3.14;
                  //printf("Chest distance: %i\n", (int) final_body.skeleton.joints[2].position.v[2]);
                  //printf("Angle: %i\n", angle);
                  printf("%i", angle);
                }
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
                    VERIFY(k4abt_frame_get_body_skeleton(bodyFrame, i, &body.skeleton), "Get skeleton from body frame failed!");
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

                k4a_capture_release(originalCapture);
                k4a_image_release(depthImage);
                k4abt_frame_release(body_frame);
                }

            else if (pop_frame_result == K4A_WAIT_RESULT_TIMEOUT)
            {
                //  It should never hit timeout when K4A_WAIT_INFINITE is set.
                printf("Error! Pop body frame result timeout!\n");
                break;
            }
          }
        else if (get_capture_result == K4A_WAIT_RESULT_TIMEOUT)
        {
            // It should never hit time out when K4A_WAIT_INFINITE is set.
            printf("Error! Get depth frame time out!\n");
            break;
        }
        else
        {
            printf("Get depth capture returned error: %d\n", get_capture_result);
            break;
        }

        //Render track
        window3d.SetLayout3d(s_layoutMode);
        window3d.SetJointFrameVisualization(s_visualizeJointFrame);
        window3d.Render();

    }

    printf("Finished body tracking processing!\n");

    window3d.Delete();
    k4abt_tracker_shutdown(tracker);
    k4abt_tracker_destroy(tracker);

    k4abt_tracker_shutdown(tracker);
    k4abt_tracker_destroy(tracker);
    k4a_device_stop_cameras(device);
    k4a_device_close(device);

    return 0;
}

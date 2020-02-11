// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

//Modified for DPEA Kinetic Maze by Andrew Xie, Feb. 2020

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <math.h>

#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

//Azure Libs (Kinect for Azure)
#include <k4a/k4a.h>
#include <k4abt.h>

//TCP Socket
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#define PORT 7266
#define SA struct sockaddr
#define VERIFY(result, error)                                                                            \
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
    //Start socket
    int sockfd, connfd, len;
    struct sockaddr_in servaddr, cli;

    // socket create and verification
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("[C] Socket creation failed!\n");
        exit(0);
    }
    else
        printf("[C] Socket successfully created!\n");
    bzero(&servaddr, sizeof(servaddr));

    // assign IP, PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);

    // Binding newly created socket to given IP and verification
    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) {
        printf("[C] Socket bind failed!\n");
        exit(0);
    }
    else
        printf("[C] Socket successfully bound!\n");

    // Now server is ready to listen and verification
    if ((listen(sockfd, 5)) != 0) {
        printf("[C] Listen failed!\n");
        exit(0);
    }
    else
        printf("[C] Server listening for verification!\n");
    len = sizeof(cli);

    // Accept the data packet from client and verification
    connfd = accept(sockfd, (SA*)&cli, &len);
    if (connfd < 0) {
        printf("[C] Verification failed!\n");
        exit(0);
    }
    else
        printf("[C] Client accepted! Starting Kinect...\n");

    //kinect setup
    k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;

    k4a_device_t device;
    VERIFY(k4a_device_open(0, &device), "[C] Open K4A Device failed!");
    VERIFY(k4a_device_start_cameras(device, &device_config), "[C] Start K4A cameras failed!");

    k4a_calibration_t sensor_calibration;
    VERIFY(k4a_device_get_calibration(device, device_config.depth_mode, K4A_COLOR_RESOLUTION_OFF, &sensor_calibration),
        "[C] Get depth camera calibration failed!");

    k4abt_tracker_t tracker = NULL;
    k4abt_tracker_configuration_t tracker_config = K4ABT_TRACKER_CONFIG_DEFAULT;
    VERIFY(k4abt_tracker_create(&sensor_calibration, tracker_config, &tracker), "[C] Body tracker initialization failed!");

    int frame_count = 0;
    while (true)
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
                printf("[C] Error! Add capture to tracker process queue timeout!\n");
                break;
            }
            else if (queue_capture_result == K4A_WAIT_RESULT_FAILED)
            {
                printf("[C] Error! Add capture to tracker process queue failed!\n");
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
                    VERIFY(k4abt_frame_get_body_skeleton(body_frame, i, &body.skeleton), "[C] Get body from body frame failed!");
                    body.id = k4abt_frame_get_body_id(body_frame, i);

                    VERIFY(k4abt_frame_get_body_skeleton(body_frame, c, &body.skeleton), "[C] Get stored body from body frame failed!");
                    cbody.id = k4abt_frame_get_body_id(body_frame, c);

                    if (body.skeleton.joints[2].position.v[2] < cbody.skeleton.joints[2].position.v[2])
                    {
                      c = i;
                    }
                }

                if (num_bodies >= 1)
                {
                  k4abt_body_t final_body; //track closest user's chest distance and hand angle.

                  VERIFY(k4abt_frame_get_body_skeleton(body_frame, c, &final_body.skeleton), "[C] Get body from body frame failed!");
                  final_body.id = k4abt_frame_get_body_id(body_frame, c);

                  float radangle = atan2 (final_body.skeleton.joints[8].position.v[1] - final_body.skeleton.joints[15].position.v[1], final_body.skeleton.joints[8].position.v[0] - final_body.skeleton.joints[15].position.v[0]);
                  int angle = radangle * 180 / 3.14;
                  //printf("Closest distance: %i\n", (int) final_body.skeleton.joints[2].position.v[2]);
                  printf("[C] Angle: %i\n", angle);

                  write(connfd, &angle, 4);




                } else {
                  printf("[C] No User Detected");
                  write(connfd, 0, 4);
                }

                k4abt_frame_release(body_frame);
                }

            else if (pop_frame_result == K4A_WAIT_RESULT_TIMEOUT)
            {
                //  It should never hit timeout when K4A_WAIT_INFINITE is set.
                printf("[C] Error! Pop body frame result timeout!\n");
                break;
            }
          }
        else if (get_capture_result == K4A_WAIT_RESULT_TIMEOUT)
        {
            // It should never hit time out when K4A_WAIT_INFINITE is set.
            printf("[C] Error! Get depth frame time out!\n");
            break;
        }
        else
        {
            printf("[C] Get depth capture returned error: %d\n", get_capture_result);
            break;
        }

    }

    printf("[C] Finished body tracking processing!\n");



    k4abt_tracker_shutdown(tracker);
    k4abt_tracker_destroy(tracker);
    k4a_device_stop_cameras(device);
    k4a_device_close(device);

    return 0;
}

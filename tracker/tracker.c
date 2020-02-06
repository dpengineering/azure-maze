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

#include <k4a/k4a.h>
#include <k4abt.h>

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
    //fifo setup
    int fd;
    char * fifo = "/tmp/fifo";
    // Creating the named file(FIFO)
    // mkfifo(<pathname>, <permission>)
    mkfifo(fifo, 0666);
    char arr[80];

    //kinect setup
    k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;

    k4a_device_t device;
    VERIFY(k4a_device_open(0, &device), "Open K4A Device failed!");
    VERIFY(k4a_device_start_cameras(device, &device_config), "Start K4A cameras failed!");

    k4a_calibration_t sensor_calibration;
    VERIFY(k4a_device_get_calibration(device, device_config.depth_mode, K4A_COLOR_RESOLUTION_OFF, &sensor_calibration),
        "Get depth camera calibration failed!");

    k4abt_tracker_t tracker = NULL;
    k4abt_tracker_configuration_t tracker_config = K4ABT_TRACKER_CONFIG_DEFAULT;
    VERIFY(k4abt_tracker_create(&sensor_calibration, tracker_config, &tracker), "Body tracker initialization failed!");

    int frame_count = 0;
    do
    {
        k4a_capture_t sensor_capture;
        k4a_wait_result_t get_capture_result = k4a_device_get_capture(device, &sensor_capture, K4A_WAIT_INFINITE);
        if (get_capture_result == K4A_WAIT_RESULT_SUCCEEDED)
        {
            frame_count++;

            printf("Start processing frame %d\n", frame_count);

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
                printf("%u bodies are detected!\n", num_bodies);

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

                  float radangle = atan2 (final_body.skeleton.joints[8].position.v[1] - final_body.skeleton.joints[15].position.v[1], final_body.skeleton.joints[8].position.v[0] - final_body.skeleton.joints[15].position.v[0]);
                  int angle = radangle * 180 / 3.14;
                  printf("Chest distance: %i\n", (int) final_body.skeleton.joints[2].position.v[2]);
                  printf("Angle: %i\n", angle);


                  // Open joint FIFO for write only
                  fd = open(fifo, O_WRONLY | O_NONBLOCK);

                  // Write the input on FIFO
                  // and close it
                  snprintf(arr,sizeof(arr),"%i",angle);
                  write(fd, arr, strlen(arr)+1);
                  close(fd);

                  k4abt_frame_release(body_frame);
                }


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

    } while (true);

    printf("Finished body tracking processing!\n");

    k4abt_tracker_shutdown(tracker);
    k4abt_tracker_destroy(tracker);
    k4a_device_stop_cameras(device);
    k4a_device_close(device);

    return 0;
}

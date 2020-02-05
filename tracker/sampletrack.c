// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <k4a/k4a.h>
#include <k4abt.h>

#define VERIFY(result, error)                                                                            \
    if(result != K4A_RESULT_SUCCEEDED)                                                                   \
    {                                                                                                    \
        printf("%s \n - (File: %s, Function: %s, Line: %d)\n", error, __FILE__, __FUNCTION__, __LINE__); \
        exit(1);                                                                                         \
    }                                                                                                    \

void print_joint_information(int i, k4abt_body_t body)
{
  k4a_float3_t position = body.skeleton.joints[i].position;
  k4abt_joint_confidence_level_t confidence_level = body.skeleton.joints[i].confidence_level;
  printf("Joint[%d]: Position[mm] ( %f, %f, %f ); Confidence Level (%d) \n",
      i, position.v[0], position.v[1], position.v[2], confidence_level);
}

void print_body_index_map_middle_line(k4a_image_t body_index_map)
{
    uint8_t* body_index_map_buffer = k4a_image_get_buffer(body_index_map);

    // Given body_index_map pixel type should be uint8, the stride_byte should be the same as width
    // TODO: Since there is no API to query the byte-per-pixel information, we have to compare the width and stride to
    // know the information. We should replace this assert with proper byte-per-pixel query once the API is provided by
    // K4A SDK.
    assert(k4a_image_get_stride_bytes(body_index_map) == k4a_image_get_width_pixels(body_index_map));

    int middle_line_num = k4a_image_get_height_pixels(body_index_map) / 2;
    body_index_map_buffer = body_index_map_buffer + middle_line_num * k4a_image_get_width_pixels(body_index_map);

    printf("BodyIndexMap at Line %d:\n", middle_line_num);
    for (int i = 0; i < k4a_image_get_width_pixels(body_index_map); i++)
    {
        printf("%u, ", *body_index_map_buffer);
        body_index_map_buffer++;
    }
    printf("\n");
}

int main()
{
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
                printf("%u bodies are detected!\n", num_bodies);

                k4abt_body_t body;
                if (num_bodies >= 1){
                  VERIFY(k4abt_frame_get_body_skeleton(body_frame, 0, &body.skeleton), "Get body from body frame failed!");
                  body.id = k4abt_frame_get_body_id(body_frame, 0);
                  //PROCESSING GOES HERE
                  //printf("Body ID: %u\n", body.id);
                  //LEFT HAND: 8 RIGHT HAND: 15 LEFT ELBOW: 6 RIGHT ELBOW: 13

                  //LEFT SIDE: tested and mostly works
                  //if (body.skeleton.joints[8].position.v[0] < body.skeleton.joints[6].position.v[0]){
                  //  printf("LH abv LE!\n");
                  //}
                  //else {
                  //  printf("Nope");
                  //}

                  //RIGHT HAND
                  //if (body.skeleton.joints[15].position.v[0] < body.skeleton.joints[13].position.v[0]){
                  //  printf("RH abv RE!\n");
                  //}
                  //else {
                  //  printf("Nope");
                  //}

                  //Both sides
                  if (body.skeleton.joints[8].position.v[0] < body.skeleton.joints[6].position.v[0] && body.skeleton.joints[15].position.v[0] < body.skeleton.joints[13].position.v[0]){
                    printf("Joint[%d]: Position[mm] ( %f, %f, %f )\n",
                        8, body.skeleton.joints[8].position.v[0], body.skeleton.joints[8].position.v[1], body.skeleton.joints[8].position.v[2]);
                    printf("Joint[%d]: Position[mm] ( %f, %f, %f )\n",
                        15, body.skeleton.joints[15].position.v[0], body.skeleton.joints[15].position.v[1], body.skeleton.joints[15].position.v[2]);
                  }
                  else {
                    printf("Nope");
                  }

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

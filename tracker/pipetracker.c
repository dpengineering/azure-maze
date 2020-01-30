#include <stdio.h>
#include <stdlib.h>

#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include <k4a/k4a.h>
#include <k4abt.h>

#define VERIFY(result, error)                                                                        \
if(result != K4A_RESULT_SUCCEEDED)                                                                   \
{                                                                                                    \
  printf("%s \n - (File: %s, Function: %s, Line: %d)\n", error, __FILE__, __FUNCTION__, __LINE__);   \
  exit(1);                                                                                           \
}


int main()
{
  int fd;
  int fd1;

  // FIFO file path
  char * jointfifo = "/tmp/jointfifo";
  char * imgfifo = "/tmp/imgfifo" //Not implemented yet

  // Creating the named file(FIFO)
  // mkfifo(<pathname>, <permission>)
  mkfifo(jointfifo, 0666);

  char arr1[80], arr2[80];
  while (1)
  {
    // Get body tracking data!
    k4a_device_t device = NULL;
    VERIFY(k4a_device_open(0, &device), "Open K4A Device failed!");

    // Start camera. Make sure depth camera is enabled.
    k4a_device_configuration_t deviceConfig = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    deviceConfig.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
    deviceConfig.color_resolution = K4A_COLOR_RESOLUTION_OFF;
    VERIFY(k4a_device_start_cameras(device, &deviceConfig), "Start K4A cameras failed!");

    k4a_calibration_t sensor_calibration;
    VERIFY(k4a_device_get_calibration(device, deviceConfig.depth_mode, deviceConfig.color_resolution, &sensor_calibration),
    "Get depth camera calibration failed!");

    k4abt_tracker_t tracker = NULL;
    k4abt_tracker_configuration_t tracker_config = K4ABT_TRACKER_CONFIG_DEFAULT;
    VERIFY(k4abt_tracker_create(&sensor_calibration, tracker_config, &tracker), "Body tracker initialization failed!");


    k4a_capture_t sensor_capture;
    k4a_wait_result_t get_capture_result = k4a_device_get_capture(device, &sensor_capture, K4A_WAIT_INFINITE);
    if (get_capture_result == K4A_WAIT_RESULT_SUCCEEDED)
    {
      frame_count++;
      k4a_wait_result_t queue_capture_result = k4abt_tracker_enqueue_capture(tracker, sensor_capture, K4A_WAIT_INFINITE);
      k4a_capture_release(sensor_capture); // Remember to release the sensor capture once you finish using it
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
        // Successfully popped the body tracking result. Start your processing

        size_t num_bodies = k4abt_frame_get_num_bodies(body_frame);
        printf("%zu bodies are detected!\n", num_bodies);

        //Get joint info for first body, ADD CHECK FOR FIRST NONEMPTY BODY IF NUMBERS DO NOT REASSIGN

        k4abt_skeleton_t skeleton;
        k4abt_frame_get_body_skeleton(body_frame, 0, &skeleton);
        uint32_t id = k4abt_frame_get_body_id(body_frame, i);


        //Calculate hand angle of body 1

        k4abt_frame_release(body_frame); // Remember to release the body frame once you finish using it
      }
      else if (pop_frame_result == K4A_WAIT_RESULT_TIMEOUT)
      {
        //  It should never hit timeout when K4A_WAIT_INFINITE is set.
        printf("Error! Pop body frame result timeout!\n");
        break;
      }
      else
      {
        printf("Pop body frame result failed!\n");
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


    printf("Got requested frame!\n");

    k4abt_tracker_shutdown(tracker);
    k4abt_tracker_destroy(tracker);


    // Open joint FIFO for write only - sent joint data (Parse into angle)
    fd = open(jointfifo, O_WRONLY);

    // Write the input on FIFO
    // and close it
    write(fd, arr2, strlen(arr2)+1);
    close(fd);


  }
  return 0;
}

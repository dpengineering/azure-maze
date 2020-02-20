// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

//Modified for DPEA Azure Maze by Andrew Xie, Feb 2020

#include <assert.h>
#include <iostream>

#include <math.h>

#include <k4a/k4a.hpp>
#include <k4abt.hpp>

int main()
{
    try
    {
        k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
        device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;

        k4a::device device = k4a::device::open(0);
        device.start_cameras(&device_config);

        k4a::calibration sensor_calibration = device.get_calibration(device_config.depth_mode, device_config.color_resolution);

        k4abt::tracker tracker = k4abt::tracker::create(sensor_calibration);

        int frame_count = 0;
        while(true)
        {
            k4a::capture sensor_capture;
            if (device.get_capture(&sensor_capture, std::chrono::milliseconds(K4A_WAIT_INFINITE)))
            {
                frame_count++;

                std::cout << "Start processing frame " << frame_count << std::endl;

                if (!tracker.enqueue_capture(sensor_capture))
                {
                    // It should never hit timeout when K4A_WAIT_INFINITE is set.
                    std::cout << "Error! Add capture to tracker process queue timeout!" << std::endl;
                    break;
                }

                k4abt::frame body_frame = tracker.pop_result();
                if (body_frame != nullptr)
                {
                    uint32_t num_bodies = body_frame.get_num_bodies();
                    std::cout << num_bodies << " bodies are detected!" << std::endl;

                    if (num_bodies > 0) {
                    uint32_t c = 0; //closest user
                    for (uint32_t i = 0; i < num_bodies; i++) // Find the closest user and remember ID
                    {
                        k4abt_body_t body = body_frame.get_body(i);
                        k4abt_body_t cbody = body_frame.get_body(c);

                        k4a_float3_t position = body.skeleton.joints[2].position;
                        k4a_float3_t cposition = cbody.skeleton.joints[2].position;

                        if (position.v[2] < cposition.v[2])
                        {
                          c = i;
                        }
                    }


                    k4abt_body_t final_body = body_frame.get_body(c);
                    std::cout << atan2 (final_body.skeleton.joints[8].position.v[1] - final_body.skeleton.joints[15].position.v[1], final_body.skeleton.joints[8].position.v[0] - final_body.skeleton.joints[15].position.v[0]) << std::endl;
                  }
                }
                else
                {
                    //  It should never hit timeout when K4A_WAIT_INFINITE is set.
                    std::cout << "Error! Pop body frame result time out!" << std::endl;
                    break;
                }
            }
            else
            {
                // It should never hit time out when K4A_WAIT_INFINITE is set.
                std::cout << "Error! Get depth frame time out!" << std::endl;
                break;
            }
        }

        std::cout << "Finished body tracking processing!" << std::endl;

    }
    catch (const std::exception& e)
    {
        std::cerr << "Failed with exception:" << std::endl
            << "    " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

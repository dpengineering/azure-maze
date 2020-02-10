import time
import math
import odrive
import contextlib
import odrive.enums
from configs.config import global_config as c

ANGLE_NORMALIZATION = 1 / math.pi

class KineticMazeMotor:
    def __init__(self):
        self.od = None
        self.approx_cycles_per_revolution = None

        self.init_odrive()

    def axis(self):
        return getattr(self.od, "axis%d" % (c.physics.MOTOR_AXIS,))

    @contextlib.contextmanager
    def axis_context(self, control_mode=None, pos_gain=None, vel_gain=None,
                     trajectory_mv=None, trajectory_ma=None, trajectory_md=None):
        old_control_mode = self.axis().controller.config.control_mode
        old_pos_gain = self.axis().controller.config.pos_gain
        old_vel_gain = self.axis().controller.config.vel_gain

        old_traj_mv = self.axis().trap_traj.config.vel_limit
        old_traj_ma = self.axis().trap_traj.config.accel_limit
        old_traj_md = self.axis().trap_traj.config.decel_limit

        try:
            if control_mode is not None:
                self.axis().controller.config.control_mode = control_mode
            if pos_gain is not None:
                self.axis().controller.config.pos_gain = pos_gain
            if vel_gain is not None:
                self.axis().controller.config.vel_gain = vel_gain

            if trajectory_mv is not None:
                self.axis().trap_traj.config.vel_limit = trajectory_mv
            if trajectory_ma is not None:
                self.axis().trap_traj.config.accel_limit = trajectory_ma
            if trajectory_md is not None:
                self.axis().trap_traj.config.decel_limit = trajectory_md

            yield self.axis()
        finally:
            self.axis().controller.config.control_mode = old_control_mode
            self.axis().controller.config.pos_gain = old_pos_gain
            self.axis().controller.config.vel_gain = old_vel_gain

            self.axis().trap_traj.config.vel_limit = old_traj_mv
            self.axis().trap_traj.config.accel_limit = old_traj_ma
            self.axis().trap_traj.config.decel_limit = old_traj_md

    def report_odrive_error(self):
        print("ODrive Error!")

    def set_velocity(self, vel, wait=False):
        if abs(vel) < c.physics.VELOCITY_MIN_CUTOFF:
            corrected = 0
        elif abs(vel) > c.physics.VELOCITY_MAX_CUTOFF:
            raise ValueError("Velocity too large!")
        else:
            corrected = vel
        try:
            self.axis().controller.vel_setpoint = corrected
        except:
            self.report_odrive_error()
            raise

        if wait:
            while abs(self.axis().encoder.vel_estimate - corrected) > \
                  c.physics.VEL_CONTROL_VELOCITY_TOLERANCE:
                pass

    def adjust_angle(self, angle):
        norm = max(min(angle * ANGLE_NORMALIZATION, 1.0), -1.0)
        adjusted = abs((abs(norm) ** c.physics.ANGLE_EXPONENT) * \
                       c.physics.ADJUSTED_ANGLE_MULTIPLIER)
        clamped = min(adjusted, c.physics.VELOCITY_MAX_CUTOFF)
        return math.copysign(clamped, norm) * (-1 if c.physics.FLIP_VELOCITY else 1)

    def ramp_down(self):
        try:
            return self.axis().controller.vel_setpoint * c.physics.RAMP_DOWN_FACTOR
        except:
            self.report_odrive_error()
            raise

    def init_odrive(self):
        print("Finding ODrive")
        self.od = odrive.find_any()

        print("Calibrating ODrive")
        self.axis().motor.config.current_lim = c.physics.MOTOR_CURRENT_LIMIT
        self.axis().motor.config.calibration_current = c.physics.MOTOR_CALIBRATION_CURRENT

        self.axis().requested_state = odrive.enums.AXIS_STATE_MOTOR_CALIBRATION
        while self.axis().current_state != odrive.enums.AXIS_STATE_IDLE:
            pass

        # Wait for any oscillation to dissipate
        print("Waiting for oscillation to dissipate")
        time.sleep(c.physics.CALIBRATION_DELAY_TIME)

        self.axis().requested_state = odrive.enums.AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        while self.axis().current_state != odrive.enums.AXIS_STATE_IDLE:
            pass

        self.axis().cycle_trigger.config.gpio_pin_num = c.physics.CYCLE_TRIGGER_GPIO_PIN
        self.axis().cycle_trigger.config.enabled = True

        self.axis().encoder.config.bandwidth = c.physics.ENCODER_BANDWIDTH
        self.axis().controller.config.vel_gain = c.physics.CONTROLLER_VEL_GAIN

        self.axis().trap_traj.config.vel_limit = c.physics.TRAJECTORY_VEL_LIMIT
        self.axis().trap_traj.config.accel_limit = c.physics.TRAJECTORY_ACCEL_LIMIT
        self.axis().trap_traj.config.decel_limit = c.physics.TRAJECTORY_DECEL_LIMIT
        self.axis().trap_traj.config.A_per_css = c.physics.TRAJECTORY_AMPS_PER_ACCELERATION

        self.axis().requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
        self.axis().controller.config.control_mode = odrive.enums.CTRL_MODE_VELOCITY_CONTROL

        self.home()

        print("ODrive initialization complete")

    def home(self):
        print("Homing . . .")
        with self.axis_context(control_mode=odrive.enums.CTRL_MODE_VELOCITY_CONTROL):
            print("Finding first edge")
            self.axis().cycle_trigger.last_edge_hit.has_hit = False
            self.set_velocity(c.physics.HOMING_VELOCITY)
            while not self.axis().cycle_trigger.last_edge_hit.has_hit:
                pass

            first_edge = self.axis().cycle_trigger.last_edge_hit.hit_location
            print("Found first edge at %d", first_edge)

            print("Finding second edge")
            self.axis().cycle_trigger.last_edge_hit.has_hit = False
            while not self.axis().cycle_trigger.last_edge_hit.has_hit:
                pass

            second_edge = self.axis().cycle_trigger.last_edge_hit.hit_location
            delta = second_edge - first_edge
            print("Found second edge at %d (offset %d)", second_edge, delta)

            self.approx_cycles_per_revolution = abs(delta)

            self.set_velocity(0, wait=True)

            self.go_to_angle(0)

            self.set_velocity(0, wait=True)

        print("Homing complete")

    def get_home(self):
        if not self.axis().cycle_trigger.last_edge_hit.has_hit:
            raise ValueError("has_hit was False; ensure home() has been called at least once")
        return self.axis().cycle_trigger.last_edge_hit.hit_location + \
            ((c.physics.HOME_OFFSET_ANGLE / (2 * math.pi)) * self.approx_cycles_per_revolution)

    def get_adjusted_home(self):
        # Ensure that home is always below us
        raw_home = self.get_home()
        if self.axis().encoder.pos_estimate < raw_home:
            return raw_home - self.approx_cycles_per_revolution
        else:
            return raw_home

    def get_counts_per_radian(self):
        return self.approx_cycles_per_revolution / (2 * math.pi)

    def calculate_relative_position(self, pos):
        return (pos - self.get_home()) % self.approx_cycles_per_revolution

    def go_to_angle(self, angle, direction=None,
                    max_velocity=None, max_accel=None, max_decel=None):
        print("Going to angle %f", angle)
        if direction is not None and direction != 1 and direction != -1:
            raise ValueError("Invalid direction")

        home = self.get_adjusted_home()
        current = self.calculate_relative_position(self.axis().encoder.pos_estimate)
        base_offset = (angle * self.get_counts_per_radian())
        if current < base_offset:
            pos_offset = base_offset
            neg_offset = base_offset - self.approx_cycles_per_revolution
        else:
            pos_offset = base_offset + self.approx_cycles_per_revolution
            neg_offset = base_offset

        if direction == 1:
            offset = pos_offset
        elif direction == -1:
            offset = neg_offset
        else:
            # Find the closest
            if abs(pos_offset - current) < abs(neg_offset - current):
                offset = pos_offset
            else:
                offset = neg_offset
        target = home + offset

        mv = max_velocity if max_velocity is not None else c.physics.TRAJECTORY_VEL_LIMIT
        ma = max_accel if max_accel is not None else c.physics.TRAJECTORY_ACCEL_LIMIT
        md = max_decel if max_decel is not None else c.physics.TRAJECTORY_DECEL_LIMIT
        with self.axis_context(control_mode=odrive.enums.CTRL_MODE_POSITION_CONTROL,
                               trajectory_mv=mv, trajectory_ma=ma, trajectory_md=md):
            print("Seeking to %d (currently at %f)", target, self.axis().encoder.pos_estimate)

            # ODrive begins calculating based on the current pos_setpoint and vel_setpoint
            # We want it to be relative to the current pos/vel, so use this workaround
            self.axis().controller.pos_setpoint = self.axis().encoder.pos_estimate
            self.axis().controller.vel_setpoint = self.axis().encoder.vel_estimate
            self.axis().controller.move_to_pos(target)

            while self.axis().controller.config.control_mode != \
                  odrive.enums.CTRL_MODE_POSITION_CONTROL:
                pass

            print("Trapezoidal planning finished")

            pos_tolerance = c.physics.POS_CONTROL_OFFSET_TOLERANCE
            velocity_tolerance = c.physics.POS_CONTROL_VELOCITY_TOLERANCE
            tick_count = 0
            while tick_count < c.physics.POS_CONTROL_TICK_COUNT:
                while True:
                    if abs(self.axis().encoder.pos_estimate - target) < pos_tolerance and \
                       abs(self.axis().encoder.vel_estimate) < velocity_tolerance:
                        break
                    tick_count = 0
                tick_count += 1

        print("Go-to-angle complete")

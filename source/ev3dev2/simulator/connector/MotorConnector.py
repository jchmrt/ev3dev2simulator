from ev3dev2.simulator.connector.MotorCommandCreator import get_motor_command_creator

FOREVER_MOCK_SECONDS = 45


class MotorConnector:
    """
    The MotorConnector class provides a translation layer between the ev3dev2 motor classes
    and the motors on the simulated robot. This includes motor positioning and speed/distance data.
    This class is responsible for calling the MotorCommandCreator to create movement commands for
    the simulator.
    """


    def __init__(self, address: str):
        self.address = address

        self.duty_cycle = None
        self.speed = None
        self.distance = None
        self.time = None
        self.stop_action = None

        self.command_creator = get_motor_command_creator()


    def set_duty_cycle(self, duty_cycle: int):
        """
        Set the percentage of power of the motor belonging to the given address.
        -100 being fully backwards and 100 fully forwards.
        :param duty_cycle: in percentage.
        """

        self.duty_cycle = duty_cycle


    def set_speed(self, speed: float):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param speed: in degrees per second.
        """

        self.speed = speed


    def set_distance(self, distance: float):
        """
        Set the distance to run of the motor belonging to the given address.
        :param distance: in degrees.
        """

        self.distance = distance


    def set_time(self, time: int):
        """
        Set the time to run of the motor belonging to the given address.
        :param time: in milliseconds.
        """

        self.time = time


    def set_stop_action(self, action: str):
        """
        Set the speed to run at of the motor belonging to the given address.
        :param action: stop action of the motor, this can be 'hold' or 'coast'.
        """

        self.stop_action = action


    def run_forever(self) -> float:
        """
        Run the motor indefinitely. This is translated to 45 seconds.
        :return a floating point value representing the number of seconds
        the given run operation will take. Here a large number is returned.
        In the real world this would be infinity.
        """

        self.distance = self.speed * FOREVER_MOCK_SECONDS
        return self._run()


    def run_to_rel_pos(self) -> float:
        """
        Run the motor for the distance needed to reach a certain position.
        :return a floating point value representing the number of seconds
        the given run operation will take.
        """

        return self._run()


    def run_timed(self) -> float:
        """
        Run the motor for a number of milliseconds.
        :return a floating point value representing the number of seconds
        the given run operation will take.
        """

        self.distance = self.speed * (self.time / 1000)
        return self._run()


    def run_direct(self) -> float:
        """
        Run the motor for at the given speed provided by the duty_cycle.
        :return a floating point value representing the number of seconds
        the given run operation will take.
        """

        self.speed = self.duty_cycle / 100 * 1050
        self.distance = self.speed * FOREVER_MOCK_SECONDS

        return self._run()


    def _run(self) -> float:
        """
        Run the motor at a speed for a distance.
        :return a floating point value representing the number of seconds
        the given run operation will take.
        """

        if self.speed == 0 or self.distance == 0:
            return 0

        return self.command_creator.create_drive_command(self.speed,
                                                         self.distance,
                                                         self.stop_action,
                                                         self.address)


    def stop(self) -> float:
        """
        Stop the motor using the provided stop action.
        :return: a floating point value representing the number of seconds the
        stop operation will take.
        """

        speed = self.speed if self.speed else 0
        stop_action = self.stop_action if self.stop_action else 0
        distance = self.distance if self.distance else 0

        if speed == 0:
            return 0

        if distance < 0:
            speed *= -1

        return self.command_creator.create_stop_command(speed, stop_action, self.address)

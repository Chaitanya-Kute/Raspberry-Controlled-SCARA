# Robot Controller GUI

This Python GUI application allows you to control a robot with 5-axis movement using serial communication. The GUI includes sliders for each axis, a home button for homing the robot, and features to save, send, and play checkpoints.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Tkinter (Python's standard GUI package)
- PySerial (for serial communication)

## Installation

1. Clone the repository to your local machine:

   https://github.com/Chaitanya-Kute/Raspberry-Controlled-SCARA.git

3. Change into the project directory:

    ```
    cd robot-controller-gui
    ```

4. Install the required dependencies:

    ```
    pip install tkinter
    pip install pyserial

    ```

## Usage

1. Run the GUI application:

    ```bash
    python robot_controller_gui.py
    ```

2. The GUI will appear with sliders for each axis, a home button, and options to save, send, and play checkpoints.

3. Select the COM port from the dropdown menu.

4. Enter the values for each axis manually or use the sliders.

5. Click the "Save" button to save the current position as a checkpoint.

6. Click the "Send" button to send the values to the robot using serial communication.

7. Click the "Play" button to play the saved checkpoints sequentially.

8. Use the "Export" and "Import" buttons to save and load checkpoints to and from a CSV file.

9. The "Clear Last" button removes the last saved checkpoint, and the "Stop" button performs an emergency stop.

10. The number of checkpoints is displayed at the bottom of the GUI.

## Note

- Make sure your robot understands the CSV format (e.g., "100,0,100,100,90") for movement.

- Adjust the baudrate in the code (`serial_baudrate`) to match your robot's communication settings.

- Ensure that the correct COM port is selected from the dropdown menu.

Enjoy controlling your robot with the GUI!


By Chaitanya Kute (chaitanya_kute@outlook.com)


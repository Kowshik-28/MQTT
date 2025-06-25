# ESP32 MQTT Publisher with Python Tkinter Subscriber

This project demonstrates a real-time data communication system using MQTT (Message Queuing Telemetry Transport) protocol. An ESP32 microcontroller acts as a publisher, sending data to an MQTT broker, while a Python application with a Tkinter GUI acts as a subscriber, receiving and displaying the messages in real-time.

## 🌟 Features

* **ESP32 Publisher:** Connects to Wi-Fi, establishes an MQTT connection, and periodically publishes incremental data to a specified topic.
* **Python Tkinter Subscriber:** Connects to the same MQTT broker, subscribes to the topic, and displays incoming messages in a user-friendly graphical interface with timestamps.
* **Thread-Safe GUI Updates:** Utilizes threading and a message queue to ensure smooth and responsive GUI updates without blocking the main Tkinter loop.
* **Modular Design:** Separates MQTT logic from GUI logic for better organization and maintainability.

## 🛠️ Technologies Used

* **Hardware:**
    * ESP32 Development Board (e.g., ESP32 DevKitC, NodeMCU ESP32)
* **Software/Libraries:**
    * **Arduino IDE:** For programming the ESP32.
    * **ArduinoMqttClient Library:** MQTT client for ESP32.
    * **`paho-mqtt`:** MQTT client library for Python.
    * **`tkinter`:** Python's standard GUI library.
    * **`threading` & `queue`:** Python modules for concurrent programming.
    * **`broker.emqx.io`:** A public MQTT broker used for communication (can be replaced with any other broker).

## 🚀 How it Works

1.  **ESP32 (Publisher):**
    * Connects to a specified Wi-Fi network.
    * Connects to the `broker.emqx.io` MQTT broker on port `1883`.
    * Every 8 seconds, it increments an integer value (`valueToSend`).
    * It then converts this integer to a string and publishes it to the MQTT topic `"rj1"`.
    * Serial output on the ESP32 shows connection status and published messages.

2.  **Python (Subscriber):**
    * Initializes a Tkinter GUI window.
    * Creates a tabbed interface (using `ttk.Notebook`), with a dedicated `ScrolledText` widget for each subscribed topic (currently `"rj1"`).
    * Starts an MQTT client in a separate thread to handle connections and message reception without freezing the GUI.
    * Subscribes to the `"rj1"` topic upon successful connection to the broker.
    * When a message is received, it's decoded, timestamped, and placed into a `message_queue`.
    * A periodic `check_queue` function in the main Tkinter thread retrieves messages from the queue and safely updates the corresponding `ScrolledText` widget in the GUI.

## ⚡ Setup and Usage

### 1. ESP32 Publisher Setup

1.  **Install Arduino IDE:** Download and install the Arduino IDE if you haven't already.
2.  **Install ESP32 Board Support:**
    * Go to `File > Preferences`.
    * In "Additional Boards Manager URLs", add: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
    * Go to `Tools > Board > Boards Manager...`, search for "esp32", and install the `esp32` by Espressif.
3.  **Install ArduinoMqttClient Library:**
    * Go to `Sketch > Include Library > Manage Libraries...`
    * Search for "ArduinoMqttClient" and install it.
4.  **Modify the ESP32 Code:**
    * Open the `arduino UNO code of esp32` provided in the repository.
    * **Crucially, update your Wi-Fi credentials:**
        ```cpp
        const char* ssid = "YOUR_WIFI_SSID";         // Replace with your WiFi SSID
        const char* password = "YOUR_WIFI_PASSWORD"; // Replace with your WiFi Password
        ```
    * (Optional) You can change the `topic` name (`"rj1"`) or `broker` address if needed.
5.  **Upload to ESP32:**
    * Select your ESP32 board (`Tools > Board > ESP32 Arduino > ...`) and the correct COM Port.
    * Upload the code to your ESP32.
    * Open the Serial Monitor (at 115200 baud) to see the connection status and published messages.

### 2. Python Tkinter Subscriber Setup

1.  **Install Python:** Ensure you have Python 3.x installed on your system.
2.  **Install `paho-mqtt`:**
    ```bash
    pip install paho-mqtt
    ```
3.  **Run the Python Code:**
    * Save the `python code` provided in the repository as a `.py` file (e.g., `mqtt_subscriber_gui.py`).
    * Open a terminal or command prompt, navigate to the directory where you saved the file, and run:
    ```bash
    python mqtt_subscriber_gui.py
    ```
    * A Tkinter window will appear, displaying messages received on the `"rj1"` topic.

## 🤝 Contribution

Feel free to fork this repository, open issues, or submit pull requests for any improvements or bug fixes.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

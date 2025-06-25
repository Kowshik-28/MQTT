import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk  # Import ttk for Notebook widget
import paho.mqtt.client as mqtt
import threading
import queue
import time

# --- MQTT Configuration ---
MQTT_BROKER_ADDRESS = "broker.emqx.io" # <--- MAKE SURE THIS MATCHES YOUR PUBLISHER
MQTT_BROKER_PORT = 1883
MQTT_CLIENT_ID = "TkinterSubscriber"
MQTT_TOPICS = [
    # "bms/data/PT_A",
    # "bms/data/PT_B",
    # "bms/data/PT_C",
    "rj1"
    # "bms/data/Cell_Voltages", # Example: Add more topics if you expand your BMS data
    # "bms/data/Temperatures"   # Example: Another potential topic
]

# --- Global Queue for messages ---
# This queue will now store (formatted_message, topic) tuples
message_queue = queue.Queue()

# --- MQTT Callbacks ---

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback function when the MQTT client connects to the broker."""
    if rc == 0:
        print("Connected to MQTT Broker!")
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
        # Optionally subscribe to a wildcard for any other topics not explicitly listed
        # client.subscribe("bms/data/#")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """Callback function when a message is received from the broker."""
    topic = msg.topic
    payload = msg.payload.decode()
    message_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    formatted_message = f"[{message_time}] Payload: {payload}\n" # No need to repeat topic here
    print(f"Topic: {topic}\n{formatted_message.strip()}") # Print to console
    message_queue.put((formatted_message, topic)) # Put message and its topic into the queue

# --- Tkinter Application ---

class MqttSubscriberApp:
    def __init__(self, master):
        self.master = master
        master.title("MQTT BMS Data Viewer")
        master.geometry("1000x700") # Increased window size for tabs

        # Create a Notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Dictionary to hold references to ScrolledText widgets for each topic
        self.topic_displays = {}

        # Create a tab and ScrolledText for each topic
        for topic in MQTT_TOPICS:
            tab_frame = ttk.Frame(self.notebook) # Create a frame for the tab
            self.notebook.add(tab_frame, text=topic.replace("bms/data/", "")) # Add tab with simplified name

            # Create ScrolledText widget inside the tab's frame
            text_widget = scrolledtext.ScrolledText(tab_frame, wrap=tk.WORD, width=100, height=30, font=("Consolas", 10))
            text_widget.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
            text_widget.config(state=tk.DISABLED) # Make it read-only

            self.topic_displays[topic] = text_widget # Store reference to the widget

        # Initialize MQTT client
        self.client = mqtt.Client(
            client_id=MQTT_CLIENT_ID,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        # Start MQTT client in a separate thread
        self.mqtt_thread = threading.Thread(target=self._start_mqtt_client)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()

        # Schedule the check_queue method to run periodically
        self.master.after(100, self.check_queue)

    def _start_mqtt_client(self):
        """Method to run the MQTT client connection loop."""
        try:
            print(f"Attempting to connect to MQTT broker: {MQTT_BROKER_ADDRESS}:{MQTT_BROKER_PORT}")
            self.client.connect(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"MQTT connection error: {e}")

    def check_queue(self):
        """Checks the message queue and updates the Tkinter display."""
        while not message_queue.empty():
            message, topic = message_queue.get() # Get both message and topic
            
            # Find the correct text widget for the topic
            if topic in self.topic_displays:
                text_widget = self.topic_displays[topic]
                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, message)
                text_widget.see(tk.END) # Scroll to the end
                text_widget.config(state=tk.DISABLED)
            else:
                print(f"Warning: Message received for unknown topic: {topic}")
        self.master.after(100, self.check_queue)

    def on_closing(self):
        """Handles closing the Tkinter window."""
        print("Disconnecting MQTT client...")
        self.client.loop_stop()
        self.client.disconnect()
        self.master.destroy()

# --- Main execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MqttSubscriberApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
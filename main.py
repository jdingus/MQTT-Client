import sys
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QLabel

# Define the MQTT broker address and port
broker_address = "45.76.236.64"
broker_port = 1883

# Create the MQTT client object and connect to the broker
client = mqtt.Client()
client.connect(broker_address, broker_port)

# Create the PyQt application object
app = QApplication(sys.argv)

# Create the main window widget and add the tree view to it
main_window = QWidget()
layout = QVBoxLayout()
main_window.setLayout(layout)

# Add QLabel to display the selected topic value
selected_topic_value = QLabel("Selected Topic Value: None")
layout.addWidget(selected_topic_value)

# Create the tree view widget
tree_widget = QTreeWidget()
tree_widget.setHeaderLabels(["Topic", "Payload"])
layout.addWidget(tree_widget)

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    topic = message.topic
    try:
        payload = message.payload.decode('utf-8')
    except UnicodeDecodeError:
        payload = message.payload.decode('latin-1')
    # print(f"Received message: {topic} - {payload}")
    update_gui(topic, payload)

# Set the message received callback function
client.on_message = on_message

# Subscribe to the desired topics
client.subscribe("#")

# Create a dictionary to hold the items in the tree
items = {}

# Create the custom function to update the tree view
def update_gui(topic, payload):
    # Split the topic into separate levels
    levels = topic.split("/")
    # Traverse the tree to the correct node and add the payload as a leaf
    current_item = tree_widget.invisibleRootItem()
    for level in levels:
        if level not in items:
            # Create a new item if it does not exist
            items[level] = QTreeWidgetItem(current_item, [level, ''])
        current_item = items[level]
    # Set the payload as the second column of the current item
    current_item.setText(1, payload)
    # print(f"Updated GUI with message: {topic} - {payload}")
    print('Data Object:', [current_item.text(0), current_item.text(1)])

# Connect the function to the tree_widget's item clicked signal
def on_tree_widget_item_clicked(item, column):
    # Set the selected topic value label to the payload of the selected item
    selected_topic_value.setText(f"Selected Topic Value: {item.text(1)}")

tree_widget.itemClicked.connect(on_tree_widget_item_clicked)

# Start the MQTT client loop in a separate thread
client.loop_start()

# Show the main window and run the PyQt application loop
main_window.show()
sys.exit(app.exec_())

import sys
import json
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QComboBox, QLineEdit, QPushButton, 
                            QTextEdit, QLabel, QFormLayout, QMessageBox,
                            QDialog, QDialogButtonBox, QTabWidget, QInputDialog, QSplitter, QListWidget, QInputDialog, QSplitter, 
                           QVBoxLayout, QPushButton, QWidget, QMessageBox,
                           QMenu)
from PyQt6.QtCore import Qt
import openai
import keyring
import os

class APIKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Key Configuration")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Create form layout
        form_layout = QFormLayout()
        
        # API Key selector
        self.key_type = QComboBox()
        self.key_type.addItems(["OpenAI API Key", "Custom API Key 1", "Custom API Key 2"])
        form_layout.addRow("Select API Key:", self.key_type)
        
        # API Key input
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("API Key:", self.key_input)
        
        # Add form to main layout
        layout.addLayout(form_layout)
        
        # Show/Hide key button
        self.toggle_visibility = QPushButton("Show Key")
        self.toggle_visibility.setCheckable(True)
        self.toggle_visibility.toggled.connect(self.toggle_key_visibility)
        layout.addWidget(self.toggle_visibility)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_key)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Load existing key if available
        self.key_type.currentTextChanged.connect(self.load_existing_key)
        self.load_existing_key()

    def toggle_key_visibility(self, checked):
        if checked:
            self.key_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_visibility.setText("Hide Key")
        else:
            self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_visibility.setText("Show Key")

    def load_existing_key(self):
        key_type = self.key_type.currentText()
        existing_key = keyring.get_password("APIAutomationTool", key_type)
        if existing_key:
            self.key_input.setText(existing_key)

    def save_key(self):
        key_type = self.key_type.currentText()
        api_key = self.key_input.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key")
            return
        
        # Save to system keyring
        keyring.set_password("APIAutomationTool", key_type, api_key)
        
        # If it's OpenAI key, set it in the openai module
        if key_type == "OpenAI API Key":
            openai.api_key = api_key
        
        QMessageBox.information(self, "Success", f"{key_type} has been saved")
        self.accept()

# ... (previous imports and APIKeyDialog class remain the same)

class APIEndpointSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Get AI Support")
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout(self)
        
        # Description input
        description_label = QLabel("Describe the issue / question:")
        layout.addWidget(description_label)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Example: I need the Microsoft Graph API Endpoint")
        layout.addWidget(self.description_input)
        
        # Results display
        results_label = QLabel("Response:")
        layout.addWidget(results_label)
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_endpoints)
        button_layout.addWidget(search_button)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)

    def search_endpoints(self):
        try:
            if not openai.api_key:
                raise ValueError("OpenAI API key is not set. Please configure it first.")

            description = self.description_input.toPlainText().strip()
            if not description:
                raise ValueError("Please enter your search query below.")

            prompt = f"""
            Help me find appropriate API endpoints based on this description:
            {description}

            For API endpoint related questions, please respond in HTML format with appropriate formatting for readability. Assume JSON formatted headers and body unless otherwise specified.
            Include:
            1. Suggested API endpoints (with full URLs)
            2. Required HTTP method
            3. Expected request headers and body format
            4. Brief description of what the endpoint does

            Use:
            - <h3> for main sections
            - <b> for important terms
            - <pre> for code blocks
            - <ul> and <li> for lists
            - <br> for line breaks
            Format the response in a clear, structured way using HTML tags.
            """

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            self.results_display.setText(response.choices[0].message.content)
            
            # Set HTML content in the results display
            self.results_display.setHtml(response.choices[0].message.content)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    
# ... (rest of the code remains the same)



class APIAutomationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API Automation Tool")
        self.setGeometry(100, 100, 1200, 800)  # Made window wider
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Create horizontal splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create sidebar for saved configurations
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Add label and buttons for configuration management
        sidebar_layout.addWidget(QLabel("Saved Requests"))
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Add New Configuration button
        new_config_btn = QPushButton("New")
        new_config_btn.clicked.connect(self.save_current_config)
        button_layout.addWidget(new_config_btn)
        
        sidebar_layout.addLayout(button_layout)
        
        # Add list widget for saved configurations
        self.config_list = QListWidget()
        self.config_list.itemDoubleClicked.connect(self.load_config)
        self.config_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.config_list.customContextMenuRequested.connect(self.show_context_menu)
        sidebar_layout.addWidget(self.config_list)
        
        # Create main content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # Add toolbar for configuration
        toolbar_layout = QHBoxLayout()
        
        # API Key configuration button
        api_key_button = QPushButton("Configure API Keys")
        api_key_button.clicked.connect(self.show_api_key_dialog)
        toolbar_layout.addWidget(api_key_button)
        
        # Add toolbar to main layout
        content_layout.addLayout(toolbar_layout)
        
        # Create tab widget
        tab_widget = QTabWidget()
        content_layout.addWidget(tab_widget)
        
        # Request Tab
        request_tab = QWidget()
        request_layout = QVBoxLayout(request_tab)
        
        # Add API Search button
        search_button = QPushButton("AI Support")
        search_button.clicked.connect(self.show_endpoint_search)
        request_layout.addWidget(search_button)
        
        # Create form layout for API configuration
        form_layout = QFormLayout()
        
        # Request body format selector
        self.body_format = QComboBox()
        self.body_format.addItems(["application/x-www-form-urlencoded", "application/json"])
        self.body_format.currentTextChanged.connect(self.update_body_placeholder)
        form_layout.addRow("Body Format:", self.body_format)
        
        # HTTP Method selector
        self.method_selector = QComboBox()
        self.method_selector.addItems(["GET", "POST", "PUT", "DELETE", "PATCH"])
        form_layout.addRow("HTTP Method:", self.method_selector)
        
        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter API URL")
        form_layout.addRow("URL:", self.url_input)
        
        # Headers input
        self.headers_input = QTextEdit()
        self.headers_input.setPlaceholderText('{"Content-Type": "application/json"}')
        self.headers_input.setMaximumHeight(100)
        form_layout.addRow("Headers (JSON):", self.headers_input)
        
        # Request body input
        self.body_input = QTextEdit()
        self.body_input.setMaximumHeight(100)
        form_layout.addRow("Request Body:", self.body_input)
        
        # Set initial placeholder
        self.update_body_placeholder()
        
        request_layout.addLayout(form_layout)
        
        # Add Send button
        self.send_button = QPushButton("Send Request")
        self.send_button.clicked.connect(self.send_request)
        request_layout.addWidget(self.send_button)
        
        # Response section
        response_label = QLabel("Response:")
        request_layout.addWidget(response_label)
        
        # Response status
        self.response_status = QLabel()
        request_layout.addWidget(self.response_status)
        
        # Response body
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)
        request_layout.addWidget(self.response_output)
        
        # Save response button
        self.save_button = QPushButton("Save Response")
        self.save_button.clicked.connect(self.save_response)
        request_layout.addWidget(self.save_button)
        
        # Add request tab to tab widget
        tab_widget.addTab(request_tab, "API Request")
        
        # History Tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        history_layout.addWidget(self.history_text)
        
        tab_widget.addTab(history_tab, "Request History")
        
        # Add both widgets to splitter
        splitter.addWidget(sidebar)
        splitter.addWidget(content)
        
        # Set initial splitter sizes (30% sidebar, 70% content)
        splitter.setSizes([300, 700])
        
        # Create main layout and add splitter
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(splitter)
        
        # Initialize request history
        self.request_history = []
        
        # Load OpenAI API key if available
        self.load_api_keys()
        
        # Load saved configurations
        self.config_file = "saved_requests.json"
        self.load_saved_configs()
    #
    ##
    #
    

    def show_context_menu(self, position):
        """Shows context menu for saved configurations"""
        menu = QMenu()
        current_item = self.config_list.currentItem()
        
        if current_item:
            load_action = menu.addAction("Load")
            edit_action = menu.addAction("Edit Name")
            delete_action = menu.addAction("Delete")
            
            action = menu.exec(self.config_list.mapToGlobal(position))
            
            if action == load_action:
                self.load_config(current_item)
            elif action == edit_action:
                self.edit_config_name(current_item)
            elif action == delete_action:
                self.delete_config(current_item)

    def load_saved_configs(self):
        """Loads saved configurations from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    configs = json.load(f)
                    for name in configs.keys():
                        self.config_list.addItem(name)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load saved configurations: {str(e)}")

    def save_current_config(self):
        """Saves current configuration"""
        try:
            name, ok = QInputDialog.getText(self, "Save Configuration", 
                                          "Enter a name for this configuration:")
            
            if ok and name:
                # Get current configuration
                config = {
                    "method": self.method_selector.currentText(),
                    "url": self.url_input.text(),
                    "headers": self.headers_input.toPlainText(),
                    "body_format": self.body_format.currentText(),
                    "body": self.body_input.toPlainText()
                }
                
                # Load existing configs
                configs = {}
                if os.path.exists(self.config_file):
                    with open(self.config_file, 'r') as f:
                        configs = json.load(f)
                
                # Add new config
                configs[name] = config
                
                # Save to file
                with open(self.config_file, 'w') as f:
                    json.dump(configs, f, indent=2)
                
                # Add to list if not already there
                if self.config_list.findItems(name, Qt.MatchFlag.MatchExactly) == []:
                    self.config_list.addItem(name)
                
                QMessageBox.information(self, "Success", "Configuration saved successfully!")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")

    def load_config(self, item):
        """Loads selected configuration"""
        try:
            with open(self.config_file, 'r') as f:
                configs = json.load(f)
                config = configs[item.text()]
                
                # Apply configuration
                self.method_selector.setCurrentText(config["method"])
                self.url_input.setText(config["url"])
                self.headers_input.setPlainText(config["headers"])
                self.body_format.setCurrentText(config["body_format"])
                self.body_input.setPlainText(config["body"])
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")

    def edit_config_name(self, item):
        """Edits name of saved configuration"""
        try:
            old_name = item.text()
            new_name, ok = QInputDialog.getText(self, "Edit Configuration Name", 
                                              "Enter new name:", text=old_name)
            
            if ok and new_name and new_name != old_name:
                # Load configs
                with open(self.config_file, 'r') as f:
                    configs = json.load(f)
                
                # Rename config
                configs[new_name] = configs.pop(old_name)
                
                # Save configs
                with open(self.config_file, 'w') as f:
                    json.dump(configs, f, indent=2)
                
                # Update list item
                item.setText(new_name)
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename configuration: {str(e)}")

    def delete_config(self, item):
        """Deletes saved configuration"""
        try:
            reply = QMessageBox.question(self, "Delete Configuration",
                                       f"Are you sure you want to delete '{item.text()}'?",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                # Load configs
                with open(self.config_file, 'r') as f:
                    configs = json.load(f)
                
                # Delete config
                del configs[item.text()]
                
                # Save configs
                with open(self.config_file, 'w') as f:
                    json.dump(configs, f, indent=2)
                
                # Remove from list
                self.config_list.takeItem(self.config_list.row(item))
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete configuration: {str(e)}")

    def update_body_placeholder(self):
        if self.body_format.currentText() == "application/x-www-form-urlencoded":
            self.body_input.setPlaceholderText('key1=value1&key2=value2&key3=value3')
        else:
            self.body_input.setPlaceholderText('{\n    "key1": "value1",\n    "key2": "value2"\n}')

    def parse_body_input(self):
        body_format = self.body_format.currentText()
        body_text = self.body_input.toPlainText().strip()
        
        if not body_text:
            return None
            
        if body_format == "application/x-www-form-urlencoded":
            try:
                body_dict = {}
                pairs = body_text.split('&')
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        body_dict[key.strip()] = value.strip()
                return body_dict
            except Exception as e:
                raise ValueError(f"Invalid form data format: {str(e)}")
        else:
            try:
                return json.loads(body_text)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format in request body")

    def send_request(self):
        try:
            # Get request parameters
            method = self.method_selector.currentText()
            url = self.url_input.text().strip()
            
            if not url:
                raise ValueError("URL is required")
            
            # Parse headers
            headers = {}
            headers_text = self.headers_input.toPlainText().strip()
            if headers_text:
                try:
                    headers = json.loads(headers_text)
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON in headers")
            
            # Set content type header based on body format
            body_format = self.body_format.currentText()
            headers['Content-Type'] = body_format
            
            # Parse body based on format
            body = self.parse_body_input()
            
            # Send request with appropriate formatting
            if body_format == "application/x-www-form-urlencoded":
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=body if body else None  # Use data parameter for form data
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body if body else None  # Use json parameter for JSON data
                )
            
            # Update status
            self.response_status.setText(f"Status: {response.status_code}")
            
            # Try to format JSON response
            try:
                formatted_response = json.dumps(response.json(), indent=2)
            except:
                formatted_response = response.text
                
            self.response_output.setText(formatted_response)
            
            # Add to history
            history_entry = {
                "method": method,
                "url": url,
                "headers": headers,
                "body_format": body_format,
                "body": body,
                "status": response.status_code,
                "response": formatted_response
            }
            self.request_history.append(history_entry)
            self.update_history_display()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_history_display(self):
        history_text = ""
        for i, entry in enumerate(self.request_history, 1):
            history_text += f"\n{'='*50}\n"
            history_text += f"Request #{i}\n"
            history_text += f"Method: {entry['method']}\n"
            history_text += f"URL: {entry['url']}\n"
            history_text += f"Content-Type: {entry['body_format']}\n"
            history_text += f"Status: {entry['status']}\n"
            history_text += f"Headers: {json.dumps(entry['headers'], indent=2)}\n"
            if entry['body']:
                if entry['body_format'] == "application/x-www-form-urlencoded":
                    body_str = "&".join(f"{k}={v}" for k, v in entry['body'].items())
                    history_text += f"Body: {body_str}\n"
                else:
                    history_text += f"Body: {json.dumps(entry['body'], indent=2)}\n"
            history_text += f"\nResponse:\n{entry['response']}\n"
        
        self.history_text.setText(history_text)

    def save_response(self):
        try:
            response_text = self.response_output.toPlainText()
            if not response_text:
                raise ValueError("No response to save")
                
            with open("api_response.json", "w") as f:
                f.write(response_text)
                
            QMessageBox.information(self, "Success", "Response saved to api_response.json")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        #?#?#?#?#?#?

    def show_endpoint_search(self):
        """Shows the API Endpoint search dialog"""
        try:
            dialog = APIEndpointSearchDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open search dialog: {str(e)}")

    def show_api_key_dialog(self):
        """Shows the API Key configuration dialog"""
        try:
            dialog = APIKeyDialog(self)
            if dialog.exec():  # Returns True if user clicked Save
                # Reload API keys after configuration
                self.load_api_keys()
                QMessageBox.information(self, "Success", "API Keys updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to configure API keys: {str(e)}")

    def load_api_keys(self):
        """Loads saved API keys from the system keyring"""
        try:
            # Load OpenAI key
            openai_key = keyring.get_password("APIAutomationTool", "OpenAI API Key")
            if openai_key:
                openai.api_key = openai_key
                
            # Load other custom keys if needed
            custom_key1 = keyring.get_password("APIAutomationTool", "Custom API Key 1")
            custom_key2 = keyring.get_password("APIAutomationTool", "Custom API Key 2")
            
            # Store custom keys in instance variables if needed
            self.custom_key1 = custom_key1
            self.custom_key2 = custom_key2
            
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load some API keys: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = APIAutomationTool()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
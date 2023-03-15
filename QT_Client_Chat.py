import markdown
import openai
import PyQt6
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget, QProgressDialog)

# add this line if you are using another API endpoint
# openai.api_base = ""

# enter your OpenAI API key here
openai.api_key = ""

class MyQTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == PyQt6.QtCore.Qt.Key.Key_Return and event.modifiers() == PyQt6.QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.parent.add_input()
        else:
            super().keyPressEvent(event)


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.chat_history = QTextEdit()
        self.chat_input = MyQTextEdit(self)
        self.send_button = QPushButton('Send')
        self.clear_button = QPushButton('Clear')
        self.chat_box = QVBoxLayout()
        self.button_box = QHBoxLayout()
        self.setWindowTitle('GPT Chat Client')
        self.messages = []
        self.textEditContent = """<style>pre, code{background-color:#DBE4C6;}</style>"""

        self.init_ui()

    def init_ui(self):
        self.chat_box.addWidget(QLabel('Chat History'))
        self.chat_box.addWidget(self.chat_history)
        self.chat_box.addWidget(QLabel('Enter your message:'))
        self.chat_box.addWidget(self.chat_input)
        self.chat_box.addLayout(self.button_box)

        self.chat_history.setReadOnly(True)

        self.button_box.addWidget(self.send_button)
        self.button_box.addWidget(self.clear_button)

        self.setLayout(self.chat_box)
        self.send_button.clicked.connect(self.add_input)
        self.send_button.setStyleSheet(
            "background-color: #94AF9F; color: white; font-size: 16px; font-weight: bold;border-radius: 10px; padding: 10px;")
        self.clear_button.clicked.connect(self.clear_chat)
        self.clear_button.setStyleSheet(
            "background-color: white;font-size: 16px; border-radius: 10px; padding: 10px;")

        self.chat_input.setPlaceholderText("Enter your message here")
        self.chat_input.setAcceptRichText(False)
        self.chat_input.setMaximumHeight(100)

        self.showMaximized()

    def send_message(self):
        pass

    def clear_chat(self):
        self.messages = []
        self.textEditContent = ""
        self.chat_history.clear()

    def display_message(self, message, role="bot"):
        message = message.strip()
        message = markdown.markdown(
            message, extensions=['fenced_code', 'tables'])

        print(message)

        if role == "user":
            message = f"""<div style="font-size: 16px;"><p style="background-color:#94AF9F; color:white; font-weight: bold;">You:</p>{message}<div>"""
        else:
            message = f"""<div style="font-size: 16px;"><p style="background-color:#94AF9F; color:white; font-weight: bold;">Bot:</p>{message}<div><br>"""

        self.textEditContent += message

        self.chat_history.setHtml(self.textEditContent)

    def add_input(self):
        user_input = self.chat_input.toPlainText()
        self.messages.append({"role": "user", "content": user_input})
        self.display_message(user_input, role="user")
        self.chat_input.clear()
        self.start_loading()

    def start_loading(self):

        self.progress = QProgressDialog(self)
        self.progress.setWindowModality(
            PyQt6.QtCore.Qt.WindowModality.WindowModal)
        self.progress.setCancelButton(None)
        self.progress.setRange(0, 1)
        self.progress.setLabelText("Waiting for answer...")
        self.progress.show()

        self.add_output()

    def add_output(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages)
        response = completion.choices[0].message.content
        self.messages.append(completion.choices[0].message)
        self.display_message(response, role="bot")
        self.end_loading()

    def end_loading(self):
        self.progress.close()


if __name__ == '__main__':
    app = QApplication([])

    # set app icon
    app_icon = PyQt6.QtGui.QIcon('favicon-180.png')
    app.setWindowIcon(app_icon)
    chat_app = ChatApp()
    app.exec()

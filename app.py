# Импорт встроенной библиотеки для работы веб-сервером
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def get_context_data(self):
        """Метод для чтения HTML-файла"""
        with open("contact.html", "r", encoding="utf-8") as file:
            context = file.read()
        return context

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(bytes(self.get_context_data(), "utf-8"))  # Тело ответа с содержимым HTML-файла

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)  # Чтение данных запроса
        print(body.decode("utf-8"))  # Декодируем байты в строку для вывода на экран
        response = {'message': 'Data received'}  # Ответ в формате JSON
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "application/json")  # Указание типа данных
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(bytes(json.dumps(response), "utf-8"))  # Тело ответа в формате JSON

if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрам в сети
    # принимать запросы и отправлять их на обработку специальному классу MyServer
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
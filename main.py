import posixpath
import socket
import os
import xml.etree.ElementTree as ET
import sys

class HttpServer:
    def __init__(self, PORT):
        self.HOST, self.PORT = '', PORT
        self.s = socket.socket(socket.AF_INET)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.MSG_LEN = 1024

    def get_file_content(self, file_path):
        if '.' in file_path:
            with open(file_path[1:]) as f:
                content = f.read()
                return content

    def get_content_from_dir(self, dir_path):
        content = {"files": [], "folders": []}
        if "favicon.ico" == dir_path:
            return content

        print(dir_path)
        dir_path = dir_path[1:]
        print(dir_path)

        for file in os.listdir(os.path.abspath(dir_path)):
            if os.path.isdir(os.path.join(dir_path, file)):
                content["folders"].append(file)
            else:
                content["files"].append(file)
        return content

    def form_html_page(self, content):
        html_tag = ET.Element('html')  # root
        head_tag = ET.SubElement(html_tag, 'head')
        body_tag = ET.SubElement(html_tag, 'body')
        h1_tag = ET.SubElement(body_tag, 'h1')
        h1_tag.text = 'Hello'

        if "folders" not in content and "files" not in content:
            return ET.tostring(html_tag)

        for directory in content["folders"]:
            href = {'href': directory}
            link_tag = ET.SubElement(body_tag, 'a', attrib=href)
            link_tag.text = directory
            br_tag = ET.SubElement(link_tag, 'br')
        for file in content["files"]:
            href = {'href': file}
            file_tag = ET.SubElement(body_tag, 'a', attrib=href)
            file_tag.text = file

        return ET.tostring(html_tag)

    def run(self):
        self.s.listen(5)
        while True:
            client_connection, client_address = self.s.accept()
            request = client_connection.recv(self.MSG_LEN)
            address_path = str(request).split()[1]

            if os.path.isfile('indx.html'):
                with open('index.html') as f:
                    response_data = str.encode(f.read())
            else:
                response_data = ''
                if address_path == "/favicon.ico":
                    continue
                if '.' in address_path:
                    response_data = str.encode(self.get_file_content(address_path))
                else:
                    content = self.get_content_from_dir(address_path)
                    response_data = self.form_html_page(content)

            client_connection.sendall(response_data)
            client_connection.close()


PORT = 8000

if len(sys.argv) == 2 and str(sys.argv[1]).isdigit():
    PORT = int(sys.argv[1])

server = HttpServer(PORT)
server.run()

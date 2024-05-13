import socket
import json
import webbrowser

def sockett():
    webbrowser.open('set.html')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 4444))
    server_socket.listen(1)

    print('服务器已启动,等待连接...')

    while True:
        client_socket, address = server_socket.accept()
        print(f'连接建立: {address}')

        data = client_socket.recv(10240).decode('utf-8')

        if 'OPTIONS' in data:
            response_headers = [
                'HTTP/1.1 200 OK',
                'Access-Control-Allow-Origin: *',
                'Access-Control-Allow-Methods: POST',
                'Access-Control-Allow-Headers: Content-Type',
                'Connection: close',
                '',
                ''
            ]
            client_socket.send('\r\n'.join(response_headers).encode('utf-8'))
        else:
            try:
                _, body = data.split('\r\n\r\n', 1)
                json_data = json.loads(body)
                json_string = json.dumps(json_data, indent=4)

                with open('set.json', 'w') as file:
                    file.write(json_string)

                print('数据已成功保存到set.json文件中')
                response_headers = [
                    'HTTP/1.1 200 OK',
                    'Access-Control-Allow-Origin: *',
                    'Content-Type: text/plain',
                    'Connection: close',
                    '',
                    '数据已成功接收并保存'
                ]
                client_socket.send('\r\n'.join(response_headers).encode('utf-8'))
                break
            except (ValueError, json.JSONDecodeError):
                print('无效的请求数据')
                response_headers = [
                    'HTTP/1.1 400 Bad Request',
                    'Access-Control-Allow-Origin: *',
                    'Content-Type: text/plain',
                    'Connection: close',
                    '',
                    '无效的请求数据'
                ]
                client_socket.send('\r\n'.join(response_headers).encode('utf-8'))

    client_socket.close()


# sockett()
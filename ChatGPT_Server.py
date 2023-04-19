import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from revChatGPT.V1 import Chatbot

chatbot = Chatbot(config={
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJwZXBlZGQ4NjRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItTVFod3JOMEg0aGpSYkZxNkZuWm44dEgxIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzhlZmZlNzhkZDIxZDA3MmFhYjlmYWQiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjgwNzkwNjkxLCJleHAiOjE2ODIwMDAyOTEsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb2ZmbGluZV9hY2Nlc3MifQ.xzMM5ejeSQfx8zG7s9Gzumcne8-WxOgBSJCgH1SMLf6iPuYnMtIRxI1t_vtDdtLMq0gPoEwW_AaaJF-m7jk6gEt2JWaR0Ldlx7uBzz_UdtqJHFVbk7MD7RIAKBG4QyVC2JPdHyr2i1F0C4ONt6LOf9erlvh95XYl8rGCXYM6afHJWc5g5SruftjbcTnX1deFciXWVadf94ZusUUkZI7TMX-_K1QUTSl8VN7muPV-8it9NXPz-BlrjSThpN0jMirnJvcejs6cohCdtfAl1vNwKtfOkbpu2FCUNZRsQFJez6oju5nc2ozFQM16TGabxTbV6mXpRJeXpiiO-J51fEUfFw"
})

class responseVO:
    # 代码枚举
    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

    def __init__(self, code, message):
        self.code = code
        self.message = message

class ChatBotServer(BaseHTTPRequestHandler):

    def do_POST(self):
        # 请求前判断请求体格式是否正确
        if self.headers['Content-Type'] != 'application/json':
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Bad Request'.encode('utf-8'))
            return
        # 解析请求数据
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length)
        request = json.loads(request_body)
        print(request)

        # 处理请求
        result = self.process_request(request)

        # 返回结果
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = responseVO(responseVO.SUCCESS, result)
        response = json.dumps(response.__dict__, indent=4, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response)

    def process_request(self, request):
        # 解析请求
        prompt = request['prompt']

        # 生成回复
        response = ''
        for data in chatbot.ask(prompt):
            response = data['message']

        # 返回结果
        return response


if __name__ == '__main__':
    # 启动服务
    server = HTTPServer(('localhost', 5000), ChatBotServer)
    print('Starting ChatGPT server, use <Ctrl-C> to stop')
    server.serve_forever()

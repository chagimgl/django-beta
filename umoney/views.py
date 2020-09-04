from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from umoney.models import TopupReq, ConnectionReq, ConnectionResp
from umoney.serializers import TopupReqSerializer, ConnectionReqSerializer, ConnectionRespSerializer
import socket
import functools

master_key = '30313233343536373839414243444546'

stx_hex = '02'
message_length = '0219'
destination_info = '0000'
source_info = 'POS0'
version = '00'
message_data = ''
etx_hex = '03'

message_request_data = 'ID1234ID1234ID1222                                                                                                              '    
pos_id = 'ID1234ID1234ID1222'
merchant_information = '3010002014                              ' 
authentication_id = '197AFA642645A992'
  

OID_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'encrypted_wk': 231,
    'min_topup_amount': 241,
    'tcp_addr1': 305,
    'tcp_port1': 311,
    'tcp_addr2': 375,
    'tcp_port2': 381,
    'merchant_name': 531,
    'system_datetime': 545,
    'filler_space': 711,
    'etx': 712}

PDA_response_len_arr = {
    'stx': 0,
    'message_length': 4,
    'routing_destination_info': 8,
    'routing_source_info': 12,
    'routing_version': 14,
    'message_type_id': 18,
    'primary_bit_map': 34,
    'processing_code': 40,
    'transmission_datetime': 50,
    'time_local': 56,
    'date_local': 60,
    'transaction_uniq': 72,
    'response_code': 74,
    'merchant_id': 89,
    'merchant_info': 129,
    'result_message_len': 132,
    'result_message_data': 196,
    'response_data_len': 199,
    'encrypted_vsam': 231,
    'filler_space': 327,
    'etx': 328
}

class UmoneyReqList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = TopupReq.objects.all()
    serializer_class = TopupReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.create(request, *args, **kwargs)
        return obj

class UmoneyReqDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = TopupReq.objects.all()
    serializer_class = TopupReqSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ConnectionReqList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = ConnectionReq.objects.all()
    serializer_class = ConnectionReqSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        message_type_id = '0300'
        primary_bit_map = '2200000008200010'
        processing_code = '481100'
        transaction_unique = '000000000001'
        req_data = prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, 1)
        data = send_socket_receive_data(req_data)
        resp_data = data_to_array_by_type(OID_response_len_arr, data)
        encrypted_wk = resp_data['encrypted_wk']
        res = decrypt_seed128(transaction_unique + merchant_information[6:10], encrypted_wk, master_key)
        decrypted_wk = res.decode("ascii")
        request.data['message_type_id'] = message_type_id
        request.data['primary_bit_map'] = primary_bit_map
        request.data['processing_code'] = processing_code
        request.data['merchant_information_terminal_id'] = merchant_information
        request.data['terminal_id'] = merchant_information
        request.data['pos_id'] = pos_id
        request.data['transaction_unique'] = transaction_unique
        obj = self.create(request, *args, **kwargs)

        oid_resp_data = {
            'message_type_id': resp_data['message_type_id'],
            'primary_bit_map': resp_data['primary_bit_map'],
            'processing_code': resp_data['processing_code'],
            'transmission_datetime': resp_data['transmission_datetime'],
            'transaction_unique': resp_data['transaction_uniq'],
            'merchant_id': resp_data['merchant_id'],
            'merchant_info_terminal_id': resp_data['merchant_info'][0:10],
            'result_message_len': resp_data['result_message_len'],
            'result_message_data': resp_data['result_message_data'],
            'response_data_len': resp_data['response_data_len'],
            'working_key': decrypted_wk,
            'minimum_topup_amount': resp_data['min_topup_amount'],
            'system_datetime': resp_data['system_datetime'],
            'pos_id': pos_id, 
            'terminal_id': merchant_information, 
            'authentication_id': '', 
        }
        serializer = ConnectionRespSerializer(data=oid_resp_data)
        if serializer.is_valid():
            serializer.save()
        
        message_type_id = '0300'
        primary_bit_map = '2200000008200010'
        processing_code = '486000'
        transaction_unique = '000000000002'
        req_data = prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, 2, authentication_id, decrypted_wk)
        pda_req_data = {
            'message_type_id': message_type_id,
            'primary_bit_map': primary_bit_map,
            'processing_code': processing_code,
            'transmission_datetime': '',
            'transaction_unique': transaction_unique,
            'merchant_info_terminal_id': merchant_information[0:10],
            'pos_id': pos_id, 
            'terminal_id': merchant_information[0:10], 
            'authentication_id': authentication_id, 
            'vsam_id': ''
        }
        serializer = ConnectionReqSerializer(data=pda_req_data)
        if serializer.is_valid():
            serializer.save()

        data = send_socket_receive_data(req_data)
        PDA_resp_data = data_to_array_by_type(PDA_response_len_arr, data)

        pda_resp_data_model = {
            'message_type_id': PDA_resp_data['message_type_id'],
            'primary_bit_map': PDA_resp_data['primary_bit_map'],
            'processing_code': PDA_resp_data['processing_code'],
            'transmission_datetime': PDA_resp_data['transmission_datetime'],
            'transaction_unique': PDA_resp_data['transaction_uniq'],
            'merchant_id': PDA_resp_data['merchant_id'],
            'merchant_info_terminal_id': PDA_resp_data['merchant_info'][0:10],
            'result_message_len': PDA_resp_data['result_message_len'],
            'result_message_data': PDA_resp_data['result_message_data'],
            'response_data_len': PDA_resp_data['response_data_len'],
            'working_key': decrypted_wk,
            'minimum_topup_amount': '',
            'system_datetime': '',
            'pos_id': pos_id, 
            'terminal_id': PDA_resp_data['merchant_info'][0:10], 
            'authentication_id': authentication_id, 
            'vsam_id': decrypt_seed128(PDA_resp_data['transaction_uniq'] + PDA_resp_data['merchant_info'][0:10], PDA_resp_data['encrypted_vsam'], decrypted_wk).decode("ascii")
        }
        serializer = ConnectionRespSerializer(data=pda_resp_data_model)
        if serializer.is_valid():
            print('hihi')
            serializer.save()
        return Response({})

class ConnectionReqDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = ConnectionReq.objects.all()
    serializer_class = ConnectionReqSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ConnectionRespList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = ConnectionResp.objects.all()
    serializer_class = ConnectionRespSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

def data_to_array_by_type(response_len_data, data):
    resp_data = {}
    tmp = -1
    for k,v in response_len_data.items():
        print(k + ": " + (data[tmp:v+1]).decode())
        resp_data[k] = (data[tmp:v+1]).decode()
        tmp = v+1
    return resp_data 

def decrypt_seed128(source_data, encrypted_str, mkey):
    compile_java('decryptSEED128.java')
    res = execute_java('decryptSEED128.java', source_data + encrypted_str + mkey, '')
    return res

def encrypt_seed128(source_data, decrypted_str, working_key):
    compile_java('encryptSEED128.java')
    res = execute_java('encryptSEED128.java', source_data + decrypted_str + working_key, '')
    return res

def send_socket_receive_data(req_data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("202.126.92.39", 12021))
    s.send(bytes(req_data, encoding='ascii'))
    data = ''
    data = s.recv(4096)
    s.close()
    return data

def prepare_req_data(message_type_id, primary_bit_map, processing_code, transaction_unique, req_type, auth_id='', working_key=''):
    message_request_data = 'ID1234ID1234ID1222                                                                                                              '    
    if req_type == 1:
        message_request_data = 'ID1234ID1234ID1222                                                                                                              '
    elif req_type == 2:
        # print(encrypt_seed128(transaction_unique+merchant_information[6:10], auth_id).decode("ascii")+"\n\n\n")
        message_request_data = 'ID1234ID1234ID1222                                              ' + encrypt_seed128(transaction_unique+merchant_information[6:10], auth_id, working_key).decode("ascii") + "                                "
    transmission_date = '0903100912'
    message_request_data_length = '131'
    
    message_data = ''
    message_data = message_data + message_type_id
    message_data = message_data + primary_bit_map
    message_data = message_data + processing_code
    message_data = message_data + transmission_date
    message_data = message_data + transaction_unique
    message_data = message_data + merchant_information
    message_data = message_data + message_request_data_length
    message_data = message_data + message_request_data
    print(message_data)
    req_data = ''
    req_data = req_data + toStr(stx_hex)
    req_data = req_data + message_length
    req_data = req_data + destination_info
    req_data = req_data + source_info
    req_data = req_data + version
    req_data = req_data + message_data
    req_data = req_data + toStr(etx_hex)
    print(req_data + "\n")
    return req_data

""" 
java compiler
"""
import os.path,subprocess
from subprocess import STDOUT,PIPE

def compile_java(java_file):
    print(subprocess.check_call(['pwd']))
    subprocess.check_call(['javac', java_file])

def execute_java(java_file, data, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class, data]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin)
    print(stdout)
    return stdout

"""
End java compiler
"""


#convert string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return functools.reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''

# @api_view(['GET', 'POST'])
# def umoney_req_list(request, format=None):
#     """
#     List all code UmoneyReq, or create a new UmoneyReq.
#     """
#     if request.method == 'GET':
#         snippets = UmoneyReq.objects.all()
#         serializer = UmoneyReqSerializer(snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UmoneyReqSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def umoney_req_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code UmoneyReq.
#     """
#     try:
#         snippet = UmoneyReq.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UmoneyReqSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UmoneyReqSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



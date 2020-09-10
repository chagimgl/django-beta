from rest_framework import serializers
from umoney.models import TopupReq, TopupResp
from umoney.models import TopupCheckReq, TopupCheckResp
from umoney.models import ConnectionReq, ConnectionResp
from umoney.models import DepositBalanceInquiryReq, DepositBalanceInquiryResp
from umoney.models import TransactionAggregationInquiryReq, TransactionAggregationInquiryResp


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     card_number = serializers.CharField(required=True, allow_blank=False, max_length=16)
#     card_algorithm_id = serializers.CharField(required=True, allow_blank=False, max_length=2)
#     card_keyset_v = serializers.CharField(required=True, allow_blank=False, max_length=2)
#     card_transaction_seq_number = serializers.CharField(required=True, allow_blank=False, max_length=10)
#     card_random_number = serializers.CharField(required=True, allow_blank=False, max_length=16)
#     card_balance = serializers.CharField(required=True, allow_blank=False, max_length=10)
#     topup_amount = serializers.CharField(required=True, allow_blank=False, max_length=10)
#     sign1 = serializers.CharField(required=True, allow_blank=False, max_length=8)
#     comment = serializers.CharField(required=False, allow_blank=True, max_length=100)

#     def create(self, validated_data):
#         """
#         Create and return a new `UmoneyReq` instance, given the validated data.
#         """
#         return UmoneyReq.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance
"""
{
    "card_number": "1610000007267156",
    "card_algorithm_id": "10",
    "card_keyset_v": "01",
    "card_transaction_seq_number": "0000000150",
    "card_random_number": "89E2478B4C6DB2B4",
    "card_balance": "0000050000",
    "topup_amount": "0000000500",
    "sign1": "F66AA671",
    "comment": "HI TOPUP 500 PLEASE.",
    "tran_type": "02",
    "payment_method": "3",
    "message_type_id": "",
    "primary_bit_map": "",
    "processing_code": "",
    "transmission_datetime": "",
    "transaction_unique": "",
    "terminal_id": "",
    "request_data_len": ""
}

{ 
    "alg": "10", 
    "bal": 0000000000, 
    "idEp": "1610000007267156", 
    "idcenter": "01", 
    "ntEp": "0000000102", 
    "rep": "02e7a9630745e3f9", 
    "sign1": "273a8af4"
}

{
"card_number": "1610000007267156",
"card_algorithm_id": "10",
"card_keyset_v": "01",
"card_transaction_seq_number": "0000000102",
"card_random_number": "02e7a9630745e3f9",
"card_balance": "0000000000",
"topup_amount": "0000000500",
"sign1": "273a8af4",
"comment": "HI TOPUP 500 PLEASE.",
"tran_type": "02",
"payment_method": "3"
}
"""

class TopupReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopupReq
        fields = [
            'id', 
            'card_number', 
            'card_algorithm_id', 
            'card_keyset_v', 
            'card_transaction_seq_number', 
            'card_random_number', 
            'card_balance',
            'topup_amount',
            'sign1',
            'comment',
            'created',
            'message_type_id',
            'primary_bit_map',
            'processing_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'request_data_len',
            'tran_type',
            'payment_method',
            'payment_id',
            ]

class TopupRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopupResp
        fields = [
            'id', 
            'created', 
            'comment', 
            'message_type_id', 
            'primary_bit_map', 
            'processing_code',
            'response_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'result_message_len',
            'result_message_data',
            'tran_type',
            'card_number',
            'vsam_tran_seq_num',
            'card_balance',
            'topup_amount',
            'sign2',
            'deposit_balance',
            'payment_method',
            'sign1',
            'vsam_id',
            'vsam_id_hex',
            'payment_id',
            ]

class TopupCheckReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopupCheckReq
        fields = [
            'id', 
            'created',
            'comment',
            'message_type_id',
            'primary_bit_map',
            'processing_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'request_data_len',
            'tran_type',
            'card_number',
            'card_algorithm_id',
            'card_keyset_v',
            'card_transaction_seq_number',
            'card_random_number',
            'topup_amount',
            'card_pre_balance',
            'card_post_balance',
            'sign3',
            'result_code',
            'payment_id',
            ]

class TopupCheckRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopupCheckResp
        fields = [
            'id', 
            'created',
            'comment',
            'message_type_id',
            'primary_bit_map',
            'processing_code',
            'response_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'result_message_len',
            'result_message_data',
            'deposit_balance',
            'vsam_id',
            'sign3',
            'tran_type',
            'card_number',
            'card_algorithm_id',
            'card_keyset_v',
            'card_transaction_seq_number',
            'card_random_number',
            'topup_amount',
            'card_pre_balance',
            'card_post_balance',
            'paymentId',
            ]

class ConnectionReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionReq
        fields = [
            'id', 
            'created', 
            'message_type_id',
            'primary_bit_map',
            'processing_code',
            'transmission_datetime',
            'transaction_unique',
            'merchant_info_terminal_id',
            'pos_id', 
            'terminal_id', 
            'authentication_id', 
            'vsam_id'
            ]

class ConnectionRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionResp
        fields = [
            'id', 
            'created', 
            'message_type_id',
            'primary_bit_map',
            'processing_code',
            'response_code',
            'transmission_datetime',
            'transaction_unique',
            'merchant_id',
            'merchant_info_terminal_id',
            'result_message_len',
            'result_message_data',
            'response_data_len',
            'working_key',
            'minimum_topup_amount',
            'system_datetime',
            'pos_id', 
            'terminal_id', 
            'authentication_id', 
            'vsam_id'
            ]

class DepositBalanceInquiryReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositBalanceInquiryReq
        fields = [
            'id', 
            'created',
            'comment',
            'message_type_id',
            'primary_bit_map',
            'processing_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'request_data_len',
            'pos_id',
            'encrypted_vsam_id',
        ]

class DepositBalanceInquiryRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositBalanceInquiryResp
        fields = [
            'id', 
            'created',
            'comment',
            'message_type_id',
            'primary_bit_map',
            'response_code',
            'result_message_len',
            'result_message_data',
            'processing_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'pos_id',
            'deposit_balance',
            ]

class TransactionAggregationInquiryReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionAggregationInquiryReq
        fields = [
            'id', 
            'created',
            'comment',
            'message_type_id',
            'primary_bit_map',
            'processing_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'request_data_len',
            'pos_id',
            'encrypted_vsam_id',
            'closing_date',
        ]

class TransactionAggregationInquiryRespSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionAggregationInquiryResp
        fields = [
            'id', 
            'created',
            'comment',
            'message_type_id',
            'primary_bit_map',
            'response_code',
            'result_message_len',
            'result_message_data',
            'processing_code',
            'transmission_datetime',
            'transaction_unique',
            'terminal_id',
            'pos_id',
            'topup_count',
            'topup_amount',
            'topup_cancellation_count',
            'topup_cancellation_amount',
            'payment_count',
            'payment_amount',
            'payment_cancellation_count',
            'payment_cancellation_amount',
            ]
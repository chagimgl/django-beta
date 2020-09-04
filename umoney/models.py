from django.db import models

# Create your models here.

class ConnectionReq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    merchant_info_terminal_id = models.CharField(max_length=10, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='')
    terminal_id = models.CharField(max_length=64, blank=True, default='')
    authentication_id = models.CharField(max_length=64, blank=True, default='')
    vsam_id = models.CharField(max_length=64, blank=True, default='')

class ConnectionResp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message_type_id = models.CharField(max_length=4, blank=True, default='')
    primary_bit_map = models.CharField(max_length=16, blank=True, default='')
    processing_code = models.CharField(max_length=6, blank=True, default='')
    transmission_datetime = models.CharField(max_length=10, blank=True, default='')
    transaction_unique = models.CharField(max_length=12, blank=True, default='')
    response_code = models.CharField(max_length=2, blank=True, default='')
    merchant_id = models.CharField(max_length=15, blank=True, default='')
    merchant_info_terminal_id = models.CharField(max_length=10, blank=True, default='')
    result_message_len = models.CharField(max_length=3, blank=True, default='')
    result_message_data = models.CharField(max_length=64, blank=True, default='')
    response_data_len = models.CharField(max_length=3, blank=True, default='')
    working_key = models.CharField(max_length=32, blank=True, default='')
    minimum_topup_amount = models.CharField(max_length=10, blank=True, default='')
    system_datetime = models.CharField(max_length=14, blank=True, default='')
    pos_id = models.CharField(max_length=64, blank=True, default='')
    terminal_id = models.CharField(max_length=64, blank=True, default='')
    authentication_id = models.CharField(max_length=64, blank=True, default='')
    vsam_id = models.CharField(max_length=64, blank=True, default='')

class TopupReq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    card_number = models.CharField(max_length=16, blank=True, default='')
    card_algorithm_id = models.CharField(max_length=2, blank=True, default='')
    card_keyset_v = models.CharField(max_length=2, blank=True, default='')
    card_transaction_seq_number = models.CharField(max_length=10, blank=True, default='')
    card_random_number = models.CharField(max_length=16, blank=True, default='')
    card_balance = models.CharField(max_length=10, blank=True, default='')
    topup_amount = models.CharField(max_length=10, blank=True, default='')
    sign1 = models.CharField(max_length=8, blank=True, default='')
    comment = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['created']
from django.shortcuts import render
import requests
import json
from time import sleep

# Create your views here.
def index(request):
    context = {
    }
    return render(request, 'sbinvestment/index.html', context)

def sms(request):
    if request.method == 'GET':
        return render(request, 'sbinvestment/sendsms.html')
    elif request.method == 'POST':
        send_msg = request.POST.get('sendmsg')
        # response = {}
        if send_msg == '':
            return_msg = "메세지를 확인하세요."
            # response['error'] = "메세지를 확인하세요."
        else:
            #print(send_msg)
            member_type = 0     # 수정사항(유료인 경우 날라가도록 함)
            base_id = 'appssITu2KHnI0zUO'
            table_id = 'tblLGqfVdDK7C1YH3'
            url = "https://api.airtable.com/v0/" + base_id + "/" + table_id
            params = {"maxRecords": 50}

            api_key = 'keyl1hCA8uM5W73Bl'  # ★★★API Key
            headers = {'Authorization': 'Bearer ' + api_key}

            response = requests.get(url, params=params, headers=headers)
            # 정상 select all
            airtable_response = response.json()
            airtable_records = airtable_response['records']
            #print(airtable_records)
            if member_type == 2:
                members = airtable_records
            elif member_type == 0:  # 유료회원
                members = [x for x in airtable_records if x['fields']['Status_Num'] == 0]
            elif member_type == 1:  # 무료회원
                members = [x for x in airtable_records if x['fields']['Status_Num'] == 1]

            phonelist = []
            for p in members:
                # membeer_name  = p['fields']['이름']
                # member_phone  = p['fields']['전화번호_010']
                phonelist.append(p['fields']['전화번호_010'])
            print(phonelist)

            ########### Solapi ###############
            #import json
            import time
            import datetime
            import uuid
            import hmac
            import hashlib
            #import requests
            # apiKey, apiSecret 입력 필수
            apiKey = 'NCSGSSAS9KEDGZID'
            apiSecret = 'CWBJSXRAHISCKW65W7UBNX3CIQ5XNETT'
            # 아래 값은 필요시 수정
            protocol = 'https'
            domain = 'api.solapi.com'
            prefix = ''

            def unique_id():
                return str(uuid.uuid1().hex)

            def get_iso_datetime():
                utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
                utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
                return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

            def get_signature(key, msg):
                return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

            def get_headers(apiKey, apiSecret):
                date = get_iso_datetime()
                salt = unique_id()
                data = date + salt
                return {
                    'Authorization': 'HMAC-SHA256 ApiKey=' + apiKey + ', Date=' + date + ', salt=' + salt + ', signature=' +
                                     get_signature(apiSecret, data),
                    'Content-Type': 'application/json; charset=utf-8'
                }

            def getUrl(path):
                url = '%s://%s' % (protocol, domain)
                if prefix != '':
                    url = url + prefix
                url = url + path
                return url

            # def sendMany(data):
            #     return requests.post('https://api.solapi.com/messages/v4/send-many', headers=get_headers(apiKey, apiSecret),
            #                          json=data)

            def sendMany(data):
                return requests.post(getUrl('/messages/v4/send-many'), headers=get_headers(apiKey, apiSecret),
                                     json=data, timeout=3)

            # 한번 요청으로 1만건의 메시지 발송이 가능합니다.
            #if __name__ == '__main__':
            data = {
                'messages': [
                    {
                        'to': phonelist,
                        'from': '01089391001',
                        'text': '[SB인베스트먼트] ' + send_msg + '\n\n◆추천회원 가입하세요!! \nhttps://bit.ly/3wBI0BN\n◆투자자유의사항:투자에 대한 원금손실발생시 투자자 귀속'
                    }
                ]
            }
            sms_res = sendMany(data)
            sms_response = sms_res.json()
            log_list = sms_response['log']

            return_msg = []
            for k in log_list:
                return_msg.append(k['message'])
            # print(return_msg)
            # response['error'] = '정상 발송되었습니다.'
            # return_msg = '정상 발송되었습니다.'
        return render(request, 'sbinvestment/sendsms.html', {'error': return_msg})

def sb_member(request):
    # member_type = selection
    # print(member_type)
    member_type = 0
    base_id = 'appssITu2KHnI0zUO'
    table_id = 'tblLGqfVdDK7C1YH3'
    url = "https://api.airtable.com/v0/" + base_id + "/" + table_id
    params = {"maxRecords": 50}

    api_key = 'keyl1hCA8uM5W73Bl'  # ★★★API Key
    headers = {'Authorization': 'Bearer ' + api_key}

    response = requests.get(url, params=params, headers=headers)
    # 정상 select all
    airtable_response = response.json()
    airtable_records = airtable_response['records']
    if member_type == 0:
        members = airtable_records
    elif member_type == 1:  # 무료회원
        members = [x for x in airtable_records if x['fields']['Status'] == '무료']
    elif member_type == 2:  # 무료회원
        members = [x for x in airtable_records if x['fields']['Status'] == '유료']

    return render(request, 'sbinvestment/airplay_member.html', {'members': members})

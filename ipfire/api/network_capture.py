from scapy.all import sniff, IP, TCP, Raw
from datetime import datetime
from api.aiModel.onlu_use_mlp import predict_with_mlp
import json

captured_packets = []

# 패킷을 캡처하는 함수
def packet_callback(packet):
    global no
    no += 1
    if IP in packet:  # 패킷이 IP 계층을 포함하고 있는지 확인
        src_ip = packet[IP].src
        proto = packet[IP].proto
        protocol_name = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}.get(proto, 'Other')
        
        src_port = "N/A"
        dst_port = "N/A"
        input_id = "N/A"
        input_passwd = "N/A"
        result = "FALSE"
        # HTTP 확인: TCP 패킷 중에서 포트 80으로의 통신인 경우 HTTP로 간주
        if TCP in packet:
            if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                protocol_name = 'HTTP'
                if Raw in packet:  # Raw 데이터가 있는 경우
                    payload = packet[Raw].load.decode(errors='ignore')
                    if 'POST' in payload:  # POST 요청 확인
                        try:
                            json_data = payload.split('\r\n\r\n', 1)[1]  # HTTP 헤더와 본문을 나누고 본문 추출
                            data = json.loads(json_data)
                            input_id = data.get('id', 'N/A')
                            input_passwd = data.get('passwd', 'N/A')
                            check_id = predict_with_mlp(input_id)
                            check_passwd = predict_with_mlp(input_passwd)
                            if int(check_id) == 1 or int(check_passwd) == 1:
                                result = "TRUE"
                        except (json.JSONDecodeError, IndexError):
                            pass
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        
        log_entry = {
            "no": no,                       # 패킷이 기록된 순서를 나타내는 번호
            "input_id": input_id,           # HTTP 패킷에서 추출한 ID
            "input_passwd": input_passwd,   # HTTP 패킷에서 추출한 PW
            "source_addr": src_ip,
            "result": result,               # RESULT는 FALSE 또는 TRUE로 설정
            "protocol": protocol_name,      # PROTOCOL에 프로토콜 이름을 저장
            "src_port": src_port,
            "dst_port": dst_port,
            "time": datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S')
        }

        if result == "TRUE":
            captured_packets.insert(0, log_entry)  # 새로운 패킷을 리스트의 맨 위에 추가
        
        if len(captured_packets) > 50:  # 메모리 관리를 위해 최대 50개까지만 저장
            captured_packets.pop()

# 백그라운드에서 패킷을 캡처하는 스레드 시작
def start_packet_sniffing():
    sniff(prn=packet_callback, store=False)  # 모든 패킷을 캡처
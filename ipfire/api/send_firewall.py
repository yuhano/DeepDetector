import requests
from flask import Blueprint, jsonify
import asyncio
from concurrent.futures import ThreadPoolExecutor

send_firewall_blueprint = Blueprint('send_firewall', __name__)

@send_firewall_blueprint.route('/', methods=['POST'])
def send_firewall(host_ip, src_addr, ruleremark):
    _send_add_firewall_rule(host_ip, src_addr, ruleremark)
    _send_apply_firewall_rule(host_ip)


def _send_add_firewall_rule(host_ip, src_addr, ruleremark):
    url = f"https://{host_ip}:444/cgi-bin/firewall.cgi"
    
    headers = {
        "Authorization": "Basic YWRtaW46S2FuZ3dvbjEyMyFAIw==",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Referer": f"https://{host_ip}:444/",
        "Connection": "keep-alive",
    }

    data = (
        f"grp1=src_addr&src_addr={src_addr}&ipfire_src=ALL&std_net_src=ALL&"
        f"cust_location_src=A1&nat=dnat&dnat=AUTO&snat=RED&tgt_addr=&ipfire=ALL&"
        f"grp2=std_net_tgt&std_net_tgt=ALL&cust_location_tgt=A1&PROT=&ICMP_TYPES=All+ICMP-Types&"
        f"SRC_PORT=&TGT_PORT=&dnatport=&grp3=cust_srv&cust_srv=DNS+%28TCP%29&"
        f"RULE_ACTION=DROP&ruleremark={ruleremark}&rulepos=&ACTIVE=ON&LOG=ON&"
        f"TIME_FROM=00%3A00&TIME_TO=00%3A00&concon=&ratecon=&RATETIME=second&"
        f"config=%2Fvar%2Fipfire%2Ffirewall%2Fconfig&ACTION=saverule"
    )

    response = requests.post(url, headers=headers, data=data, verify=False)
    return response.status_code, response.text

def _send_apply_firewall_rule(host_ip):
    url = f"https://{host_ip}:444/cgi-bin/firewall.cgi"
    
    headers = {
        "Authorization": "Basic YWRtaW46S2FuZ3dvbjEyMyFAIw==",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Referer": f"https://{host_ip}:444/",
        "Connection": "keep-alive",
    }

    data = "ACTION=Apply+changes"

    response = requests.post(url, headers=headers, data=data, verify=False)
    return response.status_code, response.text


# Example usage
if __name__ == "__main__":
    host = "192.168.8.80" 
    src_addr = "197.175.34.2" 
    ruleremark = "asdffffffff"

    # status_code, response_text = _send_add_firewall_rule(host, src_addr, ruleremark)
    status_code, response_text = _send_apply_firewall_rule(host)
    print(f"Status Code: {status_code}")
    # print(f"Response Text: {response_text}")

    # asyncio.run(send_firewall_rule(host, src_addr, ruleremark))

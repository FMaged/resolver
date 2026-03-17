

import dns.resolver
from dns.rdata import Rdata
from ipaddress import IPv4Address

from records import HostName, MXRecord,ARecord, EmailDNSRecord



def get_mail_servers(domain_name:str)->list[MXRecord]:
    answers=query_record(domain_name,EmailDNSRecord.MX)
    
    servers=[
        MXRecord(
            priority=answer.preference,
            host=HostName(name=str(answer.exchange).rstrip(".")))
        for answer in answers
    ]
    return sorted(servers,key=lambda x:x.priority)
   

def get_mail_server_ipv4(mx_record:MXRecord)->ARecord:
    answers=query_record(mx_record.host.name,EmailDNSRecord.A)

    return ARecord(ips=[IPv4Address(answer.to_text())for answer in answers]) 


def query_record(domain_name:str, record_type: EmailDNSRecord)->list[Rdata]:

    try:
        return dns.resolver.resolve(domain_name, record_type.value)
    except dns.resolver.NoAnswer:
        # No record of this type exists
        print(f"dns resolver No Answer error!!!")
        return []
    except dns.resolver.NXDOMAIN:
        # Domain does not exist
        print(f"domain[{domain_name}] dose not exist!!!")
        return []
    except Exception as e:
        # Any other DNS error
        print(f"DNS error for {domain_name} ({record_type}): {e}")
        return []
    
servers=get_mail_servers("github.com")
print(servers)
ips=[
    ip
    for server in servers
    for ip in get_mail_server_ipv4(server)
]
print(ips)
# print(query_record("gmail.com", EmailDNSRecord.MX)[0].to_text())

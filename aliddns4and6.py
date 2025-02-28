#!/usr/bin/env python3
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from urllib.request import urlopen
import json

class Dnscontroller:

    access_key_id = "需要填写"
    #阿里云的新建账户id
    access_key_secret = "需要填写"
    
    region = "cn-shanghai"
    # 时区
    record_type_ipv4 = "A"
    record_type_ipv6 = "AAAA"

    domain = "1111.xyz"
    # 上面是你的一级域名
    name_ipv4 = ["111"]
    # name_ipv4 = ["二级域名1","二级域名2","二级域名3","二级域名4","二级域名5"]上面是你要修改的域名，我们的比较多，然后呢就以数组的方式去挨个修改
    name_ipv6 = ["111"]
    # name_ipv6 = ["二级域名1","二级域名2","二级域名3","二级域名4","二级域名5"]上面是你要修改的域名，我们的比较多，然后呢就以数组的方式去挨个修改

    def __init__(self):
        self.client = AcsClient(
            self.access_key_id,
            self.access_key_secret,
            self.region
        )

    # 添加新的域名解析记录
    def add(self, DomainName, RR, Type, Value):
        from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
        request = AddDomainRecordRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(Value)
        response = self.client.do_action_with_exception(request)

    # 修改域名解析记录
    def update(self, RecordId, RR, Type, Value):
        from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(RecordId)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(Value)
        response = self.client.do_action_with_exception(request)

    # 获取公网IPv4地址并进行修改
    def Get_IPv4(self):
        ipv4 = json.load(urlopen('http://ip-api.com/json/?fields=query'))['query']
        #ipv4 = urlopen('http://ipv4.icanhazip.com').read().decode().strip()
        print("获取到IPv4地址：%s" % ipv4)

        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(self.domain)

        for item in self.name_ipv4:
            request.set_SubDomain(item + '.' + self.domain)
            response = self.client.do_action_with_exception(request)
            domain_list = json.loads(response)

            if domain_list['TotalCount'] == 0:
                self.add(self.domain, item, self.record_type_ipv4, ipv4)
                print("新建域名：%s,解析成功" % item)

            elif domain_list['TotalCount'] == 1:
                if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv4.strip():
                    self.update(domain_list['DomainRecords']['Record'][0]['RecordId'], item, self.record_type_ipv4, ipv4)
                    print("修改域名：%s,解析成功" % item)
                else:
                    print("IPv4地址没变")

            elif domain_list['TotalCount'] > 1:
                # 仅删除同类型的记录
                for record in domain_list['DomainRecords']['Record']:
                    if record['Type'] == self.record_type_ipv4:
                        delete_request = DeleteDomainRecordRequest()
                        delete_request.set_accept_format('json')
                        delete_request.set_RecordId(record['RecordId'])
                        self.client.do_action_with_exception(delete_request)
                self.add(self.domain, item, self.record_type_ipv4, ipv4)
                print("修改域名解析成功")

    def Get_IPv6(self):
        ipv6 = json.load(urlopen('https://api6.ipify.org?format=json'))['ip']
        #ipv6 = urlopen('https://ipv6.icanhazip.com').read().decode().strip()
        print("获取到IPv6地址：%s" % ipv6)

        request = DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(self.domain)

        for item in self.name_ipv6:
            request.set_SubDomain(item + '.' + self.domain)
            response = self.client.do_action_with_exception(request)
            domain_list = json.loads(response)

            if domain_list['TotalCount'] == 0:
                self.add(self.domain, item, self.record_type_ipv6, ipv6)
                print("新建域名：%s,解析成功" % item)

            elif domain_list['TotalCount'] == 1:
                if domain_list['DomainRecords']['Record'][0]['Value'].strip() != ipv6.strip():
                    self.update(domain_list['DomainRecords']['Record'][0]['RecordId'], item, self.record_type_ipv6, ipv6)
                    print("修改域名：%s,解析成功" % item)
                else:
                    print("IPv6地址没变")

            elif domain_list['TotalCount'] > 1:
                # 仅删除同类型的记录
                for record in domain_list['DomainRecords']['Record']:
                    if record['Type'] == self.record_type_ipv6:
                        delete_request = DeleteDomainRecordRequest()
                        delete_request.set_accept_format('json')
                        delete_request.set_RecordId(record['RecordId'])
                        self.client.do_action_with_exception(delete_request)
                self.add(self.domain, item, self.record_type_ipv6, ipv6)
                print("修改域名解析成功")

if __name__ == "__main__":
    dns = Dnscontroller()
    dns.Get_IPv4()
    dns.Get_IPv6()
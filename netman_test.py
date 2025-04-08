import unittest
from netmiko import ConnectHandler

def connect(device):
    net_connect = ConnectHandler(**device)
    return net_connect

class UnitTest(unittest.TestCase):
    
    def test_loopback_R3(self):
        R3 = {
                'device_type': 'cisco_ios',
                'ip' : '198.51.100.13',
                'username' : 'sarang',
                'password' : 'sarang',
            }
        hdl = connect(R3)
        output = hdl.send_command('show run int lo99')
        if "10.1.3.1 255.255.255.0" not in output : 
            self.fail("IP Address not correct / Not Found")   


    def test_R1_single_area(self):  
        R1 = {
                'device_type': 'cisco_ios',
                'ip' : '198.51.100.11',
                'username' : 'sarang',
                'password' : 'sarang',
            }
        hdl = connect(R1)
        output = hdl.send_command('show run | sec ospf')
        output_lines = output.splitlines()
        seen_area = set()
        for ospf_config in output_lines : 
            if "area" in ospf_config : 
                area = int(ospf_config.split()[-1])
                if area not in seen_area :
                    seen_area.add(area)
                if len(seen_area) > 1 : 
                    self.fail('More than 1 area on R1') 

        
    def test_ping(self):
        R2 = {
                'device_type': 'cisco_ios',
                'ip' : '198.51.100.12',
                'username' : 'sarang',
                'password' : 'sarang',
            }
        hdl = connect(R2)
        output = hdl.send_command('ping 10.1.5.1')
        if "Success rate is 100 percent" not in output:
            self.fail("Ping from R2 Failed")


if __name__ == "__main__":
    unittest.main()
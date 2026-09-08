from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result


# Initialize Nornir
nr = InitNornir(
    inventory = {
        "plugin":"AnsibleInventory",
        "options":{"hostsfile":"../inventory/hosts.yaml"}
    }
)

# Filtering switches 
dist_switches = nr.filter(filter_func=lambda host: host.name in ["DIST-01","DIST-02"])

for host_name, host_obj in dist_switches.inventory.hosts.items():
    host_obj.platform = "ios"

# Define tasks 
def check(task):
    task.run(task=netmiko_send_command,
             command_string = "show ip ospf neighbor",
             name="1. OSPF neighbors")

    task.run(task=netmiko_send_command,
             command_string="show standby brief",
             name = "2.HSRP status")

print("[*] Starting ssh conection with Nornir...")

results = dist_switches.run(task=check)
print_result(results)
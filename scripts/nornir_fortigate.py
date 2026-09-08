from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(
    inventory={
        "plugin": "AnsibleInventory",
        "options":{"hostsfile":"../inventory/hosts.yaml"}
    }
)

fortigate = nr.filter(filter_func=lambda host: host.name=="FW-EDGE")


for host_name, host_obj in fortigate.inventory.hosts.items():
    host_obj.platform = "fortinet"

def fortigate_telemetry(task):
    task.run(
        task=netmiko_send_command,
        command_string="get router info routing-table ospf",
        name="1. OSPF routes verficiation"
    )

    task.run(
        task=netmiko_send_command,
        command_string = "get system session list",
        name = "2. Global stats from NAT"
    )

print("[*] Connecting to FortiGate via SSH... ")
results = fortigate.run(task=fortigate_telemetry)
print_result(results)
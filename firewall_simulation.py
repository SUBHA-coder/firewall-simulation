class Packet:
    def __init__(self, src_ip, dest_ip, src_port, dest_port, protocol):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.src_port = src_port
        self.dest_port = dest_port
        self.protocol = protocol

class Rule:
    def __init__(self, src_ip=None, dest_ip=None, src_port=None, dest_port=None, protocol=None, action='ALLOW'):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.src_port = src_port
        self.dest_port = dest_port
        self.protocol = protocol
        self.action = action

class Firewall:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def inspect_packet(self, packet):
        for rule in self.rules:
            if self.match_rule(packet, rule):
                return rule.action
        return 'BLOCK'

    def match_rule(self, packet, rule):
        return (
            (rule.src_ip is None or packet.src_ip == rule.src_ip) and
            (rule.dest_ip is None or packet.dest_ip == rule.dest_ip) and
            (rule.src_port is None or packet.src_port == rule.src_port) and
            (rule.dest_port is None or packet.dest_port == rule.dest_port) and
            (rule.protocol is None or packet.protocol == rule.protocol)
        )

    def process_packet(self, packet):
        action = self.inspect_packet(packet)
        return action

if __name__ == "__main__":
    # Create a Firewall instance
    firewall = Firewall()

    # Add rules
    firewall.add_rule(Rule(src_ip='192.168.1.1', action='ALLOW'))
    firewall.add_rule(Rule(dest_ip='192.168.1.2', dest_port=80, action='ALLOW'))
    firewall.add_rule(Rule(protocol='TCP', action='BLOCK'))

    # Simulate packets
    packets = [
        Packet('192.168.1.1', '192.168.1.2', 12345, 80, 'TCP'),
        Packet('192.168.1.3', '192.168.1.4', 12345, 80, 'UDP'),
        Packet('192.168.1.1', '192.168.1.2', 12345, 443, 'TCP'),
    ]

    # Process packets
    for packet in packets:
        action = firewall.process_packet(packet)
        print(f'Packet from {packet.src_ip} to {packet.dest_ip} on port {packet.dest_port} with protocol {packet.protocol} is {action}')

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

# Create a Firewall instance
firewall = Firewall()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_rule', methods=['POST'])
def add_rule():
    data = request.json
    rule = Rule(src_ip=data.get('src_ip'), dest_ip=data.get('dest_ip'), src_port=data.get('src_port'),
                dest_port=data.get('dest_port'), protocol=data.get('protocol'), action=data.get('action'))
    firewall.add_rule(rule)
    return jsonify({'status': 'Rule added successfully'})

@app.route('/inspect_packet', methods=['POST'])
def inspect_packet():
    data = request.json
    packet = Packet(src_ip=data['src_ip'], dest_ip=data['dest_ip'], src_port=data['src_port'],
                    dest_port=data['dest_port'], protocol=data['protocol'])
    action = firewall.process_packet(packet)
    return jsonify({'action': action})

if __name__ == '__main__':
    app.run(debug=True)

document.getElementById('ruleForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const ruleData = {
        src_ip: document.getElementById('src_ip').value,
        dest_ip: document.getElementById('dest_ip').value,
        src_port: document.getElementById('src_port').value,
        dest_port: document.getElementById('dest_port').value,
        protocol: document.getElementById('protocol').value,
        action: document.getElementById('action').value
    };

    fetch('/add_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(ruleData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('ruleResult').textContent = data.status;
    });
});

document.getElementById('packetForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const packetData = {
        src_ip: document.getElementById('packet_src_ip').value,
        dest_ip: document.getElementById('packet_dest_ip').value,
        src_port: document.getElementById('packet_src_port').value,
        dest_port: document.getElementById('packet_dest_port').value,
        protocol: document.getElementById('packet_protocol').value
    };

    fetch('/inspect_packet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(packetData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('packetResult').textContent = `Packet action: ${data.action}`;
    });
});

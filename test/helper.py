import pickle
from time import sleep

from pueue.helper.socket import connect_client_socket


def command_factory(state, params={}):
    instruction = {'mode': state}
    for key, value in params.items():
        instruction[key] = value
    return send_command(instruction)


def send_command(command):
    client = connect_client_socket()
    client.send(pickle.dumps(command, -1))
    answer = client.recv(1048576)
    response = pickle.loads(answer)
    client.close()
    return response


def execute_add(command):
    command['mode'] = 'add'
    command['status'] = 'queued'
    command['returncode'] = ''
    command['path'] = '/tmp'
    send_command(command)


def get_status():
    status = send_command({'mode': 'status'})
    return status


def wait_for_process(key):
    status = get_status()
    while (key not in status['data']) or (status['data'][key]['status'] != 'done'):
        sleep(1)
        status = get_status()
        print(status)
    return status

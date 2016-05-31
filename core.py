import time
from docker import Client

from .rabbit_inst_create import *


cli = Client(base_url='unix://var/run/docker.sock')
app_path = '/home/lancer/PycharmProjects/SampleRabbit'  # - should be cmd argument (where is app)
data_path = '/home/lancer/PycharmProjects/Jungler/Logs' # - cmd arg - where to store logs...
container_list = {}


class Jungler(object):
    def __init__(self, cli, config, testbunch):
        self.cli = cli
        self.config = config
        self.testbunch = testbunch

    def create_containers(self, backends):
        cont = create_discovery(1)
        container_list['discovery{0}'.format(1)] = cont.get('Id')

        for x in range(0, backends):
            cont = create_backend(self.cli, x)
            container_list['backend{0}'.format(x)] = cont.get('Id')

        cont = create_frontend(self.cli, 1)
        container_list['frontend{0}'.format(1)] = cont.get('Id')

        cont = create_client(self.cli, 1)
        container_list['client{0}'.format(1)] = cont.get('Id')


    def start_containers(self):
        for name, contid in container_list.items():
            response = self.cli.start(container=contid)


    def stop_containers(self):
        for name, contid in container_list.items():
            response = self.cli.stop(container=contid, timeout=1)

    def remove_containers(self):
        for name, contid in container_list.items():
            response = self.cli.remove_container(container=contid)


# ----------------------------------------------------------------------------------------------------------------------
def delay_simple(cont_id, delay, period):
    cli.exec_create(cont_id, cmd='tc qdisc add dev eth0 root netem delay {0}ms {1}ms'.format(delay, period))


def delay_distr(cont_list, delay, period, distribution):
    for name in cont_list:
        execid = cli.exec_create(container_list[name], cmd='tc qdisc add dev eth0 root netem delay {0}ms {1}ms distribution {2}'.format(
            delay, period, distribution))
        response = cli.exec_start(exec_id=execid)
        print(response)


def loss(cont_list, percent):
    for name in cont_list:
        execid = cli.exec_create(container_list[name], cmd='tc qdisc del dev eth0 root netem loss {0}%'.format(percent))
        cli.exec_start(exec_id=execid)

def duplicate(cont_list, percent):
    for name in cont_list:
        execid = cli.exec_create(container_list[name], cmd='tc qdisc change dev eth0 root netem duplicate {0}%'.format(percent))
        cli.exec_start(exec_id=execid)

def restore(cont_list):
    for name in cont_list:
        execid = cli.exec_create(container_list[name], cmd='tc qdisc del dev eth0 root')
        cli.exec_start(exec_id=execid)

# create_containers(1)
# start_containers()
#
# time.sleep(20)
# delay_distr(['backend0', 'frontend1'], 2000, 50, 'normal')
# time.sleep(30)
# loss(['client1', 'frontend1'], 90)
# time.sleep(30)
#
# stop_containers()
# remove_containers()
#
#
# # time.sleep(20)
# # restore(['backend0', 'frontend1', 'client1'])
#
#
# # stop_containers()

"""
docker run --name="backend2" -v /home/lancer/PycharmProjects/Jungler:/mnt/app /home/lancer/PycharmProjects/Jungler/Logs:/mnt/dat  -w="/mnt/app" -itd "mephidude/basenode:latest"  python3 backend.py
"""
import time
from docker import Client

from CreateBindings import create_backend, create_frontend, create_discovery, create_client


class Jungler(object):
    def __init__(self, _app_path, _data_path, _docker_ip, _backends, _tls_config):
        self.cli = Client(base_url='https://'+_docker_ip, tls=_tls_config)
        self.list_containers = {}
        self.app_path = _app_path
        self.data_path = _data_path
        self.backends = _backends
        self.create_containers()

    def create_containers(self):
        cont_d = create_discovery(self.cli, 0, self.app_path, self.data_path)
        self.list_containers['discovery{0}'.format(1)] = cont_d.get('Id')

        for x in range(0, self.backends):
            cont = create_backend(self.cli, x, self.app_path, self.data_path)
            self.list_containers['backend{0}'.format(x)] = cont.get('Id')

        cont_f = create_frontend(self.cli, 0, self.app_path, self.data_path)
        self.list_containers['frontend{0}'.format(0)] = cont_f.get('Id')

        cont_c = create_client(self.cli, 0, self.app_path, self.data_path)
        self.list_containers['client{0}'.format(0)] = cont_c.get('Id')

    def start_containers_all(self):
        for name, contid in self.list_containers.items():
            response = self.cli.start(container=contid)

    def start_container(self, contname):
        response = self.cli.start(container=contname)

    def stop_containers_all(self):
        for name, contid in self.list_containers.items():
            response = self.cli.stop(container=contid, timeout=2)

    def stop_container(self, contname):
        response = self.cli.stop(container=contname, timeout=2)

    def remove_containers_all(self):
        for name, contid in self.list_containers.items():
            response = self.cli.remove_container(container=contid)
    # ------------------------------------------------------------------------------------------------------------------

    def exec_tc(self, affected, opts):
        """
        Execute tc with parms in opts
        :param affected: string for further split
        :param opts: string for tc call
        """
        affected_list = affected.split(' ')
        for name in affected_list:
            execid = self.cli.exec_create(self.list_containers[name],
                                          cmd='tc qdisc add dev eth0 root netem ' + opts)
            response = self.cli.exec_start(exec_id=execid)


    def recover(self, affected_list):
        for name in affected_list:
            execid = self.cli.exec_create(self.list_containers[name],
                                          cmd='tc qdisc del dev eth0 root netem')
            response = self.cli.exec_start(exec_id=execid)


    def delay_distr(self, affected_list, delay, period, distribution):
        for name in affected_list:
            execid = self.cli.exec_create(self.list_containers[name],
                                          cmd='tc qdisc add dev eth0 root netem delay {0}ms {1}ms distribution {2}'.format(
                                              delay, period, distribution))
            response = self.cli.exec_start(exec_id=execid)


    def loss(self, affected_list, percent):
        for name in affected_list:
            execid = self.cli.exec_create(self.list_containers[name],
                                          cmd='tc qdisc add dev eth0 root netem loss {0}%'.format(
                                              percent))
            self.cli.exec_start(exec_id=execid)


    def down(self, affected_list):
        for name in affected_list:
            execid = self.cli.exec_create(self.list_containers[name],
                                          cmd='tc qdisc add dev eth0 root netem loss 100%')
            self.cli.exec_start(exec_id=execid)


    def duplicate(self, affected_list, percent):
        for name in affected_list:
            execid = self.cli.exec_create(self.list_containers[name],
                                          cmd='tc qdisc change dev eth0 root netem duplicate {0}%'.format(
                                              percent))
            self.cli.exec_start(exec_id=execid)


    def restore_all(self):
        for name, contid in self.list_containers.items():
            execid = self.cli.exec_create(contid,
                                          cmd='tc qdisc del dev eth0 root')
            self.cli.exec_start(exec_id=execid)


    def restore(self, cont_list):
        for name in cont_list:
            execid = self.cli.exec_create(self.list_containers[name],
                                          cmd='tc qdisc del dev eth0 root')
            self.cli.exec_start(exec_id=execid)


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

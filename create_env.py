import time
from docker import Client


cli = Client(base_url='unix://var/run/docker.sock')
app_path = '/home/lancer/PycharmProjects/SampleRabbit'  # - should be cmd argument (where is app)
data_path = '/home/lancer/PycharmProjects/Jungler/Logs' # - cmd arg - where to store logs...
container_list = {}


def create_discovery(num):
    container_id = cli.create_container(
        image='mephidude/basenode:latest',
        command='python3 discovery-node.py',
        # command='/bin/bash',
        volumes=['/mnt/app', '/mnt/dat'],
        host_config=cli.create_host_config(binds={
            app_path: {
                'bind': '/mnt/app',
                'mode': 'ro',
            },
            data_path: {
                'bind': '/mnt/dat',
                'mode': 'rw',
            }
        }, cap_add=["NET_ADMIN", "SYS_ADMIN"]),
        working_dir='/mnt/app',
        name='discovery{0}'.format(num),
        tty=True,
        detach=True
    )
    return container_id


def create_frontend(num):
    container_id = cli.create_container(
        image='mephidude/basenode:latest',
        command='python3 frontend-node.py',
        # command='/bin/bash',
        volumes=['/mnt/app', '/mnt/dat'],
        host_config=cli.create_host_config(binds={
            app_path: {
                'bind': '/mnt/app',
                'mode': 'ro',
            },
            data_path: {
                'bind': '/mnt/dat',
                'mode': 'rw',
            }
        }, cap_add=["NET_ADMIN", "SYS_ADMIN"]),
        working_dir='/mnt/app',
        name='frontend{0}'.format(num),
        tty=True,
        detach=True
        # entrypoint='python3 frontend-node.py'  # - discovery starts first and stop
    )
    return container_id


def create_backend(num):
    container_id = cli.create_container(
        image='mephidude/basenode:latest',
        command='python3 backend-node.py',
        # command='/bin/bash',
        volumes=['/mnt/app', '/mnt/dat'],
        host_config=cli.create_host_config(binds={
            app_path: {
                'bind': '/mnt/app',
                'mode': 'ro',
            },
            data_path: {
                'bind': '/mnt/dat',
                'mode': 'rw',
            }
        },cap_add=["NET_ADMIN", "SYS_ADMIN"]),
        working_dir='/mnt/app',
        name='backend{0}'.format(num),
        tty=True,
        detach=True
    )
    return container_id


def create_client(num):
    container_id = cli.create_container(
        image='mephidude/basenode:latest',
        command='python3 client.py',
        # command='/bin/bash',
        volumes=['/mnt/app', '/mnt/dat'],
        host_config=cli.create_host_config(binds={
            app_path: {
                'bind': '/mnt/app',
                'mode': 'ro',
            },
            data_path: {
                'bind': '/mnt/dat',
                'mode': 'rw',
            }
        }, cap_add=["NET_ADMIN", "SYS_ADMIN"]),
        working_dir='/mnt/app',
        name='client{0}'.format(num),
        tty=True,
        detach=True
    )
    return container_id


def create_containers(backends):
    """
    Create containers (base image + hardcoded config)
    :param s: list
    """
    cont = create_discovery(1)
    container_list['discovery{0}'.format(1)] = cont.get('Id')

    for x in range(0, backends):
        cont = create_backend(x)
        container_list['backend{0}'.format(x)] = cont.get('Id')

    cont = create_frontend(1)
    container_list['frontend{0}'.format(1)] = cont.get('Id')

    cont = create_client(1)
    container_list['client{0}'.format(1)] = cont.get('Id')


def start_containers():
    for name, contid in container_list.items():
        response = cli.start(container=contid)


def stop_containers():
    for name, contid in container_list.items():
        response = cli.stop(container=contid, timeout=1)

def remove_containers():
    for name, contid in container_list.items():
        response = cli.remove_container(container=contid)


def remove_containers():
    for name, contid in container_list.items():
        response = cli.remove_container(container=contid)


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

create_containers(1)
start_containers()

time.sleep(20)
delay_distr(['backend0', 'frontend1'], 2000, 50, 'normal')
time.sleep(30)
loss(['client1', 'frontend1'], 90)
time.sleep(30)

stop_containers()
remove_containers()


# time.sleep(20)
# restore(['backend0', 'frontend1', 'client1'])


# stop_containers()

"""
docker run --name="backend2" -v /home/lancer/PycharmProjects/Jungler:/mnt/app /home/lancer/PycharmProjects/Jungler/Logs:/mnt/dat  -w="/mnt/app" -itd "mephidude/basenode:latest"  python3 backend.py
"""
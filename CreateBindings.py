def create_discovery(cli, num, app_path, data_path):
    container_id = cli.create_container(
        image='basenode:latest',
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


def create_frontend(cli, num, app_path, data_path):
    container_id = cli.create_container(
        image='basenode:latest',
        # command='python3 frontend-single.py',       #####################
        command='python3 frontend-threadfork.py',       #####################
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


def create_backend(cli, num, app_path, data_path):
    container_id = cli.create_container(
        image='basenode:latest',
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


def create_client(cli, num, app_path, data_path):
    container_id = cli.create_container(
        image='basenode:latest',
        command='python3 parallel_client.py',  ####################
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
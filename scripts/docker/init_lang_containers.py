import docker
import os

PYTHON_IMG = "pythonlang_docker"


def main():
    client = docker.from_env()

    client = docker.APIClient()
    container = client.create_container(
        PYTHON_IMG,
        stdin_open=True,
    )

    code = b"""
# PYTHON: authogenerated runtime code
import re
import traceback

# context
# define some context here (e.g. types for arguments)
# initial code
# function should have name 'main'
def main(arg1: int, arg2: str, *args, **kwargs):
    pass


__RESULT = {
    'errors': [],
    'passed': 0,
    'failed': 0
}

# assertions

try:
    assert True
    assert False
    __RESULT['done'] += 1
except AssertionError:
    error = str(traceback.format_exc())
    error = re.sub(r'".*?"', '***', error)

    __RESULT['failed'] += 1
    __RESULT['errors'].append(error)



    """

    sock = client.attach_socket(container, params={"stdin": 1, "stdout": 1, "stderr": 1, "stream": 1})
    client.start(container)
    sock._sock.send(code)
    sock._sock.close()
    sock.close()

    status = client.wait(container)
    status_code = status["StatusCode"]
    stdout = client.logs(container, stderr=False).decode()
    stderr = client.logs(container, stdout=False).decode()

    client.remove_container(container)

    import json

    print(json.loads(stdout))

    print("Exit: {}".format(status_code))
    print("log stdout: {}".format(stdout))
    print("log stderr: {}".format(stderr))

    # print(client.images.get(PYTHON_IMG))

    # for img in client.images.list():
    #     print(img)

    # container = client.containers.run(PYTHON_IMG, detach=True, stdin_open=True)

    # # container = client.containers.create(PYTHON_IMG, stdin_open=True)
    # stdin_data = 'some data to send to stdin'

    # socket = container.attach_socket(params={'stdin': 1, 'stream': 1})
    # os.write(socket.fileno(), stdin_data.encode())
    # socket.close()

    # # res = client

    # exit_code = container.wait()

    # containers = client.containers.list()

    # for cnt in containers:
    #     print(cnt.attrs['Config']['Image'])


if __name__ == "__main__":
    main()

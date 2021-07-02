import os
import shutil


def test_docker_compose(docker_compose, retrying_requests):
    assert retrying_requests.get(f"http://{docker_compose['server']}:8000").ok


def test_docker_compose_cm_default(docker_compose_cm, retrying_requests):
    with docker_compose_cm() as docker_compose:
        assert retrying_requests.get(f"http://{docker_compose['server']}:8000").ok


def test_docker_compose_cm_with_yml(tmpdir, docker_compose_cm, retrying_requests):
    docker_compose_yml = tmpdir / "docker-compose.yml"
    shutil.copy(os.path.join(os.path.dirname(__file__), "docker-compose.yml"), docker_compose_yml)

    with docker_compose_cm(docker_compose_yml) as docker_compose:
        assert retrying_requests.get(f"http://{docker_compose['server']}:8000").ok


def test_docker_compose_cm_with_network(request, docker_compose_cm, retrying_requests):
    with docker_compose_cm(
        docker_compose_yml=os.path.join(
            os.path.dirname(request.fspath), "networked-docker-compose.yml"
        ),
        network_name="network",
    ) as docker_compose:
        assert retrying_requests.get(f"http://{docker_compose['server']}:8000").ok


def test_docker_compose_cm_with_context(docker_context_cm, docker_compose_cm, retrying_requests):
    with docker_context_cm(name="custom_context") as context, docker_compose_cm(
        docker_context=context
    ) as docker_compose:
        assert retrying_requests.get(f"http://{docker_compose['server']}:8000").ok

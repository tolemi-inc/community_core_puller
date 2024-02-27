all:build-image

build-image:
	podman manifest rm community-core-puller:latest
	podman build --jobs=2 --platform=linux/amd64,linux/arm64 --manifest community-core-puller:latest .
# Docker

## Key ideas

- An **image** is a read-only template, for example `ubuntu:24.04`.
- A **container** is a running (or stopped) instance of an image, with its own writable layer, for example `lab`.
- A **bind mount** (`-v host:container`) shows a host folder inside the container. Same files, not a copy.
- A container lives as long as its main process. When `bash` exits, the container stops.

## Q&A

### What does each part of `docker run -it --name lab -v ~/…/sre-lab:/lab ubuntu:24.04 bash` do?

| Part | Meaning |
|---|---|
| `docker run` | Create a **new** container from an image and start it. Pulls the image first if missing. |
| `-i` | Keep stdin open, so the container reads what I type. |
| `-t` | Give it a terminal (TTY), so I get a proper prompt. `-it` = interactive shell. |
| `--name lab` | Name the container. Otherwise Docker picks a random one. |
| `-v host:container` | Bind mount a Mac folder into the container. |
| `ubuntu:24.04` | Image as `name:tag`. The tag pins the version. |
| `bash` | The process the container runs. |

### What survives what?

| Action | Files in `/lab` | Packages installed with `apt` |
|---|---|---|
| `exit` (container stops) | ✅ kept | ✅ kept |
| `docker rm lab` | ✅ kept (they live on the Mac) | ❌ gone |
| `--rm` flag on `docker run` | ✅ kept | ❌ gone on exit |

→ That's why my `lab` container has **no** `--rm`.

### Why did `docker start` fail with "requires at least 1 argument"?
It needs to know **which** container. In the usage line `docker start [OPTIONS] CONTAINER`, the parts in `[brackets]` are optional and the rest are required.
Get back into my lab with `docker start -ai lab` (`-a` attach output, `-i` attach input).

### What does the prompt `root@0415ed695eb8:/#` mean?
- `root`: I'm the root user inside the container (no `sudo` needed).
- `0415ed695eb8`: the hostname, which is the container's short ID (matches `docker ps`).
- `/`: current directory.
- `#`: root's prompt symbol (`$` for a normal user).

### What does "Unable to find image locally … Pulling" mean?
The image wasn't on my machine, so `docker run` downloaded it from Docker Hub first. The next run starts instantly.

## Commands to know

| Command | Does |
|---|---|
| `docker ps` | Running containers |
| `docker ps -a` | All containers, stopped ones too |
| `docker images` | Images on this machine |
| `docker start -ai lab` | Restart my lab and attach to it |
| `docker rm lab` | Delete the container |
| `docker rmi <image>` | Delete an image |

## Common mistakes

- Running `docker run --name lab …` a second time → **"name already in use"**. Use `docker start -ai lab`.
- Forgetting the container name: `docker start` on its own fails.
- Committing from inside the container: git isn't installed there. Commit from the Mac.

## Self-test

1. What's the difference between an image and a container? Which is `ubuntu:24.04` and which is `lab`?
2. I ran `exit`. How do I get back in, and is my installed `strace` still there?
3. What happens to files in `/lab` if I run `docker rm lab`? To packages I installed?
4. Why does my lab container not use `--rm`?

## References

- [docker run reference](https://docs.docker.com/reference/cli/docker/container/run/)
- [docker start reference](https://docs.docker.com/reference/cli/docker/container/start/)
- [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
- [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)

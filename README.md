# SpaceX-Telegram

> Bot follow Official SpaceX youtube channel and sends updates to telegram channel

![](https://github.com/alex-bormotov/spacex-telegram/workflows/Github-CICD/badge.svg)   [![Codacy Badge](https://app.codacy.com/project/badge/Grade/138eb3776f71492ebcb77edc3d37a5d7)](https://www.codacy.com/manual/alex-bormotov/spacex-telegram?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alex-bormotov/spacex-telegram&amp;utm_campaign=Badge_Grade)

## Install (Ubuntu + Docker)

```bash
git clone https://github.com/alex-bormotov/spacex-telegram
```

```bash
cd spacex-telegram
```

```bash
cp config/config.json.sample config/config.json
```

> Edit config/config.json

```bash
sudo chmod +x docker_ubuntu_install.sh && sudo ./docker_ubuntu_install.sh
```

```bash
sudo docker run -d --rm --mount src=`pwd`/config,target=/spacex-telegram/config,type=bind skilfulll1/spacex-telegram:latest
```
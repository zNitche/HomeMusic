# HomeMusic
### Easy to use minimalist music downloader

---
### Install
1. Clone this repo.
2. Generate `.env` config file and change config values (`FILES_PATH` and `MYSQL_ROOT_PASSWORD`).
```
python3 generate_dotenv.py
```
3. Run docker container.
```
sudo docker compose up -d
```
4. Bash into container.
```
sudo docker container exec -it home_music_web_app bash
```
5. Create users accounts using `users_manager.py`.

### Dev
1. Change `MYSQL_SERVER_HOST` in `.env` to `127.0.0.1`
2. Change `REDIS_SERVER_ADDRESS` in `.env` to `127.0.0.1`
3. Run DEV docker-compose.
```
sudo docker compose -f docker-compose-dev.yml up
```

### Usage
1. Enter yt link/links (if many seperate them with `|`)
2. Press `Get!` button.
3. Wait until process to finish (or cancel it)
4. Press `Download` button to download `.zip` file containing your music

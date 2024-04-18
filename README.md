# HomeMusic
### Easy to use minimalist music downloader

---

## App Setup:
### Install
1. Clone this repo.
2. Generate `.env` config file and change config values (`FILES_PATH`).
```
python3 generate_dotenv.py
```
3. Run docker container.
```
sudo docker compose -f docker-compose.yml up -d
```

### Dev
1. Change `REDIS_SERVER_ADDRESS` in `.env` to `127.0.0.1`
2. Run DEV docker-compose.
```
sudo docker compose -f docker-compose-dev.yml up
```

3. If needed run database migrations
```
python3 migrate.py
```

## Create accounts
1. Bash into container.
```
sudo docker container exec -it home_music_web_app bash
```
2. Create users accounts using `users_manager.py`.

## Usage
1. Enter yt link/links (if many seperate them with `|`)
2. Press `Get!` button.
3. Wait until process to finish (or cancel it)
4. Press `Download` button to download `.zip` file containing your music

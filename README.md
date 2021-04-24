# HomeMusic
### Easy to use minimalist music downloader

---
### Install
1. Clone this repo
2. Create users accounts using `manage_users.py`
3. Build docker image `sudo docker build -t homemusic .`
4. Run docker container
```
sudo docker run --name=homemusic -d -v <path_to_files_storage> -p 8080:8080 homemusic
```
5. Make docker container restart after reboot `sudo docker update --restart unless-stopped homemusic`

### Usage
1. Login
2. Enter yt link/links (if many seperate them with `|`)
3. Press `Get!` button, when whole process will be finished you will be prompted to choose where the `.zip` file will be saved to
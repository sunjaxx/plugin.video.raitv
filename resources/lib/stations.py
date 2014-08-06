import urllib2
import json
import StorageServer

def get_tv_stations():
    url = "http://www.rai.tv/dl/RaiTV/iphone/android/smartphone/advertising_config.html"
    response = json.load(urllib2.urlopen(url))
    channels = response["Channels"]
    
    for channel in channels:
        channel["icon"] = channel["icon"].replace(".png", "-big.png")
        
        # Force replay availability for Rai Gulp and Rai YoYo
        if channel["name"] in ("Rai Gulp", "Rai Yoyo"):
            channel["hasReplay"] = "YES"
            
        # Fix tag for Rai Gulp
        if channel["name"] == "Rai Gulp":
            channel["tag"] = "RaiGulp"
    
    return channels
    
def get_radio_station():
    url = "http://www.rai.tv/dl/RadioRai/config_json.html"
    response = json.load(urllib2.urlopen(url))
    return response["canali"]

# Cache channels for 1 hour
cache = StorageServer.StorageServer("plugin.video.raitv", 1) # (Your plugin name, Cache time in hours)

tv_stations = cache.cacheFunction(get_tv_stations)
radio_stations = cache.cacheFunction(get_radio_station)

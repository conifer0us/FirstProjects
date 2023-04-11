import json
import requests
import sounddevice as sd
from scipy.io import wavfile
import os
from pynput.keyboard import Key, Controller
import time 
import asyncio
from pydub import AudioSegment

async def main():
    playlistID = None # Replace with Your Playlist ID
    CLIENT_ID = None
    CLIENT_SECRET = None
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    headers =  {"Accept": "application/json", "Content-Type": "application/json"}
    song_list = []
    offset = 0
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    headers["Authorization"] = "Bearer " + auth_response.json()['access_token']
    while True:
        playlist_api_query = requests.get("https://api.spotify.com/v1/playlists/"+playlistID+"/tracks?offset="+str(offset)+"&limit=100", headers=headers)
        api_json = json.loads(playlist_api_query.text)
        temp_song_list = []
        for x in api_json['items']:
            temp_song_list.append([replaceString(x["track"]["name"]), x["track"]["artists"][0]["name"], x["track"]["duration_ms"] + 100])
        if len(temp_song_list) > 0:
            song_list += temp_song_list
            offset += 100
        else: 
            break
    # Songs now formatted in song_list in lists with the data as follows ["Song Name", "Artist Name", "Duration (+0.1 seconds)"]
    print("Songs Selected: " + str(len(song_list)))
    print("Once the spotify window opens, you will have 8 seconds to select the song at the top of the list. Do not play it, only select it.")
    time.sleep(2)
    os.startfile("spotify.exe")
    time.sleep(8)
    for song_data in song_list:
        keyboard_object = Controller()
        if song_data[0] + "-" + song_data[1] + ".mp3" in os.listdir("./"+playlistID):
            keyboard_object.press(Key.down)
            time.sleep(0.03)
            keyboard_object.release(Key.down)
            time.sleep(0.5)
            continue
        coroutine = recordComputerAudio(song_data, playlistID)
        keyboard_object.press(Key.enter)
        time.sleep(0.03)
        keyboard_object.release(Key.enter)
        await coroutine
        if song_list.index(song_data) < len(song_list) - 1:
            time.sleep(0.2)
            keyboard_object.press(Key.enter)
            time.sleep(0.03)
            keyboard_object.release(Key.enter)
            time.sleep(0.5)
            keyboard_object.press(Key.down)
            time.sleep(0.03)
            keyboard_object.release(Key.down)
            time.sleep(0.5)
            keyboard_object.press(Key.space)
            time.sleep(0.03)
            keyboard_object.release(Key.space)
            time.sleep(0.5)

async def recordComputerAudio(songdata, playlistID):
    fs = 48000  # Record at 48000 samples per second
    seconds = songdata[2] / 1000
    if not os.path.exists("./"+playlistID):
        os.makedirs("./"+playlistID)
    # filename = os.getcwd() + "\\"+playlistID+"\\" + songdata[0] + "-" + songdata[1] + ".wav"
    filename = songdata[0] + "-" + songdata[1] + ".wav"

    print('Recording '+songdata[0])

    sd.default.device[0] = 2
    recording = sd.rec(frames=int(fs * seconds), samplerate=fs, blocking=True, channels=1)
    sd.wait()
    wavfile.write(filename, fs, recording)

    print(filename)
    song = AudioSegment.from_wav(filename)
    song += 20
    mp3filename = filename.replace(".wav", ".mp3")
    song.export("./" + playlistID + "/" + mp3filename, "mp3")
    os.remove(filename)

    return True

def replaceString(input): 
    unacceptable_characters = "/\\!@#$%^&*()_-.|<>?,\""
    for char in unacceptable_characters:
        input = input.replace(char, "")
    return input

if __name__ == "__main__":
    asyncio.run(main())
from MusicLibrary.kuGouMusicApi import KuGouMusicApi, Platform, KugouProcessEnv

kugou = KuGouMusicApi(KugouProcessEnv(platform=Platform.LITE))
# response = kugou.top_song()
response = kugou.album_detail(id='10729818')
print(response)

from MusicLibrary.neteaseCloudMusicApi import NeteaseCloudMusicApi, NcmProcessEnv

ncm = NeteaseCloudMusicApi(None)
response = ncm.request('/top/song', """{"id": "96"}""")
print(response)
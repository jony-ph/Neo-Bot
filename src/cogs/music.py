import discord
import youtube_dl
import shutil
import os
import re

from discord.ext import commands
from urllib import parse, request

class Music(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.play_list = {}

        self.MUSIC_FOLDER = './assets/music/'
        self.QUEUE_PATH = './assets/music/queue/'
        self.SONG_ONLINE = './assets/music/song.mp3'


    def download_video(self, output, args):

        ''' Downloand music and settings '''

        ydl_options = {

            'format' : 'bestaudio/best',
            'keepvideo' : False,
            'quiet' : True, 
            'outtmpl' : output,
            'postprocessors': [{

                'key': 'FFmpegExtractAudio',
                'preferredcodec' : 'mp3',
                'preferredquality' : '192',

            }]

        }

        query_str = parse.urlencode({'search_query': args})
        html_content = request.urlopen('http://www.youtube.com/results?' + query_str)
        search_results = re.findall(r'/watch\?v=(.{11})', html_content.read().decode())
        url = 'https://www.youtube.com/watch?v=' + search_results[0]
                
        with youtube_dl.YoutubeDL(ydl_options) as ydl:

            print("Descargando archivo...")
            ydl.download([url])


    def check_list(self, VOICE_CLIENT):

        ''' Prove for songs in the queue '''

        if os.path.isdir(self.QUEUE_PATH):

            size_list = len(os.listdir(self.QUEUE_PATH))
            active_song = size_list - 1 

            try:

                first_song = os.listdir(self.QUEUE_PATH)[0] 
            except:

                print("Ya no hay más canciones por reproducir!")
                self.play_list.clear()
                return

            song_location = self.QUEUE_PATH + first_song
 
            if size_list != 0:

                print("Canción lista, se reproducirá en breve")
                print(f"Canciones en la lista: {active_song}")

                if os.path.isfile(self.SONG_ONLINE):

                    os.remove(self.SONG_ONLINE)
                    shutil.move(song_location, self.MUSIC_FOLDER)

                    for file in os.listdir(self.MUSIC_FOLDER):

                        if file.endswith('.mp3'):

                            os.rename(self.MUSIC_FOLDER + file, self.SONG_ONLINE)

                    self.ffmpeg_options(VOICE_CLIENT)

                else:

                    self.play_list.clear()
                    return

            else:

                self.play_list.clear()
                print("No se agregaron cancione a la lista de reproducción")


    def ffmpeg_options(self, VOICE_CLIENT):

        ''' Sound settings '''

        ffmpeg_options = { 'options' : '-vn'}

        VOICE_CLIENT.play(discord.FFmpegPCMAudio(self.SONG_ONLINE, **ffmpeg_options), after=lambda e: self.check_list(VOICE_CLIENT)) 
        VOICE_CLIENT.source = discord.PCMVolumeTransformer(VOICE_CLIENT.source, volume=1)


    @commands.command(pass_context = True, name = 'play', aliases=['p', 'pla', 'PLAY', 'PLA'], 
                      help = 'Reproduce una canción de YouTube')
    async def play(self, ctx, *, args):

        ''' Play music or add to queue '''

        AUTHOR_CONNECTION = ctx.message.author.voice
        if AUTHOR_CONNECTION: 

            CHANNEL = ctx.message.author.voice.channel
            if not ctx.message.guild.voice_client: 

                await CHANNEL.connect()

            VOICE_CLIENT = ctx.message.guild.voice_client
            if VOICE_CLIENT and not VOICE_CLIENT.is_playing():

                try:

                    if os.path.isfile(self.SONG_ONLINE): 

                        os.remove(self.SONG_ONLINE) 
                        self.play_list.clear() 
                        print("Removiendo archivo...")

                    if os.path.isdir(self.QUEUE_PATH):

                        print("Removiendo carpeta...")
                        shutil.rmtree(self.QUEUE_PATH)

                except PermissionError:

                    print("Se ha intentado eliminar un archivo, pero se encuentra en reproducción")
                    await ctx.send("Error, la canción aún se está reproduciendo")
                    return

                await ctx.send("Todo listo!")

                PLAY_PATH = './assets/music/%(title)s.%(ext)s'
                self.download_video(PLAY_PATH, args)

                for file in os.listdir(self.MUSIC_FOLDER):

                    if file.endswith('.mp3'):

                        name_file = file

                        print(f"Renombrando archivo: {file}")
                        os.rename(self.MUSIC_FOLDER + file, self.SONG_ONLINE)

                self.ffmpeg_options(VOICE_CLIENT)

                print(f"Reproduciendo: {name_file}")
                await ctx.send(f"Reproduciendo: {name_file[:-4]}")

            else:

                if not os.path.isdir(self.QUEUE_PATH):

                    os.mkdir(self.QUEUE_PATH)
                    

                list_num = len(os.listdir(self.QUEUE_PATH))
                list_num += 1

                add_list = True

                while add_list:

                    if list_num is self.play_list:

                        list_num += 1
                    
                    else:

                        add_list = False
                        self.play_list[list_num] = list_num

                LIST_PATH = self.QUEUE_PATH + f'/song: {list_num}.%(ext)s'
                self.download_video(LIST_PATH, args)
                
                print("Se añadió una nueva canción")
                await ctx.send("Se añadió una nueva canción a la lista de reproducción: " + str(list_num))

        else:

            await ctx.send("No estás conectado a un canal de voz!")

def setup(bot):

    bot.add_cog(Music(bot))
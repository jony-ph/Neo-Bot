import discord
import requests
import re 
import os 

from discord.ext import commands
from urllib import parse, request
from googlesearch import search
from bs4 import BeautifulSoup
from PIL import Image

class Search(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.images_selected = []


    @commands.command(pass_context = True, name = 'y!', help = 'Hace búsquedas de videos en YouTube')
    async def youTube(self, ctx, *, arg):

        query_str = parse.urlencode({'search_query': arg})
        html_content = request.urlopen('http://www.youtube.com/results?' + query_str)
        search_results = re.findall(r'/watch\?v=(.{11})', html_content.read().decode())

        url = 'https://www.youtube.com/watch?v=' + search_results[0]

        await ctx.send(url)

    @commands.command(pass_context = True, name = 'g!', help = 'Hace búsquedas en Google')
    async def google(self, ctx, *, arg):

        ''' Google search '''

        for i in search(arg, start=0, stop=3, pause=2):

            await ctx.send(i)

    @commands.command(pass_context = True, name = 'img', help = 'Buscar imágenes en Google')
    async def images_google(self, ctx, *, arg):

        ''' Web scraping to Google images '''

        GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
        IMAGES_FOLDER = './assets/images'

        def save_images():

            ''' Save images '''

            if not os.path.exists(IMAGES_FOLDER):

                os.mkdir(IMAGES_FOLDER)
            
            download_images()
            

        def download_images():

            ''' Download and rename images '''

            data = arg
            url = GOOGLE_IMAGE + 'q=' + data
            n_images = 5
            # Request to Google and 
            response = requests.get(url)
            html = response.text
            # Extract the img attribute
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.find_all('img', {'class':'t0fcAb'}, limit=n_images)

            # Search and extract the path of the results
            image_links = []
            for res in results:

                try:

                    link = res['src']
                    image_links.append(link)

                except KeyError:

                    continue

            print('Descargando imágenes...')

            # Rename images
            for i, link in enumerate(image_links):

                response = requests.get(link)
                image_name = IMAGES_FOLDER + '/' + data + str(i + 1) + '.jpg'

                with open(image_name, 'wb') as fh:

                    fh.write(response.content)

            print('Hecho')

        def resize_images():

            ''' Edit image size '''

            # Resize and stored images 
            for image in os.listdir(IMAGES_FOLDER):

                if image.endswith('.jpg'):
        
                    img = Image.open(IMAGES_FOLDER + '/' + image)
                    width, height = img.size
                    width, height = int(width * 1.3), int(height * 1.3)
                    img = img.resize((width, height))
                    img.save(IMAGES_FOLDER + '/' + image)

                    self.images_selected.append(image)

            print("Imagen redimensionada")

        def remove_folder_images():

            ''' Delete files and folder  '''

            if os.path.exists(IMAGES_FOLDER):

                if os.listdir(IMAGES_FOLDER):

                     for file in os.listdir(IMAGES_FOLDER):

                        os.remove(IMAGES_FOLDER + '/' + file)

                os.rmdir(IMAGES_FOLDER)

            print("Eliminando imágenes...")


        save_images()
        resize_images()

        # Send the images one by one
        for image in self.images_selected:

            await ctx.send(file = discord.File( IMAGES_FOLDER + '/' + image ))

        remove_folder_images()


def setup(bot):

    ''' Searches setup '''

    bot.add_cog(Search(bot))
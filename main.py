import telebot
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOKEN = '6805111873:AAECH20eYq1ZpKdLV2GB2vEdDGCTMCYtwhM'
YOUTUBE_API_KEY = 'AIzaSyDVL0BAXxSU9PoMVt3_TcBHCC11H5RitBs'
bot = telebot.TeleBot(TOKEN)

print("Бот запущен, переходи по ссылке: https://t.me/musicify_from_youtube_bot")

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Привет! Введите название песни или исполнителя для поиска музыки на YouTube.')

@bot.message_handler(func=lambda message: True)
def handle_search_music(message):
    search_query = message.text
    music_url = search_music(search_query)
    
    if music_url:
        bot.reply_to(message, f'Вот ссылка для прослушивания музыки: {music_url}')
    else:
        bot.reply_to(message, 'К сожалению, не удалось найти музыку.')

def search_music(query):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=query,
            part='id',
            maxResults=1,
            type='video'
        ).execute()

        video_id = search_response['items'][0]['id']['videoId']
        music_url = f'https://www.youtube.com/watch?v={video_id}'
        return music_url

    except HttpError as e:
        print(f'An HTTP error occurred: {e}')

    return None

bot.polling()
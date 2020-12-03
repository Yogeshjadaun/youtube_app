**Steps to Setup:**

`docker-compose build
`

`docker-compose run web ./manage.py createsuperuser
`

`Login into admin at 0.0.0.0:8000/admin
`

`Add YoutubeApiKey`


`Use this for now: AIzaSyDJNbhb_gcAd6tKBE14YHkG2xmZcr1UZLo
(It will be deactivated after 48 hours)`

**Api's:**


**Get videos Api:**
- 0.0.0.0:8000/api/youtube-videos/
- eg http://0.0.0.0:8000/api/youtube-videos/?page=1
- query params: 

            page:str (page_number)

Search youtube video api:
- 0.0.0.0:8000/api/youtube-videos/search/
- eg. http://0.0.0.0:8000/api/youtube-videos/search/?page=1&video=non+becomes
- query params: 

            page:str (page_number)
            video:str (text to search)

Dashboard api:
- 0.0.0.0:8000/api/youtube-videos/dashboard/
- eg. http://0.0.0.0:8000/api/youtube-videos/dashboard/?page=1&video=non+becomes&sort=-title
- query params:

            page:str (page_number)
            video:str (text to search)
            sort:str (publishing_date,title,description)(append with - to reverse order)

**Background Server:**

- Using Celery for backgound tasks
- It is updating database by response from youtube data api.
- Taking new keys if the key is expired or its quota is exhausted.
- It is in youtube_engine/tasks.py
- In case if you want to change:
    - Search keyword is in youtubeapp/settings
    - Max Result (Youtube result limit) is in youtubeapp/settings

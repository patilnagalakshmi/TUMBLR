'''Logic for All features to manage Tumblr'''
import csv
import requests
import sqlalchemy as db
from database import ResponseRecords, connection
from model import settings, auth
from custom_logging import loggers
BASE_URL='https://api.tumblr.com/v2'
class Tumblr:
    '''Providing methods for features '''
    def create_post(self):
        """Send a post request to the Tumblr API to create a new post"""
        url=f"{BASE_URL}/blog/{settings.BLOG_IDENTIFIER}/post"
        title=input('enter a title:')
        body=input('enter a body:')
        post_data = {
            "type": "text",
            "title": title,
            "body":body
            }
        try:
            response = requests.post(url, auth=auth, data=post_data, timeout=10)
            response.raise_for_status()
            loggers.info("Posted Successfully")
            return response.json(),post_data
        except requests.exceptions.RequestException as e:
            loggers.error("API request failed:%s",{e})
            return None,post_data
    def delete_post(self):
        '''Delete a post by using ID'''
        url=f"{BASE_URL}/blog/{settings.BLOG_IDENTIFIER}/post/delete"
        post_id=int(input('enter a ID:'))
        params={
            "id":post_id
        }
        try:
            response = requests.post(url, auth=auth, params=params, timeout=10)
            response.raise_for_status()
            loggers.info("Posted Deleted Successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            loggers.error("API request failed:%s",{e})
            return None
    def search_posts(self):
        '''Search for the posts with tag'''
        url= f"{BASE_URL}/tagged"
        tag=input('enter a tag:')
        params={
            "tag":tag,
            "limit":100
        }
        try:
            response=requests.get(url,auth=auth,params=params,timeout=10)
            response.raise_for_status()
            loggers.info("Searched Results")
            return response.json()
        except requests.exceptions.RequestException as e:
            loggers.error("API request failed:%s",{e})
            return None
    def get_post(self):
        '''Display all posts '''
        url=f"{BASE_URL}/blog/{settings.BLOG_IDENTIFIER}/posts"
        params = {
            "limit":2
        }
        try:
            response=requests.get(url,auth=auth,params=params,timeout=10)
            response.raise_for_status()
            loggers.info("Searched Results")
            return response.json()
        except requests.exceptions.RequestException as e:
            loggers.error("API request failed:%s",{e})
            return None


def store_data(response_data,post_data):
    """Store response data in the database and write it to a CSV file"""
    if not response_data:
        loggers.error("No response data to store.")
        return

    try:
        status = response_data['meta']['status']
        msg = response_data['meta']['msg']
        post_id = response_data['response']['id']
        post_state = response_data['response']['state']
        post_display_text = response_data['response'].get('display_text', '')

        # Insert into the database
        query = db.insert(ResponseRecords).values(
            id=post_id,
            status=status,
            msg=msg,
            state=post_state,
            display_text=post_display_text,
            post_data=post_data
        )
        connection.execute(query)
        connection.commit()
        loggers.info("Post data stored successfully in the database")

        # Write into CSV file
        with open('tumblr.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['status', 'msg', 'post_id', 'state', 'display_text','postdata']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0:  # Write header if file is empty
                writer.writeheader()
            dataset = {
                'status': status,
                'msg': msg,
                'post_id': post_id,
                'state': post_state,
                'display_text': post_display_text,
                'postdata':post_data
            }
            writer.writerow(dataset)
        loggers.info("Post data written successfully to CSV")

    except ImportError as e:
        loggers.error("Failed to store post data:%s",{e})
    
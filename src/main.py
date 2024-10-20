'''To manage Tumblr using API'''
from services import Tumblr,store_data
from custom_logging import loggers
tumblr=Tumblr()
def main():
    '''To manage various features'''
    while True:
        print("\n-----TUMBLR-----")
        print("1. Create a post")
        print("2. Get posts")
        print("3. Delete a post")
        print("4. Search a blog")
        print("5. Exit")
        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            response_data,post_data = tumblr.create_post()
            if response_data and response_data['meta']['status'] == 201:
                store_data(response_data,post_data)
            else:
                loggers.error("Post creation failed or received invalid response")
        elif choice == '2':
            result=tumblr.get_post()
            posts = result["response"]["posts"]
            for post in posts:
                post_id = post.get("id")
                post_type = post.get("type", "Unknown type")
                post_summary = post.get("summary", "No summary available")
                post_url = post.get("post_url", "No URL available")
                loggers.info("Post ID:%s",post_id)
                loggers.info("Post Type:%s",post_type)
                loggers.info("Summary:%s",post_summary)
                loggers.info("Post URL:%s",post_url)
        elif choice == '3':
            tumblr.delete_post()
        elif choice == '4':
            posts=tumblr.search_posts()["response"]
            for post in posts:
                post_type = post.get("type", "Unknown type")
                post_summary = post.get("summary", "No summary available")
                post_url = post.get("post_url", "No URL available")
                blog_name = post.get("blog_name", "Unknown blog")
                loggers.info("Post Type:%s",{post_type})
                loggers.info("Summary:%s",{post_summary})
                loggers.info("Post URL:%s",{post_url})
                loggers.info("Blog Name:%s",{blog_name})

        elif choice == '5':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

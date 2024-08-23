import wikipediaapi

def Wiki_Search(prompt):

    # Specify a User-Agent string that adheres to Wikipedia's policy
    user_agent = "3D Assistant/1.0 (Sohaib; Contact: afzalsohaib59@gmail.com)"

    # Create a Wikipedia API object with the User-Agent
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)

    # Search for a page
    page = wiki_wiki.page(prompt)

    # Check if the page exists
    if page.exists():
        print(f"Title: {page.title}")
        print(f"Summary: {page.summary[:1000]}...")  # Print the first 500 characters of the summary
    else:
        print("Page not found.")
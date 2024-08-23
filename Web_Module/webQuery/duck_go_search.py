from duckduckgo_search import DDGS


def Duck_Search(prompt):

    # Perform a search on DuckDuckGo
    results = DDGS().text(prompt, max_results=5)
    print(results)

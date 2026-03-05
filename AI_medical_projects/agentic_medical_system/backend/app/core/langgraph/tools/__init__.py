from langchain_community.tools import DuckDuckGoSearchResults

# We can add more specific medical tools here later
search_tool = DuckDuckGoSearchResults()

tools = [search_tool]

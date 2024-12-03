import os
from jira import JIRA

def main():
    # Fetch environment variables for Jira token and base URL
    token = os.getenv('JIRA_TOKEN')
    jira_base_url = os.getenv('JIRA_BASE_URL', 'https://issues.redhat.com')  # Default to Red Hat Jira if not provided
    
    if not token:
        print("Error: JIRA_TOKEN is not set in the environment variables.")
        return
    
    # Define the JQL filter and other necessary data
    jql_query = os.getenv('JQL_QUERY')
    
    if not jql_query:
        print("Error: JQL_QUERY is not set in the environment variables.")
        return

    print(f"Using JQL filter: {jql_query}")

    # Connect to Jira using the token for authentication
    jira = JIRA(jira_base_url, token_auth=token)

    # Perform the search using the JQL query
    issues_in_release = jira.search_issues(jql_query)

    # Print the Jira issue keys (IDs) to the console
    for issue in issues_in_release:
        print(f"Jira Issue Key: {issue.key}")

if __name__ == "__main__":
    main()

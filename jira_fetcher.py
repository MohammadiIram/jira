import os
from jira import JIRA

def fetch_all_issues(jira, jql_query, max_results=100):
    # Initialize an empty list to store all issue keys
    all_issue_keys = []
    
    # Jira's search function can be paginated
    start_at = 0
    while True:
        # Fetch a batch of issues (set maxResults to 100)
        issues = jira.search_issues(jql_query, startAt=start_at, maxResults=max_results)  # Fetch 100 at a time
        all_issue_keys.extend([issue.key for issue in issues])
        
        # If we fetched fewer issues than max_results, we are done
        if len(issues) < max_results:
            break
        
        # Move to the next page of results
        start_at += max_results
    
    return all_issue_keys

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

    # Fetch all issues matching the JQL filter, handling pagination
    all_issue_keys = fetch_all_issues(jira, jql_query)

    # Print the Jira issue keys (IDs) to the console
    for issue_key in all_issue_keys:
        print(f"Jira Issue Key: {issue_key}")

if __name__ == "__main__":
    main()

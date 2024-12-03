import os
from jira import JIRA

def fetch_all_issues(jira, jql_query, max_results=100):
    # Initialize an empty list to store all issues in the required format
    all_issues = []
    
    # Jira's search function can be paginated
    start_at = 0
    while True:
        # Fetch a batch of issues (set maxResults to 100)
        issues = jira.search_issues(jql_query, startAt=start_at, maxResults=max_results)  # Fetch 100 at a time
        
        # Add each issue in the desired format to the all_issues list
        for issue in issues:
            all_issues.append({
                'id': issue.key,
                'source': 'issues.redhat.com'
            })
        
        # If we fetched fewer issues than max_results, we are done
        if len(issues) < max_results:
            break
        
        # Move to the next page of results
        start_at += max_results
    
    return all_issues

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
    all_issues = fetch_all_issues(jira, jql_query)

    # Print the formatted issues
    for issue in all_issues:
        print(f"- id: {issue['id']}")
        print(f"  source: {issue['source']}")

if __name__ == "__main__":
    main()

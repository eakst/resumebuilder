import requests
from bs4 import BeautifulSoup

def analyze_job_requirements(job_url):
  """
  Extracts the entire job posting content from a given URL.

  Args:
    job_url: The URL of the job posting.

  Returns:
    The job posting content as a string, or None if an error occurs.
  """

  try:
    # Fetch the webpage content
    response = requests.get(job_url)
    response.raise_for_status()

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # --- Strategy 1: Target the main content area ---
    # Many job websites have a main <div> or <article> that holds the posting
    content_element = soup.find('div', class_='main-content-area')  # Example class name
    if not content_element:
      content_element = soup.find('article', class_='job-posting') # Another example

    # --- Strategy 2: If no specific container, get all text within <body> ---
    if not content_element:
      content_element = soup.find('body')

    if content_element:
      # Extract the text content
      job_description = content_element.get_text(separator='\n', strip=True)
      return job_description
    else:
      print(f"Could not find job posting content on {job_url}")
      return None

  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
    return None
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    return None

# Example usage
job_url = "https://jobs.lever.co/applydigital/4322650c-8d14-487c-863d-2bf0b027f250"  # Replace with the actual URL
job_posting = analyze_job_requirements(job_url)

if job_posting:
  print(job_posting)

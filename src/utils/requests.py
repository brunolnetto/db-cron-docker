import requests
from requests.exceptions import RequestException
from setup.logging import logger

def download_file(
    url: str, 
    destination: str, 
    timeout:int=10, 
    retries:int=3
) -> bool:
  """
  Downloads a file from the specified URL with timeout and retry handling.

  Args:
      url (str): The URL of the file to download.
      timeout (int, optional): The connection timeout in seconds. Defaults to 10.
      retries (int, optional): The number of retries on failure. Defaults to 3.

  Returns:
      bool: True if download is successful, False otherwise.
  """
  for attempt in range(retries + 1):
    try:
      response = requests.get(url, timeout=timeout)
      response.raise_for_status()
      
      with open(destination, 'wb') as f:
        f.write(response.content)

      return True
    
    except RequestException as e:
      logger.info(f"Download attempt {attempt} failed: {e}")
  
  return False
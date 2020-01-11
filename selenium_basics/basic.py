from selenium import webdriver
from shutil import which

edge_path = which("MicrosoftEdgeSetupDev")

driver = webdriver.Edge(executable_path=edge_path)
driver.get("https://duckduckgo.com")

search_input = driver.find_elements_by_class_name("js-search-input")
search_input.send_keys("my user agent")



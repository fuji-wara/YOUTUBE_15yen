from selenium import webdriver

# selenium 設定
options = webdriver.chrome.options.Options()
profile_path = '/Users/fujiwarayuuki/Library/Application Support/Google/Chrome/Default'
options.add_argument('--user-data-dir=' + profile_path)
options.add_argument('--profile-directory=profile2')
driver = webdriver.Chrome("./chromedrive/chromedriver",options=options)
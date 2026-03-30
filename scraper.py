from playwright.sync_api import sync_playwright
import json


def remove_popup(page):
    page.wait_for_timeout(2000)  # wait for popup to appear

    #Runs JavaScript inside the browser context, not Python.
    page.evaluate("""
        const modal = document.querySelector('#pagegate');
        if (modal) modal.remove();
                  
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) backdrop.remove();

        document.body.classList.remove('modal-open');
    """)

def scrape_entertainment(page):
    # Navigation
    page.goto("https://ekantipur.com")
    remove_popup(page)
    
    page.wait_for_selector("text=मनोरञ्जन")

    # Click Entertainment
    page.click("text=मनोरञ्जन")

    # Wait for page  to load including articles and dynamic contents
    page.wait_for_load_state("networkidle")
    remove_popup(page)
  

    # STEP 1: to select first five articles with class category-inner-wrapper
    articles = page.query_selector_all(".category-inner-wrapper")[:5]

    #Initialize a empty list to store scraped article data
    news_data = []

    # Loop over each article element to exteract title, image and author
    for article in articles:
        #use try and except to avioid crashing if an element is missing
        try:
            # Extract title	
            title_el = article.query_selector("h2 a")
            title = title_el.text_content().strip() if title_el else None 
      
            # Extract image 
            img_el = article.query_selector(".category-image img")
            image_url = img_el.get_attribute("src") if img_el else None
            
            #to handle lazy loaded images(some images are not in src initially, only in data-src)
            if img_el:
                image_url = (
                    img_el.get_attribute("src") or
                    img_el.get_attribute("data-src")
                )
            else:
                image_url = None    
            

            # Handeling missing author safely
            author_el = article.query_selector(".author-name a")
            author = author_el.text_content().strip() if author_el else None

        except: 
            title = None
            image_url = None
            author = None
       
       # Append data to news_data
        news_data.append({
            "title": title,
            "image_url": image_url,
            "category": "मनो रञ्जन",
            "author": author
        })

    return news_data

def scrape_cartoon(page):
    page.goto("https://ekantipur.com/cartoon")
    page.wait_for_load_state("networkidle")
    
    try:
        # .cartoon-image img selects <img> inside the container with class .cartoon-image
        img_el=page.query_selector(".cartoon-image img")

        # Extract title from alt attribute of <img>
        title = img_el.get_attribute("alt") if img_el else None

        # Extracting image_url from src attribute of <img>
        image_url = img_el.get_attribute("src") if img_el else None

        # create the dictionary to stire cartoon data
        cartoon_data= {
            "title": title,
            "image_url": image_url,
            "author": None
        }

    except:
        title = None
        image_url = None
        author = None
 
    return cartoon_data


def main():
    # Initializing Playwrite
    with sync_playwright() as p:
        # opens visible chrome browser
        browser = p.chromium.launch(headless=False)

	# link to open in new page
        page = browser.new_page()

        # runs both scrapers and stores result
        entertainment = scrape_entertainment(page)
        cartoon = scrape_cartoon(page)

        # Save json
        output = {
            "entertainment_news": entertainment,
            "cartoon_of_the_day": cartoon
        }

        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        browser.close()
        
if __name__ == "__main__":
    main()

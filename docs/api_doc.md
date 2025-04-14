## project documentation

### api structure 
    root/
    ├── docs/
    │   └── documentation.md
    ├── src/
    │   ├── main.py
    │   ├── database.py
    │   └── utils/
    │       └── web_scrape.py
    ├── venv/
    ├── .gitignore
    └── README.md


### api functioning
#### endpoints

    /scrape/ --> endpoint a url is given and it returns the text of given site

        it gives back a disctionary with the following elements

        already_scraped: boolean if true the link was alread scraped else it was not 
        result: with the three following data part
            time: when was it scraped first
            url: which url
            text: the scraped text
    
    /search_url/ --> searches by give url, it has to be case sensitive returns the folowing values

        already_scraped: boolean if true the link was alread scraped else it was not 

        result: a single result with the following structure

            time: above explained already
            url: above explained already
            text above explained already


    /search_keyword/ --> searches for given keyword, it has to be case sensitive

        returns the folowing values

        already_scraped: boolean if true the link was alread scraped else it was not 

        result: a list/dictionary of elements with the following structure with given index regarding the amount of results 

            0: 
                time: above explained already
                url: above explained already
                text above explained already
            1: 
                time: above explained already
                url: above explained already
                text above explained already



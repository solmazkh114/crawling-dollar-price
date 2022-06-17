import crawling_engine
import storing_data
from analyzing_data import *



if __name__ == "__main__":
    crawler = crawling_engine.crawling_app()
    print("data is crawling, please wait...")
    crawler.extract_data()
    print("Data was crawled")
    table ="table_dollar_price"
    #store data on database
    store_obj = storing_data.store_on_database(table=table)
    store_obj.store_data()
    #retrieve data for analyzing
    df = retrieve_data(table=table)
    plot(preprocess(df))
    candlestick(df)





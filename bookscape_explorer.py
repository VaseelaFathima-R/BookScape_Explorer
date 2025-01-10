import streamlit as st
import mysql.connector
import pandas as pd
import requests

# Function to create a connection to MySQL
def create_connection():
    return mysql.connector.connect(
        host="localhost",  # Change this to your MySQL server if it's not local
        user="root",
        password="raja",
        database="bookscape_explorer"
    )

# Connect to MySQL
conn = create_connection()

# Create a cursor object
mycursor = conn.cursor()
def page_1():
    # Streamlit UI
    st.markdown(
        '<h1 style="text-align: center;"><p style="font-size:50px; font-style:italic; color:red;">Data Analysis</p></h1>',
        unsafe_allow_html=True
    )
    col1,col2 = st.columns([1, 1],gap="small",border=True)

    with col1:
        mycursor.execute("""
            SELECT COUNT(*) FROM bookscape_explorer.books WHERE isEbook = 1;
                """)
        eBook_count = mycursor.fetchone()[0]  # Fetch result of the first query

        # Execute the second query for Physical books
        mycursor.execute("""
             SELECT COUNT(*) FROM bookscape_explorer.books WHERE isEbook = 0;
            """)
        physicalBook_count = mycursor.fetchone()[0]  # Fetch result of the second query

        # Create a DataFrame with the results
        table_data = [['eBook', eBook_count], ['Physical', physicalBook_count] ]

        answer_1 = pd.DataFrame(table_data, columns=['format', 'total_books'])
        st.write("**1.Check Availability of eBooks vs Physical Books**")
        # Display the DataFrame when the button is clicked
        if st.button("1.Answer"):
            st.dataframe(answer_1)
        st.write("**2.Find the Publisher with the Most Books Published**")
        mycursor.execute("""
            SELECT publisher, COUNT(*) AS total_books
            FROM books
            GROUP BY publisher
            ORDER BY total_books DESC
            LIMIT 3;
            """)

        # Fetch the results
        results = mycursor.fetchall()

        # Convert results to a pandas DataFrame
        top_publishers = pd.DataFrame(results, columns=['publisher', 'total_books'])

        if st.button("2.Answer"):
            st.dataframe(top_publishers)# Display the result

        st.write("**3.Identify the Publisher with the Highest Average Rating**")
        mycursor.execute("""
            SELECT publisher, AVG(averageRating) AS average_rating
            FROM books
            GROUP BY publisher
            ORDER BY average_rating DESC
            LIMIT 1;
            """)

        # Fetch the result
        result = mycursor.fetchone()  # Returns a single row as a tuple

        # Convert the result into a DataFrame by wrapping it in a list
        columns = ['publisher', 'average_rating']
        top_publisher_df = pd.DataFrame([result], columns=columns)  # Wrap result in a list

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("3.Answer"):
            st.dataframe(top_publisher_df)  # Display the result

        st.write("**4.Get the Top 5 Most Expensive Books by Retail Price**")

        mycursor.execute("""
            SELECT book_title, amount_retailPrice, publisher
            FROM books
            ORDER BY amount_retailPrice DESC
            LIMIT 5;
            """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_title', 'amount_retailPrice', 'publisher']
        top_books_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("4.Answer"):
            st.dataframe(top_books_df)  # Display the result

        st.write("**5.Find Books Published After 2010 with at Least 500 Pages**")
    
        mycursor.execute("""
            SELECT book_title, publisher, year, pageCount
            FROM books
            WHERE year > 2010 AND pageCount >= 500
            ORDER BY year DESC;
            """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_title', 'publisher', 'year', 'pageCount']
        books_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("5.Answer"):
            st.dataframe(books_df)  # Display the result

        st.write("**6. List Books with Discounts Greater than 20%**")
        mycursor.execute("""
            SELECT book_title, publisher, amount_listPrice, amount_retailPrice, 
                ROUND((amount_listPrice - amount_retailPrice) / amount_listPrice * 100, 2) AS discount_percentage
                FROM books
                WHERE (amount_listPrice - amount_retailPrice) / amount_listPrice > 0.20
                ORDER BY discount_percentage DESC;
                 """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_title', 'publisher', 'amount_listPrice', 'amount_retailPrice', 'discount_percentage']
        discounted_books_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("6.Answer"):
            st.dataframe(discounted_books_df)  # Display the result
   
        st.write("**7.Find the Average Page Count for eBooks vs Physical Books**")
        mycursor.execute("""
            SELECT 
            CASE WHEN isEbook = 1 THEN 'eBook' ELSE 'Physical' END AS format,
            AVG(pageCount) AS average_page_count
            FROM books
            GROUP BY isEbook;
            """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['format', 'average_page_count']
        page_count_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("7.Answer"):
            st.dataframe(page_count_df)  # Display the result

        st.write("**8.Find the Top 3 Authors with the Most Books**")
        mycursor.execute("""
            SELECT book_authors, 
                COUNT(*) AS total_books
                FROM books
                GROUP BY book_authors
                ORDER BY total_books DESC
                LIMIT 3;
                """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_authors', 'total_books']
        top_authors_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("8.Answer"):
            st.dataframe(top_authors_df)  # Display the result

        st.write("**9.List Publishers with More than 10 Books**")
        mycursor.execute("""
            SELECT publisher, COUNT(*) AS total_books
            FROM books
            GROUP BY publisher
            HAVING total_books > 10
            ORDER BY total_books DESC;
            """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['publisher', 'total_books']
        publishers_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("9.Answer"):
            st.dataframe(publishers_df)  # Display the result

    
        st.write("**10.Find the Average Page Count for Each Category**")
    
        mycursor.execute("""
            SELECT 
                categories, 
                AVG(pageCount) AS average_page_count
                FROM books
                GROUP BY categories;
                """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['categories', 'average_page_count']
        category_page_count_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("10.Answer"):
            st.dataframe(category_page_count_df)  # Display the result


    with col2:
        st.write("**11.Retrieve Books with More than 3 Authors**")
        mycursor.execute("""
            SELECT book_title, book_authors
            FROM books
            WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;
            """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_title', 'book_authors']
        books_with_multiple_authors_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("11.Answer"):
            st.dataframe(books_with_multiple_authors_df)  # Display the result
    
        st.write("**12.Books with Ratings Count Greater Than the Average**")
        mycursor.execute("""
            SELECT 
                book_title, 
                ratingsCount, 
                averageRating 
                FROM books
                WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books);
                """)
    
        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_title', 'ratingsCount', 'averageRating']
        books_above_avg_ratings_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("12.Answer"):
            st.dataframe(books_above_avg_ratings_df)  # Display the result

        st.write("**13.Books with the Same Author Published in the Same Year**")
        mycursor.execute("""
            SELECT 
                book_authors, 
                year, 
                GROUP_CONCAT(book_title SEPARATOR ', ') AS book_titles,
                COUNT(*) AS book_count
                FROM books
                GROUP BY book_authors, year
                HAVING COUNT(*) > 1;
                """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_authors', 'year', 'book_titles', 'book_count']
        same_author_same_year_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("13.Answer"):
            st.dataframe(same_author_same_year_df)  # Display the result

        st.write("**14.Books with a Specific Keyword in the Title**")
    
        keyword = st.text_input("Enter a keyword to search in book titles:", value="")

        # Execute the query only if a keyword is provided
        if keyword:
            query = f"""
                SELECT 
                    book_id, 
                    book_title, 
                    book_authors, 
                    averageRating
                    FROM books
                    WHERE book_title LIKE '%{keyword}%';
                    """
            mycursor.execute(query)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_id', 'book_title', 'book_authors', 'averageRating']
        books_with_keyword_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("Search"):
            st.dataframe(books_with_keyword_df)  # Display the result

        st.write("**15.Year with the Highest Average Book Price**")
    
        mycursor.execute("""
            SELECT 
                year, 
                AVG(amount_retailPrice) AS average_price
                FROM books
                GROUP BY year
                ORDER BY average_price DESC
                LIMIT 1;
                """)

        # Fetch the result
        result = mycursor.fetchone()

        # Convert the result into a pandas DataFrame
        columns = ['year', 'average_price']
        highest_avg_price_df = pd.DataFrame([result], columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("15.Answer"):
            st.dataframe(highest_avg_price_df)  # Display the result

        st.write("**16.Count Authors Who Published 3 Consecutive Years**")
    
        mycursor.execute("""
            SELECT 
            COUNT(DISTINCT book_authors) AS authors_with_three_consecutive_years
            FROM (
                SELECT 
                    book_authors, 
                    year, 
                    LEAD(year, 1) OVER (PARTITION BY book_authors ORDER BY year) AS next_year,
                    LEAD(year, 2) OVER (PARTITION BY book_authors ORDER BY year) AS next_to_next_year
                    FROM books
                 ) AS consecutive_years
            WHERE next_year = year + 1 AND next_to_next_year = year + 2;
            """)

        # Fetch the result
        result = mycursor.fetchone()

        # Convert the result into a pandas DataFrame
        columns = ['authors_with_three_consecutive_years']
        three_consecutive_years_df = pd.DataFrame([result], columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("16.Answer"):
            st.dataframe(three_consecutive_years_df)  # Display the result

        st.write("**17.Find Authors with Different Publishers in the Same Year**")
    
        # Execute the query
        mycursor.execute("""
            SELECT 
                book_authors,
                year,
                COUNT(DISTINCT publisher) AS different_publishers,
                COUNT(*) AS total_books
                FROM books
                GROUP BY book_authors, year
                HAVING COUNT(DISTINCT publisher) > 1;
            """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_authors', 'year', 'different_publishers', 'total_books']
        authors_different_publishers_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("17.Answer"):
            st.dataframe(authors_different_publishers_df)  # Display the result

        st.write("**18.Average Prices of eBooks and Physical Books**")
        mycursor.execute("""
            SELECT 
            COALESCE(AVG(CASE WHEN isEbook = 1 THEN amount_retailPrice END), 0) AS avg_ebook_price,
            COALESCE(AVG(CASE WHEN isEbook = 0 THEN amount_retailPrice END), 0) AS avg_physical_price
            FROM books;
            """)

         # Fetch the result
        result = mycursor.fetchone()

        # Convert the result into a pandas DataFrame
        columns = ['avg_ebook_price', 'avg_physical_price']
        average_prices_df = pd.DataFrame([result], columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("18.Answer"):
            st.dataframe(average_prices_df)  # Display the result    

        st.write("**19.Find Outlier Books by Rating**")
        mycursor.execute("""
        WITH Stats AS (
            SELECT 
                AVG(averageRating) AS avg_rating,
                STDDEV(averageRating) AS stddev_rating
                FROM books
                )
            SELECT 
                book_title,
                averageRating,
                ratingsCount
                FROM books, Stats
                WHERE 
                ABS(averageRating - avg_rating) > 2 * stddev_rating;
            """)

        # Fetch the result
        result = mycursor.fetchall()

        # Convert the result into a pandas DataFrame
        columns = ['book_title', 'averageRating', 'ratingsCount']
        outliers_df = pd.DataFrame(result, columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("19.Answer"):
            st.dataframe(outliers_df)  # Display the result

        st.write("**20.Find Publisher with Highest Average Rating**")
         # Execute the query
        mycursor.execute("""
            WITH PublisherStats AS (
            SELECT 
                publisher,
                AVG(averageRating) AS average_rating,
                COUNT(*) AS total_books
                FROM books
                GROUP BY publisher
                HAVING COUNT(*) > 10
                )
            SELECT 
                publisher,
                average_rating,
                total_books
                FROM PublisherStats
                ORDER BY average_rating DESC
                LIMIT 1;
                """)

        # Fetch the result
        result = mycursor.fetchone()

        # Convert the result into a pandas DataFrame
        columns = ['publisher', 'average_rating', 'total_books']
        top_publisher_df = pd.DataFrame([result], columns=columns)

        # Display the DataFrame in Streamlit when the button is clicked
        if st.button("20.Answer"):
            st.dataframe(top_publisher_df)  # Display the result

def page_2():
    API_KEY = "AIzaSyCvTA2GqYH2tYfI1vYxjkrDJ6lMzeNcStE"
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
  
    # Function to fetch books data
    def fetch_books(query, max_results, api_key):
        start_index = 0
        books_data = []
        while len(books_data) < max_results:
            params = {
                    "q": query,
                    "key": api_key,
                    "startIndex": start_index,
                    "maxResults": min(40, max_results - len(books_data))
                    }
            response = requests.get(BASE_URL, params=params)
            if response.status_code != 200:
                st.error(f"Error fetching data from API: {response.status_code}")
                break
            data = response.json()
            if "items" not in data:
                st.warning("No books found.")
                break
            books_data.extend(data["items"])
            start_index += 40
        return books_data

        # Function to process the book data
    def process_books_data(books, query):
        processed_data = []
        for book in books:
            volume_info = book.get('volumeInfo', {})
            sale_info = book.get('saleInfo', {})
            processed_data.append({
                'book_id': book.get('id'),
                'search_key': query,
                'book_title': volume_info.get('title', 'N/A'),
                'book_subtitle': volume_info.get('subtitle', 'N/A'),
                'book_authors': ", ".join(volume_info.get('authors', ['N/A'])),
                'book_description': volume_info.get('description', 'N/A'),
                'industryIdentifiers': ', '.join(f"{i['type']}: {i['identifier']}" for i in volume_info.get('industryIdentifiers', [])),
                'text_readingModes': volume_info.get('readingModes', {}).get('text', False),
                'image_readingModes': volume_info.get('readingModes', {}).get('image', False),
                'pageCount': volume_info.get('pageCount', 0),
                'categories': ", ".join(volume_info.get('categories', ['N/A'])),
                'language': volume_info.get('language', 'N/A'),
                'imageLinks': volume_info.get('imageLinks', {}).get('thumbnail', 'N/A'),
                'ratingsCount': volume_info.get('ratingsCount', 0),
                'averageRating': volume_info.get('averageRating', 0.0),
                'country': sale_info.get('country', 'N/A'),
                'saleability': sale_info.get('saleability', 'N/A'),
                'isEbook': sale_info.get('isEbook', False),
                'amount_listPrice': sale_info.get('listPrice', {}).get('amount', 0.0),
                'currencyCode_listPrice': sale_info.get('listPrice', {}).get('currencyCode', 'N/A'),
                'amount_retailPrice': sale_info.get('retailPrice', {}).get('amount', 0.0),
                'currencyCode_retailPrice': sale_info.get('retailPrice', {}).get('currencyCode', 'N/A'),
                'buyLink': sale_info.get('buyLink', 'N/A'),
                'year': volume_info.get('publishedDate', 'N/A'),
                'publisher': volume_info.get('publisher', 'N/A')
                })
        return processed_data

# Function to insert books data into the database
    def insert_books_into_db(conn, books_data, append_mode):
        try:
            cursor = conn.cursor()

            if not append_mode:
                st.warning("Overwrite mode selected. Existing data will be deleted.")
                cursor.execute("DELETE FROM books")
                conn.commit()

            insert_query = '''
                INSERT IGNORE INTO books (book_id, search_key, book_title, book_subtitle, book_authors, book_description, 
                industryIdentifiers, text_readingModes, image_readingModes, pageCount, categories, language, imageLinks, 
                ratingsCount, averageRating, country, saleability, isEbook, amount_listPrice, currencyCode_listPrice, 
                amount_retailPrice, currencyCode_retailPrice, buyLink, year, publisher) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                '''
            data_to_insert = [
                (
                    book['book_id'], book['search_key'], book['book_title'], book['book_subtitle'], book['book_authors'], book['book_description'],
                    book['industryIdentifiers'], book['text_readingModes'], book['image_readingModes'], book['pageCount'], book['categories'],
                    book['language'], book['imageLinks'], book['ratingsCount'], book['averageRating'], book['country'], book['saleability'],
                    book['isEbook'], book['amount_listPrice'], book['currencyCode_listPrice'], book['amount_retailPrice'],
                    book['currencyCode_retailPrice'], book['buyLink'], book['year'], book['publisher']
                )
                for book in books_data
                    ]
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
            st.success(f"Inserted {len(data_to_insert)} records into the database.")
        except mysql.connector.Error as e:
            st.error(f"Error inserting data into database: {e}")
        finally:
            cursor.close()

    # Streamlit App
    def main():
        st.title("Web Scraping: Google Books API")

        # User input for the search term and other options
    query = st.text_input("Enter a search term (e.g., 'python programming')", "")
    max_results = st.number_input("Number of results to fetch (max: 1000)", min_value=1, max_value=1000, value=100, step=10)
    append_mode = st.checkbox("Append Mode (Keep existing data)")

    if st.button("Fetch and Save Books"):
            if not query:
                st.error("Please enter a search term.")
                return

            st.info("Fetching books from Google Books API...")
            books = fetch_books(query, max_results, API_KEY)
            if not books:
                st.error("No books found.")
                return

            st.info("Processing books data...")
            processed_data = process_books_data(books, query)

            st.info("Inserting books data into the database...")
            conn = create_connection()
            if conn:
                insert_books_into_db(conn, processed_data, append_mode)
                conn.close()

# Create the styled radio button
st.markdown(
    '<h1 style="font-size: 40px; text-align: center;">Choose the selection:</h1>',
    unsafe_allow_html=True
)

# Radio button for page selection
page = st.radio("", ["Data Analysis", "Web Scraping"])


# Display content based on the selected page
if page == "Data Analysis":
    st.write("**Data analysis page content**")
    page_1()
elif page == "Web Scraping":
    page_2()

   
    mycursor.close()
    conn.close()

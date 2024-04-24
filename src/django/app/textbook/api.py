import requests

def searchISBN(isbn):
    api = 'https://www.googleapis.com/books/v1/volumes'
    
    response_isbn = requests.get(api, params={'q': f'isbn:{isbn}'})
    if response_isbn.status_code != 200 or response_isbn.json()['totalItems'] == 0:
        return None 
    response_isbn = response_isbn.json()['items'][0]
    
    bookInfo = {
		'isbn' : isbn,
		'title' : response_isbn['volumeInfo']['title'],
		'authors' : response_isbn['volumeInfo']['authors'],
		'publishedDate' : response_isbn['volumeInfo']['publishedDate'],
		'image' : response_isbn['volumeInfo']['imageLinks']['thumbnail']
	}
    
    return bookInfo
    

def main():
    response = searchISBN('9780345444882')
    for keys in response.keys():
        print(f'{keys}: {response[keys]}')

if __name__ == '__main__':
    main()


"""
The Talisman

{
  "kind": "books#volumes",
  "totalItems": 1,
  "items": [
    {
      "kind": "books#volume",
      "id": "XI483aadNEcC",
      "etag": "+7JHj+D+KN0",
      "selfLink": "https://www.googleapis.com/books/v1/volumes/XI483aadNEcC",
      "volumeInfo": {
        "title": "The Talisman",
        "subtitle": "A Novel",
        "authors": [
          "Stephen King",
          "Peter Straub"
        ],
        "publisher": "Simon and Schuster",
        "publishedDate": "2012-09-25",
        "description": "Originally published: New York: Viking: Putnam, 1984.",
        "industryIdentifiers": [
          {
            "type": "ISBN_13",
            "identifier": "9781451697216"
          },
          {
            "type": "ISBN_10",
            "identifier": "145169721X"
          }
        ],
        "readingModes": {
          "text": false,
          "image": false
        },
        "pageCount": 902,
        "printType": "BOOK",
        "categories": [
          "Fiction"
        ],
        "maturityRating": "NOT_MATURE",
        "allowAnonLogging": false,
        "contentVersion": "0.1.1.0.preview.0",
        "panelizationSummary": {
          "containsEpubBubbles": false,
          "containsImageBubbles": false
        },
        "imageLinks": {
          "smallThumbnail": "http://books.google.com/books/content?id=XI483aadNEcC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
          "thumbnail": "http://books.google.com/books/content?id=XI483aadNEcC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
        },
        "language": "en",
        "previewLink": "http://books.google.com/books?id=XI483aadNEcC&printsec=frontcover&dq=isbn:9781451697216&hl=&cd=1&source=gbs_api",
        "infoLink": "http://books.google.com/books?id=XI483aadNEcC&dq=isbn:9781451697216&hl=&source=gbs_api",
        "canonicalVolumeLink": "https://books.google.com/books/about/The_Talisman.html?hl=&id=XI483aadNEcC"
      },
      "saleInfo": {
        "country": "US",
        "saleability": "NOT_FOR_SALE",
        "isEbook": false
      },
      "accessInfo": {
        "country": "US",
        "viewability": "PARTIAL",
        "embeddable": true,
        "publicDomain": false,
        "textToSpeechPermission": "ALLOWED_FOR_ACCESSIBILITY",
        "epub": {
          "isAvailable": false
        },
        "pdf": {
          "isAvailable": false
        },
        "webReaderLink": "http://play.google.com/books/reader?id=XI483aadNEcC&hl=&source=gbs_api",
        "accessViewStatus": "SAMPLE",
        "quoteSharingAllowed": false
      },
      "searchInfo": {
        "textSnippet": "Originally published: New York: Viking: Putnam, 1984."
      }
    }
  ]
}
	"""
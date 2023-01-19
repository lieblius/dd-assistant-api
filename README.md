# DoorDash Assistant Api

<p align="center"><img src="https://i.imgur.com/9rTx9OH.png" width=300/></p>

This repo contains API used in a project for an embedded security class where the objective was to create an embedded voice assistant with various defense mechanisms against attacks; specifically [this one](https://lightcommands.com/). Our idea was a voice assistant for ordering food on DoorDash. Below is the relevant excerpt from our [report](report.pdf).

## Implementation Details

To interact with our hardware, a cloud server was hosted in the form of a RESTful API through a provider called [render](https://render.com/). Our server serves as an intermediary micro-service which contains its own logic and facilitates interactions between other services. 

At our server’s core is a Flask application with four main routes and an HTML page: 

- /api - Health check endpoint. 

- /api/transcribe - Development endpoint to see audio transcriptions. Input is an HTTP POST request of the audio bit stream from the microphone sent over the ESP32. Transcription is sent to Google Speech-to-Text and returned as the response. 

- /api/save - Development endpoint used to help see the recordings and transcriptions server side. It saves the audio and transcriptions to a disk and serves them on an HTML page at the root directory on the server to be viewed. 
- /api/dash - Handles the full order flow by acquiring audio transcriptions and sending the result to our command parser. The resolved command is then executed and the corresponding API call is made to DoorDash if the command is valid. 

To serve our requests, some of these endpoints utilize external services such as Google’s Speech-to-Text API and DoorDash’s private API. 

To interact with Google Speech-to-Text, a couple functions were written to convert the audio bit stream into a legible format for Google’s API as well as to configure and send the request. 

To interact with DoorDash’s private API a more complicated design was needed. First, API endpoints and request payloads were scraped using Chrome DevTools and Postman. These payloads were retrieved as JSON and contain GraphQL queries. To avoid having to deserialize GraphQL, these payloads were left as is and individually saved to their own files in JSON format. With payloads saved for all necessary functions (adding individual items to cart, clearing the cart, ordering, getting the cart items, getting the cart id), they can be loaded from their files, modified (setting item quantity, cart id, etc.), serialized, and sent off as HTTP requests. 

In order to utilize our interactions with external services correctly in the context of processing requests to our API, there is a command parser. The command parser searches through the retrieved audio transcription for keywords resolving to commands in many ways, some depending on sequential input and some order-invariant. The intent is to execute syntactically correct commands and ignore erroneous ones. After a command is discovered and the command’s parameters are successfully parsed, the correct payload is loaded, modified, serialized, and executed as described previously. It is either loaded directly, or in the case of a specific item, the command’s parameters are passed to an item payload resolver to retrieve the correct payload for that item. The command parser also contains additional logic to handle DTMF tones. The bits at the end of the data sent by the ESP32 contain information on whether a DTMF tone was detected for every 0.1 seconds of audio data. The command parser calls a utility function which aggregates these detected tones and resolves them to the most prominent tone found for that request if a threshold is reached. In this situation the command parser ignores any speech command and executes the command associated with the DTMF tone identified.

## Usage Notes

- Commit history has been purged and json files have been stripped of id's for privacy since a lot of this project involved tokens from DoorDash as well as third-party payment processing that I had left in the mess of json when scraping DoorDash's API.
- Google cloud requires setting GOOGLE_APPLICATION_CREDENTIALS env var to the path of the service account json file.
- dash.py requires doordashprivate.json which contains request headers needed for auth.

## Other Notes

- DoorDash's API is... pretty bad?
- Did they make an acquisition at some point and are stuck supporting multiple backends for different types of restaurants? Because otherwise I have no other idea why there would be such of a lack of consistency. Take a look at the differences between the json in the stores folder.
- So much bloat. You can make requests with a fraction of the data currently being sent in the payloads. Sometimes this makes sense if you would want a request to succeed in spite of missing information, but this does not seem to be the case in most of what I saw.
- Also their session tokens live for weeks which I guess optimizes revenue (making users sign in again would decrease conversion) but doesn't seem like the best security practice to me.
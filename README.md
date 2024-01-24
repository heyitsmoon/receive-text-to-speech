# Text To Speech With Azure Services
## Motivation
I wanted to start this project because I thought it would be fun to get messages from my friends read out to me. 

My main goals were to learn how to use API keys to access services and use environment variables to keep sensitive information separate from my code

## App Description

This code is a basic Flask web app that uses Azures text to speech services to convert messages submitted on a form from the html.

AZURE_VOICES and AZURE_VOICE_STYLES are configuration variables for the message to vary the voice it uses and the style of the voice. I have set these to be random, but the code could be modified so the senders of the message can modify how they want their message to be read.

The SPEECH_KEY and SPEECH_REGION is the API key and region provided by Microsoft Azure. Those have to be replaced with the ones provided to you.

When I used this code I ran it on 0.0.0.0 and opened port 5000 so that friends that I can give friends that I trust my IP address and they could visit the webapp from their computers and send me messages.

I know that this is an unsafe way to do this and there are other safer ways to achieve that functionality. I only wanted to text the functionality and have a bit of fun.
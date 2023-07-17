### QR Code Generator 

## Overlook 

<img width="511" alt="Screenshot 2023-07-17 at 12 26 02" src="https://github.com/StefanIancu/projects/assets/124818078/61b15851-745e-415d-8211-a14a57fad343">

## Purpose

<li>Helps the user generate a free QR Code for their website</li>
<li>Unlike the other online solutions, this QR Code never expires</li>

## First look 

When the user runs the application, it asks for the link. If the link doesn't have the correct format, the user cannot proceed further. 

*the input doesn't verify the termination of the domain link (".com", ".org", ".net"), it just verifies that the string starts with "www."

<img width="456" alt="Screenshot 2023-07-17 at 16 43 54" src="https://github.com/StefanIancu/projects/assets/124818078/a20fe665-9157-447e-8332-eea73b2768a7">

If the link respects the format, the QR code will be generated and saved into "codes" directory. The name of the .png file would be the name of the website. 

<img width="450" alt="Screenshot 2023-07-17 at 16 45 13" src="https://github.com/StefanIancu/projects/assets/124818078/c4b5eedb-ad37-4aad-bbff-63e725955462">

<img width="234" alt="Screenshot 2023-07-17 at 16 45 39" src="https://github.com/StefanIancu/projects/assets/124818078/a99b0613-425a-4ee2-bd4e-ca73cdb1fd20">

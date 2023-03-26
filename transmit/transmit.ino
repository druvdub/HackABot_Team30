/*Some code from:
 * Arduino Wireless Communication Tutorial
 *     Example 1 - Transmitter Code
 *
 * by Dejan Nedelkovski, www.HowToMechatronics.com
 *
 * Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
 */

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN

const byte address[2][12] = {"Node19", "Node20"};

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

void setup()
{
    Serial.begin(115200);
    Serial.println("<Arduino is ready>");
    radio.begin();
    // radio.openWritingPipe(address);
    // radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_MIN);
    radio.stopListening();
}

void loop()
{
    // for (int i = 0; i < 2; i++)
    // {
    //     radio.openWritingPipe(address[i]);

    //     recvWithStartEndMarkers();
    //     showNewData();

    //     radio.write(&receivedChars, sizeof(receivedChars));
    //     delay(50);
    // }

    // // recvWithStartEndMarkers();
    // // showNewData();

    // // radio.write(&receivedChars, sizeof(receivedChars));
    // // delay(50);

    recvWithStartEndMarkers();
    if (newData == true)
    {
        radio.write(&receivedChars, sizeof(receivedChars));
        newData = false;
    }

    radio.openWritingPipe(address[0]);
    radio.write(&receivedChars, sizeof(receivedChars));
    delay(50);

    radio.openWritingPipe(address[1]);
    radio.write(&receivedChars, sizeof(receivedChars));
    delay(50);
}

void recvWithStartEndMarkers()
{
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false)
    {
        rc = Serial.read();

        if (recvInProgress == true)
        {
            if (rc != endMarker)
            {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars)
                {
                    ndx = numChars - 1;
                }
            }
            else
            {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker)
        {
            recvInProgress = true;
        }
    }
}

void showNewData()
{
    if (newData == true)
    {
        Serial.println(receivedChars);
        newData = false;
    }
}
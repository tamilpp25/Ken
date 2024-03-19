#define pir 7
#define dht 5
#define ldr 4
#define soundSensor 2
#define ultra_trig 8
#define ultra_echo 10

#include <ArduinoJson.h>

JsonDocument doc;
void setup()
{
    // put your setup code here, to run once:
    Serial.begin(9600);
    pinMode(pir, INPUT);
    pinMode(dht, INPUT);
    pinMode(ldr, INPUT);
    pinMode(soundSensor, INPUT);
    pinMode(ultra_trig, OUTPUT);
    pinMode(ultra_echo, INPUT);
    while (!Serial)
        continue;
}

String get_ultrasonic(int triggerPin, int echoPin)
{ // Clear the trigger
    digitalWrite(triggerPin, LOW);
    delayMicroseconds(2);
    // Sets the trigger pin to HIGH state for 10 microseconds
    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);
    float time = pulseIn(echoPin, HIGH);
    float distance = 0.01723 * time;
    // Serial.println(distance);
    if (distance >= 0 && distance < 113)
    {
        return "low";
    }
    if (distance >= 113 && distance < 224)
    {
        return "mid";
    }
    if (distance >= 224 && distance <= 336)
    {
        return "high";
    }
}

String get_dht(int temp_data)
{

    float voltage = analogRead(temp_data) * 5.0;
    voltage /= 1024.0;
    float val = (voltage - 0.5) * 100.0;
    // Serial.print("temp: ");
    // Serial.println(val);
    if (val <= 0)
    {
        return "low";
    }
    if (val > 0 && val < 100)
    {
        return "mid";
    }
    else
    {
        return "high";
    }
}

String get_ldr(int ldr_pin)
{
    float val = analogRead(ldr_pin);
    // Serial.print("ldr val :");
    // Serial.println(val);
    if (val >= 200 && val < 250)
    {
        return "high";
    }
    if (val >= 250 && val < 275)
    {
        return "mid";
    }
    if (val <= 275 && val <= 400)
    {
        return "low";
    }

    return "low";
}

// takes pin input and gives of high or low
String get_soundSensor(int sound_pin)
{
    // If pin goes LOW, sound is detected
    int val = digitalRead(sound_pin);
    //  Serial.print("sound_sense: ");
    //  Serial.println(val);
    switch (val)
    {
    case 0:
        return "high";
    case 1:
        return "low";
    default:
        return "mid";
    }
}

String get_pir(int pir_pin)
{
    // delay for reading sensor?
    // goes high if detected
    int val = digitalRead(pir_pin);
    delay(1000);
    //  Serial.print("PIR: ");
    //  Serial.println(val);
    switch (val)
    {
    case 0:
        return "high";
    case 1:
        return "low";
    }
}

void loop()
{
    // the sensor combination logic
    // The three ranges are high medium and low
    // StaticJsonDocument<200> doc;
    JsonDocument doc;
    doc["distance"] = get_ultrasonic(ultra_trig, ultra_echo);
    doc["temp"] = get_dht(dht);
    doc["ldr"] = get_ldr(ldr);
    doc["noise"] = get_soundSensor(soundSensor);
    doc["pir"] = get_pir(pir);
    serializeJson(doc, Serial);
    deplay(5000);
}
from openai import OpenAI

from loguru import logger
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

class Models:
    
    @staticmethod
    async def prescribe(context: dict[str, str]):
        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': f'''You are an intelligent model who can prescribe the surrounding using the available conditions being satisfied and context that are available:

                    Context:
                    1. temperature is {context['temp']}
                    2. noise level is {context['noise']}
                    3. distance between the closest object and the sensor is {context['distance']}
                    4. the ambience light level is {context['ldr']}
                    5. PIR returns {context['pir']} value

                    Conditions:
                    1. if noise level is "high", then its a possibility that its an outdoor environment or else its an indoor environment
                    2. if distance to the closest object is "high" it is outdoor, else if it is "low" it is an indoor environment, if it is "mid" it can be indoor or outdoor so check with the remaining contradicting conditions.
                    3. if the ambient light is "low", there is maximum chance that it is an indoor environment or else it is night time, if it is "high" it is outdoor or its an indoor with lights on else its a "mid" ambience meaning we should check with other conditions before deciding environment.
                    4. if PIR reads "high" then there is a mostly likely humans near us which means its a crowded environment or else its not
                    5. if ambient light is "low" and distance "low" then it must be an indoor environment or else its an outdoor environment.
                    6. DO NOT SAY PIR IN THE OUTPUT SENTENCE!! IF PIR VALUE IS HIGH THEN ITS A CROWDED AREA OR ELSE ITS NOT A CROWDED AREA
                    7. MAKE SURE THAT OUTPUT JSON DOES NOT BREAK!!!
                    8. 
                    
                    Example:
                    Distance: Mid / LOW
                    Temperature: Mid / LOW
                    LDR: Low
                    Noise: Low
                    PIR: High or LOW
                    This description suggests an indoor environment.
                    
                    Now give me a very detailed perception of the environment using the context information and satisfy the conditions (MUST) and return the output in the form of json and the sentence should have information in words and not numbers based on the values given:

                    and form a meaningful sentence using the perception values form each output and put that aswell into the json output which should always have the keys:
                    "environment", "sentence"

                    what kind of environment does it match? for example its a forest / indoor room / conference room / playground / 
                        '''
                }
            ],
            stream=False
        )
        
        # logger.debug(stream.choices[0].message.content)
        return json.loads(stream.choices[0].message.content)
    

    @staticmethod
    async def prescribe_alt(context: dict[str, str]):
        stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': f'''
                            You are an intelligent model who can prescribe the surrounding using the available conditions being satisfied and context that are available:

                    Context:
                    1. temperature is {context['temp']}
                    2. noise level is {context['noise']}
                    3. distance between the closest object and the sensor is {context['distance']}
                    4. the ambience light level is {context['ldr']}
                    5. PIR returns {context['pir']} value

                    Conditions:
                    1. if noise level is "high", then its a possibility that its an outdoor environment or else its an indoor environment
                    2. if distance to the closest object is "high" it is outdoor, else if it is "low" it is an indoor environment, if it is "mid" it can be indoor or outdoor so check with the remaining contradicting conditions.
                    3. if the ambient light is "low", there is maximum chance that it is an indoor environment or else it is night time, if it is "high" it is outdoor or its an indoor with lights on else its a "mid" ambience meaning we should check with other conditions before deciding environment.
                    4. if PIR reads "high" then there is a mostly likely humans near us which means its a crowded environment or else its not
                    5. if ambient light is "low" and distance "low" then it must be an indoor environment or else its an outdoor environment.
                    6. DO NOT SAY PIR IN THE OUTPUT SENTENCE!! IF PIR VALUE IS HIGH THEN ITS A CROWDED AREA OR ELSE ITS NOT A CROWDED AREA
                    7. MAKE SURE THAT OUTPUT JSON DOES NOT BREAK!!!
                    8. 
                    
                    Example:
                    Distance: Mid / LOW
                    Temperature: Mid / LOW
                    LDR: Low
                    Noise: Low
                    PIR: High or LOW
                    This description suggests an indoor environment.
                    
                    Now give me a very detailed perception of the environment using the context information and satisfy the conditions (MUST) and return the output in the form of json and the sentence should have information in words and not numbers based on the values given:

                    and form a meaningful sentence using the perception values form each output and put that aswell into the json output which should always have the keys:
                    "environment", "sentence"

                    what kind of environment does it match? for example its a forest / indoor room / conference room / playground /


                    *Outdoor Area Description:*

                    - *Distance:* 
                    - High: Objects are far away, indicating an open space or a large outdoor area with minimal obstruction.
                    - Mid: Some objects are present at a moderate distance, suggesting moderate obstruction or structures in the vicinity.
                    - Low: Objects are nearby, indicating a densely populated area with significant obstruction or obstacles.

                    - *Temperature:*
                    - High: The temperature is warm or hot, indicating a sunny day or exposure to direct sunlight.
                    - Mid: The temperature is moderate, suggesting a comfortable outdoor environment with mild weather conditions.
                    - Low: The temperature is cold, indicating cooler weather or possibly night-time conditions.

                    - *LDR (Light Dependent Resistor):*
                    - High: The ambient light level is bright, suggesting ample sunlight or well-lit surroundings.
                    - Mid: The ambient light level is moderate, indicating partially shaded or dimly lit areas.
                    - Low: The ambient light level is low, suggesting darkness or limited visibility, possibly indicating nighttime.

                    - *Noise:*
                    - High: There is a significant amount of noise, suggesting a busy or crowded environment with high activity levels.
                    - Mid: There is moderate noise, indicating some activity or occasional sounds in the surroundings.
                    - Low: There is minimal noise, suggesting a quiet or serene environment with little to no activity.

                    
                    - *PIR (Passive Infrared) / Motion:*
                    - High: There is frequent motion detected, indicating the presence of multiple moving objects or individuals.
                    - Mid: There is occasional motion detected, suggesting sporadic movement or activity in the area.
                    - Low: There is little to no motion detected, indicating a static or dormant environment with minimal activity.

                    This description provides a comprehensive overview of an outdoor area, considering key parameters such as distance, temperature, light, noise, and motion, each categorized into three degrees of truth (high, mid, low) based on their respective sensor readings or observations.

                    *Wild Environment Description:*

                    - *Distance:*
                    - High: Objects are distant, indicating vast open plains or expansive wilderness with minimal obstruction.
                    - Mid: Some objects are present at a moderate distance, suggesting scattered trees or occasional terrain features.
                    - Low: Objects are nearby, indicating dense vegetation or rugged terrain with significant obstruction.

                    - *Temperature:*
                    - High: The temperature is hot, indicating exposure to direct sunlight or a scorching day in the wild.
                    - Mid: The temperature is moderate, suggesting a comfortable outdoor environment with pleasant weather conditions.
                    - Low: The temperature is cold, indicating cooler weather or the onset of nightfall in the wilderness.

                    - *PIR (Passive Infrared) / Motion Sensors:*
                    - High: PIR sensors detect frequent motion, indicating the presence of active wildlife or possibly human activity.
                    - Mid: PIR sensors detect occasional motion, suggesting intermittent movement of animals or environmental factors.
                    - Low: PIR sensors detect minimal motion, indicating a tranquil setting with little disturbance or activity.

                    - *Noise:*
                    - High: There is significant noise, suggesting a bustling ecosystem with calls of animals, rustling leaves, and the rush of water.
                    - Mid: There is moderate noise, indicating occasional wildlife activity or natural phenomena such as wind rustling through trees.
                    - Low: There is minimal noise, suggesting a serene and quiet environment with only faint whispers of nature's symphony.
                        '''
                }
            ],
            stream=False
        )
        
        # logger.debug(stream.choices[0].message.content)
        return json.loads(stream.choices[0].message.content)
    

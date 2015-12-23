import random
import itertools

weather_responses = {
    "Red sky at night, shepherd's delight. Red sky in the morning, shepherd's warning",
    "When the wind is out of the East, tis never good for man nor beast",
    "When halo rings Moon or Sun, rain's approaching on the run",
    "Mackerel sky and mare's tails make tall ships carry low sails",
    "Rain before seven, fine by eleven",
    "If crows fly low, winds going to blow; If crows fly high, winds going to die.",
    "Whether it's cold or whether it's hot; We shall have weather, whether or not!",
    "No weather is ill, if the wind is still",
    "Rain, rain go away; come back another day"
}
weather_prompts = {
    "Hows the weather where you are?": weather_responses,
    "So what about all this weather we've been having?": weather_responses
}

general_prompts = \
    {
        "How are you today?":
            {
                "I'm SUPER! Thanks for asking!",
                "Fair to middlin'",
                "Can't complain"
            }
    }

prompts = {}
prompts.update(general_prompts)
prompts.update(weather_prompts)

prompts_list = [str(key) for key in prompts.keys()]

prompts_and_responses = set()
prompts_and_responses.update(prompts.keys())
for responses in prompts.values():
    prompts_and_responses.update(responses)


def response(text_stripped):
    if text_stripped in prompts:
        return random.choice(prompts[text_stripped])
    else:
        return random.choice(prompts)

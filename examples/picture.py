#!/usr/bin/env python

from jarvisbot import JarvisBot

client = JarvisBot(api_key="123",
                   base_url="http://418a4e4d87705aaf21.jarvisbot.live/sdapi/v1", )

prompt = "An astronaut lounging in a tropical resort in space, pixel art"
model = "dall-e-3"
batch_count = 4


def main() -> None:
    print(f"Prompt: {prompt}")
    # Generate an image based on the prompt
    response = client.images.generate(prompt=prompt, model=model, n=4)
    # print(response)

    images = response.model_extra.get("images")
    for index, image in enumerate(images):
        import base64
        bs = base64.b64decode(image)
        with open(f"jarvisbot_sd_{index}.png", "wb") as f:
            f.write(bs)


if __name__ == "__main__":
    main()

# z-AutoArtistMix
an interesting method to weigh artists.

This is a webui extension (https://github.com/Panchovix/stable-diffusion-webui-reForge) that is meant to be used with noob vpred 1.0 (https://civitai.com/models/833294/noobai-xl-nai-xl)
(idk about other webui variations, i only tested with reforge)

to install it simply clone this repo into the extensions folder or install from URL in the webui.

the concept is simple, this extension scans your prompt for artist tags and weighs them automatically depending on how many images of them were included in noob's dataset. (https://huggingface.co/datasets/Laxhar/noob-wiki/tree/main)

this method should work on any model that has been trained long enough on a single dataset and had it's creator(s) disclose how many images of each artist were in the dataset, but so far only noob fits in this category afaik.

it is not a perfect science, but for the most part it works pretty well, you can get pretty decent results even with 10+ artists prompted.

here is a comparison:

before:![image](https://github.com/user-attachments/assets/9f0616c2-c2ae-4752-98c1-bf573690f0f4)
(yoako, wanimaru, valitran, automatic giraffe, neco, koto inari, quasarcake, greatodoggo, ooji, miyao ryuu)

after: ![image](https://github.com/user-attachments/assets/4195c243-a4d9-4ce5-9a7b-5530f8bc8279)
(yoako:0.3933054393), (wanimaru:0.7324675325), valitran, (automatic giraffe:0.7249357326), (neco:0.7249357326), (koto inari:0.2351959967), (quasarcake:0.9894736842), (greatodoggo:0.7249357326), (ooji:0.7230769231), (miyao ryuu:0.7212276215)


# Usage

![image](https://github.com/user-attachments/assets/7c485618-cc9f-4501-9528-7e29db9c4d3a)

I recommend using the "Min" method with max tag weight of 1 for the best consistency.

in the "Min" method the artist with the lowest amount of dataset entries is set to max tag weight and others are weighted down accordingly.

example: input: quasarcake, wlop, greatodoggo - output: (quasarcake:1), (wlop:0.782967033), (greatodoggo:0.7326478149)
("Min" method with max tag weight of 1)

in the "Average" method, the average of all artists's entry count is used as a baseline, therefore weights can end up higher than 1. this method works well if all artists have a relatively similar entry count.

also, in the "Average" method, max tag weight simply acts as a weight cap. recommended <1.2.

example: input: quasarcake, wlop, greatodoggo - output: (quasarcake:1.214035088), (wlop:0.9505494505), (greatodoggo:0.8894601542),
("Average" method with max tag weight of 2)

# Credit

some of the prompt replacement code i stole from tipo.py (https://github.com/KohakuBlueleaf/z-tipo-extension) thanks kblue

basically all the other coding was done by deepseek.

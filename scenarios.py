"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# Ten pieces I wrote myself, no AI help, each at least 50 words (criterion 3
# needs that). Used by criteria 1, 2 (first five) and 3.
# Pieces alternate between my astrophotography final report and my New
# Testament course reflection, so the first five (criterion 2) mix both.
# Kept exactly as I wrote them, typos included.
MY_WRITING = [
    # astrophotography report, paragraph 1
    "The type of astrophotography chosen for the final project was deep sky astrophotography. This involves imaging nebulae and galaxies. In order to obtain these images, I used data mining in order to find the deep sky object to process. The object I chose to process was NGC7380, which is the wizard nebula. I chose this object because I knew I wanted to do an image of a nebula, since my group project focused on a galaxy. I decided to look through past data and see images of nebulae that I could possibly find. The data for the image was taken at the UMD observatory, and it was obtained by looking at the 2023-2026 DATA dropbox. I looked through the 2023 folder to find the possible nebula candidates, all starting with “NGC”. I then googled them to see which one I wanted to process. I then decided on imaging NG7380",
    # New Testament reflection, paragraph 1
    "This course has allowed me to grow alot in my awareness of the new testament, and how the new testament came to be. Growing up and even now, reading the bible was soley for devotional purposes, and being able to grow in the relationship with the lord.I had never considered how the books of the bible really came to me, or learned much about the contexts behind the books. Some of the things that were new to me, especially at the beginning, was little things like how Jesus spoke in Aramaic, but the bible was written in greek. Furthermore exploring how some stories of the bible, such as jesus walking on water and the miraculous catch of fish, and its similarities to greco roman mythology, forced me to wrestle with things about what I knew about my faith. A few other things knew to me at the beginning of class was how stories like mary magdalene and throwing the stones were not in the original greek text. These allowed me to wrestle with my faith in a positive way and allowed me to think critically about things.",
    # astrophotography report, paragraph 2
    "Data mining was used to obtain these images. The telescope used was the 07in AP Refractor, and the camera type was the SBIG ST-10. This equipment is owned by the University of Maryland as they were taken in the UMD observatory. For NGC7380, there was data from 2 nights, October 12th, 2023 and November 1st, 2023.. I decided to use both of these nights when processing the data as it would allow for more data for a clearer stacked image. The 2 filters used in the images were h-alpha and nitrogen, which are both on the red side. This means that the final nebula would show more redness and contrast in this color rather than another color like blue.",
    # New Testament reflection, paragraph 2
    "A few things that were new and interesting to learn was about the actual history behind the gospels, and learning some of the context behind the authors and how and when these texts were written down. For example, learning about how the gospel of John had stories unique to this specific gospel, and how mark’s greek was often very basic and liminal, were all cool things to learn. I do feel as if my engagement with the material at this point started off high, and then possibly reduced a little bit. Some of the stuff, like how Mark was known as peters assistent, and Luke being a physician, were not too knew to me.",
    # astrophotography report, paragraph 3
    "Calibration frames were used to remove any sort of artifacts from the images, such as thermal noise (darks) or readout noise (bias). There were biases and darks taken for each day, and sky flats for each filter (hα, n), for each day. These were then stacked frames to create master versions. I stacked the bias frames to create a master bias frame, then calibrated the darks with the master bias so that the glow and light pixels would be removed. This created the master bias. Flat frames were done to remove uneven illumination and dust spots and were also calibrated with the bias frames. Flat frames were done separately for each day of data and for each filter. Then, I moved on to the light images.These images were calibrated with both the bias master frames, darks, and flats in order to remove readout noise, thermal noise, and any other artifacts like dust. Before moving on to stacking, I had to align the stars on the images.",
    # New Testament reflection, paragraph 3
    "Another area which was interesting to know was the study of the paschal lamb and the passover. Being christian, I had already known alot about what the lamb is and what it really represents, so this part wasn't too new or interesting. However, the context for the passover, and being able to understand how the ancient israelites might have celebrated it, was very cool and enjoyable and allowed me to learn alot. Going off of this, the easter vigil experience was also really cool to me as it gave me another insight into how earlier denominations celebrate easter, rather than the typical modern service that I am used too today.",
    # astrophotography report, paragraph 4
    "Registration was needed to align the stars in the images.  Due to the natural movement of stars from earth's rotation, images taken across the night creates a drift due to the stars moving.  If the images aren't registered, then the stars in the picture would be smeared. For registration, I was able to use 2 pass star alignment with no issues, since there were plenty of identifiable stars in the image. Stacking was done to enhance the individual images from each night and reduce the noise. The more exposures stacked, the more information can be extracted from the image. This increases the signal to noise ratio and allows for a clearer image.  We used sigma clipping for pixel rejection instead of no rejection because of cosmic rays. After each night was stacked, I combined all the nights for one filter to create a final stacked image for that filter. This resulted in 2 stacked filter images, ha and n.  I also did registration again on this final stacked image in order to resolve any alignment issues. Stacking allowed us to create a clean image in each filter for each day.",
    # New Testament reflection, paragraph 4
    "Another part of this class that I appreciated was looking into specifically theories for proving certain stories of the gospels, and how we know those to be true. For example, some of the things we explored were looking at the author credibility of a gospel, and how useful the gospel was to the communities that were forming at that time. We also looked at how some stories are repeated across different gospels, which also can allow us to prove these gospels as true,. Other things like looking into the stories is also beneficial. For example, the stories of Judas betraying Jesus is most likely to have been true and not made up, since a story like that would paint a bad mark on early christianity, and is therefore not likely that early christians made the story up. This type of thinking is not something that I have really engaged with more, so it was cool to be able to look at these different arguments of my faith. Later on in the class, I appreciated learning about how the case for the historical Jesus was proved, especially by looking at how he was seen as an apocalyptic figure whos teachings corresponded to earlies known prophets.",
    # astrophotography report, paragraph 5
    "After stacking was done for each filter, I moved on to stretching. Each filter was stretched after stacking, using generalized hyperbolic stretch transformations to enhance the contrast and brightness. Due to time limitations, I was not able to do any denoising for these images. After each stacked filter image was stretched, I moved on to coloring. Stretching individually before the final coloring seemed to be an easier way to remove any issues I could be having as I moved on. Coloring was done with n on the red channel, since it is the longest wavelength, and H alpha was placed on the green and blue channels. After coloring, I had to play around with the color calibration and stretching in order to bring out more color. Since all the filters are really similar in color, combining them caused the image to have almost a grey tint. To fix this, I played around with stretching just the red channel to hopefully bring out more color. Then I applied a background neutralization to allow the background to be a more neutral darker color. After this, I stretched the whole image again to increase the nebula's brightness and bring out a little more blueness..  After this was done, I used saturation to increase the redness of the filters a little more. After I was satisfied with the final image, I saved it as a jpeg.",
    # New Testament reflection, paragraph 5
    "Towards the end of the semester, I also enjoyed looking into the Pauline letters and exploring how some of these letters are easily attributed to paul, and how some of these letters are said to be written by paul, but was probably written by someone else, perhaps someone paul had lead or taught. Looking at these different things also allowed me to think more deeply and critically of my faith, and explore harder topics that I may not have given much though to before. These topics gave me a deeper appreciation and understanding of the word of God, and why its important to think deeply about these things and understand things more. In terms of a personal context, this class gave me a deeper understanding of my faith and especially church background allowing me to make connections and understand why we have certain books of the bible, etc. In a religious perspective, I definitely do feel I love the bible more and am appreciative of the work human authors, Inspired by the holy spirit, have done in order to put the bible together",
]

# Five chatbot outputs with no edits, each at least 50 words. Used by
# criteria 2 and 3. Generated with Claude on the same topics as my own
# writing, so the comparison tests who wrote it rather than what it's about.
AI_SAMPLES = [
    # choosing a deep sky object from archived data
    "For my astrophotography final project, I wanted a target that would reward careful processing without requiring weeks of my own telescope time, so I turned to archived observatory data. I started by browsing the archive’s catalog and listing deep sky objects that had multiple filters available, since color images need data from more than one wavelength. Next, I narrowed my list by checking how many exposures each object had, how long each exposure was, and whether calibration frames were included. I also thought about how the object would look as a finished picture, favoring a nebula with both bright structure and faint, wispy detail. After comparing a handful of candidates, I chose an emission nebula because its data showed strong signal in several narrowband filters and left plenty of room to practice stacking, stretching, and color mapping. The process taught me that planning and data quality matter just as much as processing skill.",
    # calibration frames
    "Calibration frames are what turn raw astrophotography exposures into clean, trustworthy data. Bias frames are the shortest possible exposures, and they record the electronic offset that the camera sensor adds to every image, even when no light reaches it. Dark frames are taken with the same exposure time and temperature as the light frames but with the sensor covered, so they capture thermal noise and hot pixels that build up during long exposures. Flat frames are taken of an evenly lit surface, and they reveal vignetting, dust shadows, and uneven sensitivity across the sensor. During processing, I combine each type of frame into a master calibration frame to reduce random noise. I then subtract the master bias and master dark from each light frame and divide the result by the master flat. This removes unwanted artifacts before stacking and leaves a cleaner image where real astronomical detail is easier to separate from noise.",
    # stacking, stretching and coloring
    "To process my nebula image, I started with separate grayscale datasets from the H-alpha and nitrogen filters. After calibrating each set, I aligned the frames and stacked them in software, which averages many exposures together to boost the signal and reduce random noise. The stacked images looked dark and flat at first because the data was linear, with most of the detail packed into the darkest tones. To fix that, I stretched each image, gradually adjusting the histogram so that the faint gas clouds became visible without blowing out the brightest stars and cores. I was careful not to stretch too aggressively, since that can amplify noise and flatten contrast. Next came coloring. Because narrowband filters capture only specific wavelengths, they have no natural color, so I assigned each dataset to a color channel to create a false-color image. I mapped H-alpha to one channel, nitrogen to another, and blended the two to fill in the third, which separated the different gas structures visually. Finally, I adjusted color balance, saturation, and contrast, and trimmed the star brightness slightly so they would not overpower the nebula. The result felt like discovering hidden detail that was always there in the data.",
    # New Testament history reflection
    "This course changed the way I think about how the New Testament came to be. Before taking it, I pictured the gospels as straightforward eyewitness accounts written shortly after the events they describe. I learned instead that they were written decades after Jesus’s life, drawing on oral traditions, earlier written sources, and the particular concerns of each author’s community. Comparing Matthew, Mark, and Luke showed me how much the writers shared in structure and content, and how they also shaped and arranged the material differently to emphasize their own themes. John, with its distinct style and theology, made the variety even clearer. I also learned how early Christian writings were copied, circulated, and eventually collected into a canon over several centuries. At first, these ideas felt unsettling, but they gave me a deeper appreciation for the texts as human documents written for real audiences with real purposes. I now read the gospels more carefully, asking who wrote them, why, and for whom.",
    # historical Jesus and Paul reflection
    "Studying the historical Jesus and Paul’s letters affected my faith in ways I did not expect. I came into the course with a fairly simple view of Jesus, shaped mostly by what I had heard growing up. Learning to examine him as a figure in first-century Jewish Palestine, using historical methods and asking what can be known about him, challenged many of my assumptions. At times it was uncomfortable, because it forced me to separate what I had always believed from what the evidence could support. Reading Paul’s letters, which are the earliest writings in the New Testament, was equally eye-opening. I saw that they were practical messages written to specific communities facing specific problems, not polished theological textbooks. That context made Paul feel more human and his arguments more vivid. Over time, my faith shifted from certainty toward something more thoughtful and open to questions. I no longer feel I need every answer to hold onto what matters to me. Instead, I value the effort to understand where these ideas came from, and I feel my faith is more honest and more my own as a result.",
]

SCENARIOS = [
    {
        "name": "c1 my own writing",
        "criterion": 1,
        # Target: at most 1 of 10 labelled high-confidence AI, in every trial.
        "texts": MY_WRITING,
    },
    {
        "name": "c2 ai samples",
        "criterion": 2,
        # Target: the average of these is at least 0.30 above the average of
        # "c2 human samples", in every trial.
        "texts": AI_SAMPLES,
    },
    {
        "name": "c2 human samples",
        "criterion": 2,
        "texts": MY_WRITING[:5],
    },
    {
        "name": "c3 label coverage",
        "criterion": 3,
        # Target: at least one of these gets each of the three labels, in
        # every trial. All are full paragraphs of 50+ words.
        "texts": MY_WRITING + AI_SAMPLES,
    },
    {
        "name": "c5 bad input",
        "criterion": 5,
        # Target: every one of these gets a 400 and no content_id, in every
        # trial. Each has its own creator_id so the rate limiter doesn't
        # count them all against one address.
        "bodies": [
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t  ", "creator_id": "eval_bad_whitespace"},
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": ["a", "list"], "creator_id": "eval_bad_list"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "word " * 2001, "creator_id": "eval_bad_huge"},  # 10,005 chars
        ],
    },

    # Criterion 4 (appeals) is tested by hand, not here: it needs a submission
    # first and then an appeal against the content_id that came back, and
    # run_eval.py only calls /submit.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems

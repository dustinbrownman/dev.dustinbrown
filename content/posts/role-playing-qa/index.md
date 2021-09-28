---
title: "Role Playing QA"
date: 2021-09-28T03:40:21Z
draft: true
toc: false
images: [dice.jpg]
tags:
  - QA
  - development
  - role playing
author:
  name: "Dustin Brown"
  email: "me@dustinbrown.dev"
---

{{< full-width-image "dice.jpg" 250 Center >}}

This week I ran a fun experiment and thought others would get a kick out of it.

Over the last couple of weeks I've been working on an automation project. I can't go into details, but the project was unlike anything I'd ever worked on. Lots of tinkering, testing, and trial and error.

Nearing the end, I knew I needed some folks to walk through the different workflows I'd created and made sure they made sense to people that, well, weren't me. I tapped my fellow teammates who only vaguely knew what I was working on and they agreed to help.

Here was the challenge though: how could I give my teammates instructions on what to test without just walking them through the flows step by steps?

## BDD - Behavioral dungeon delving

I was reminded of my first job where we used [Cucumber-style tests](https://en.wikipedia.org/wiki/Cucumber_(software)). These tests attempted to, in very human-readable language, walk through each step of our mission critical processes. Here's an example what one of those tests might look like:

```
As a potential customer
When I visit the homepage
 And I scroll down to the bottom of the page
 And I click the "sign up" button
Then I see the sign up form
```

One of the big advantage of these kinds of tests is they cause you to be explicit about the important flows within your application. This looks a lot like what I myself was going through as I built out this project.

"Okay, I'm a content owner who just got pinged on this new GitHub issue"

"I visit the issue page and see instructions"

"I have verified things are up to date"

Having that mental checklist of what the user flow should look like is crucial during development. But if I were to give these steps to my teammates I would miss testing _its intuitive-ness_.

These flow are going to be used by real people. They aren't concerned with, nor do they know about an aribitrary set of steps I've lined up. They have circumstances and goals. When my application is finally released, there is only one question I care about: **does it help people reach their goals given their circumstances?**

## Character sheets

"Okay, here is your background info for the test. It's supposed to be somewhat vague, but if you're really confused let me know. I'm going to run the script in about 10 minutes. Thank you again for agreeing to help!"

I was going out on a limb here. I didn't want to waste my teammates' time with my silly experiment, but I knew I couldn't just spell out steps without spoiling the point of their testing. So I rolled the dice and gave each person a character.

Like an old [text adventure game](https://en.wikipedia.org/wiki/Interactive_fiction), each person was set up with a brief but rich background.

<div class="zork">
    <p>
      You helped build Git Smart, a tool for teaching new developers how to use Git.
    </p>
    <p>
      At first, you were the only developer on the project. As it's grown, you've decided to collaborate with other devs (some of the same folks that learned via Git Smart). You're looking for a platform to collaborate on and have decided to investigate GitHub.
    </p>
    <p>
      Once you read what they have to offer on their homepage, you are compelled to sign up and try out their service.
    </p>
</div>

(Forgive the cheesiness, this is just for illustrative purposes only 😅)

- I gave the "character sheets" to each of my teammates, ran the script to ping them, and waited
- maybe something about their reaction "whoa, this is fun!"
- Sucess!
  - Each person understood the assignment and knew what they needed to do
  - Got some good feedback on how each flow can be approved
    - "I didn't see anything happen when I did X so I tried it again
    - "I wasn't sure what to fill in at this point"


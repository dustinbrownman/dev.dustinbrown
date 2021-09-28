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

These week a ran a fun experiment I thought others would get a kick out of.

Over the last couple of weeks I've been working on an automation project. I can't go into details, but the project was unlike anything I'd ever worked on. Lots of tinkering, testing, and trial and error.

Nearing the end, I knew I needed some folks to walk through the different workflows I'd created and made sure they made sense to people that, well, weren't me. I tapped my fellow teammates who only vaguely knew what I was working on and they agreed to help.

Here was the challenge though: how could I give my teammates instructions on what to test without just walking them through the flows step by steps?

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

These flow are going to be used by real people. They aren't concerned with, nor do they know about an aribitrary set of steps I've lined up. They have circumstances and goals. When my application is finally released, there is only one question I care about: **does it help its users reach their goals given their circumstances?**

## In progress...

This is where the fun part comes in

I gave each of my teammates a character. This character had a (brief but rich) history. I gave them a vague setup of who they were and some understanding of their goals

I then told them they'd be mentioned in an upcoming issue. Give their character background, they were supposed to do whatever seemed natural

---
layout: blogpost
tag: gamedev
title: Wave Function Collapse Implementation
description: Describing my wave function collapse implementation
---

At some point I decided to use wave function collapse for level generation in a game prototype I was working on.

However the implementatiosn I was finding online were all focused on pulling local patterns from an example image,
and I wanted to describe all possible tile patterns and adjust their odds of appearing.
This way I could do things like outlaw any patterns with roads diagonally adjacent to each other,
and control how zig-zaggy the level would be by changing the priority of T intersection or + intersections.

Here's the result, black areas are roads and white areas are blocks of buildings:

<iframe width="560" height="315" src="https://www.youtube.com/embed/yiYwUG49R3g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<!--more-->

## Optimization

I wanted to be able to iterate rapidly on the results, which meant I needed to significantly optimize this over the naive implementation.

This required a bunch of tricks, like memoizing results, swapping inner and outer for loops to get better cache performance, rewriting parts of the algorithm to be equivalent but have better big O performance...

The most complicated thing I did was replace a map of coordinates to vectors of indexes with a one-time allocated 2D array of bitfields.
This drastically improved performance, removing a large number of allocations and pointer hops.
Though it required some nonsense to get rust to be happy with my bitfield's size not being known at compile time.
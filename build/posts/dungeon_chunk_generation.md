@title Dungeon Chunk Generation @date 2024-09-27 @perdayindex 0

## I keep making dungeon generation algorithms

And I'm never quite satisfied with the gameplay of anything I've implemented.

{{{readmore_top}}}

## BSP (Binary Space Partition)

I'm not a big fan of rogue/nethack style "rooms with hallways connecting them" style.
BSP is really easy, but it creates a bunch of isolated rooms connected with hallways.
This means that the actual layout of the rooms barely matters, really the player is exploring a graph.
I really want to have more rooms adjacent to each other, so fights could spill from room to room or players could guess the layout of the space they haven't explored yet.

## Push 'em along a line

An idea I read about somewhere was to place new rooms by always starting at the same position, then picking a random direction and sliding the room in that direction until it can fit.
Eventually rooms stop fitting, and after a certain point you stop.

Then you fill in the gaps between rooms with "hallways" that are essentially big rooms with columns placed in them to make them linear.

This was better, but it still led to things being pretty sparse as rooms tended to barely touch each other and gaps were rarely filled in because a small enough room had to wind up with the right random line.

## Starting over again

So for a new project I started over creating dungeon generation AGAIN.

The main idea is that there are both large scale things I want to be true and small scale things I want to be true, that aren't always in alignment.
For example, nearby rooms should generally be pretty connected to each other.
Thus most adjacent rooms should have doorways between them.
But also there should be noticeable zones to the dungeon so that different areas can feel unique!

My solution is to use a BSP to split the dungeon up into Chunks, do a smaller form of room generation on each Chunk, and then connect all the chunks together.

That way certain things can be true for individual chunks (highly locally connected) but not true for every single thing on the map at once (chunk boundaries only have 1 doorway across them).

## Visualization

Unlike some previous projects with dungeon generation, the actual gameplay I'm working on this time is 3D.
Which means that it's harder to use the game itself as debug visualization while developing the level generation. Whoops.

I had been looking into rust GUI libraries anyways (I'm doing all of this in rust btw) so I threw something together to visualize what I was working on.

## Bam!

<div class="image-container">
<img class="wideimage" src="{{relativelink}}images/level_gen/rooms_without_doors_gui.png" alt="eframe GUI with a bunch of colorful rectangles">
</div>

On the left is the grid broken up into chunks with a BSP.
On the right is those grids filled with rooms, until no more rooms could fit.

I'm pretty happy with this density and general layout of rooms, and I was able to tweak things quickly until I was happy.

You can see that it's clearly not finished, as the chunks don't necessarily connect to each other, but it's a pretty good start.

## Doors

Then I added doors! This required turning all the empty space in the chunks into weirdly shaped rooms.
Then connecting all rooms that share a boundary with a door, and all chunks that share a boundary with a door.
This guarantees all rooms are connected.

<div class="image-container">
<img class="wideimage" src="{{relativelink}}images/level_gen/rooms_with_doors_gui.jpg" alt="eframe GUI with a bunch of colorful rectangles and white lines representing doors">
</div>

## In game display!

<div class="image-container">
<img class="wideimage" src="{{relativelink}}images/level_gen/generated_rooms_with_doors.jpg" alt="3D game with a bunch of rooms with floors and walls and doors">
</div>

And here it is in game! (Assets are from <a href="https://kaylousberg.itch.io/kaykit-dungeon-remastered">this pretty awesome asset pack</a>)

## Next steps

Next, I want to improve how chunks are connected a bit.
I liked the chunks being not entirely flush, so I'd like to use hallways to ensure chunks connect but in a more interesting way than simply filling all squares in a chunk with hallways.

I'd also like to remove some of the doors so that not EVERY possible connection has a door, but ensuring that everything is still connected.

Overall, this has been fun so far and I'm really glad I put in the time to get a debug GUI up and running!

{{{readmore_bottom}}}

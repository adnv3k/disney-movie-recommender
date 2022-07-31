from recommender.recc import Recommendations

# Sample movie_list
movie_list = [
    "Ratatouille",
    "The Conjuring",
    "Spider-Man: Into the Spider-Verse",
    "Dune",
    "Shutter Island",
    "Interstellar",
    "Annabelle",
    "Doctor Strange in the Multiverse of Madness",
    "Doctor Strange",
    "Pirates of the Caribbean",
    "Harry Potter",
    "The Wolf of Wall Street"
]
movie_list = [
    "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe",
    "The Chronicles of Narnia: Prince Caspian",
    "The Chronicles of Narnia: The Voyage of the Dawn Treader",
    "A Bug's Life",
    "Toy Story",
    "Toy Story 2",
    "Toy Story 3",
    "Mulan",
    "Beauty and The Beast",
    "A Goofy Movie",
    "Hunchback of Notre Dame",
    "Aristocats",
    "Mickey, Donald, Goofy: The three musketeers",
    "Pinocchio",
    "Sleeping Beauty",
    "The Little Mermaid",
    "Lion King",
    "Ice Age",
    "Ice Age: The Meltdown",
    "Ice Age: Dawn of the Dinosaurs",
    "Ice Age: Continental Drift",
    "Ice Age: Collision Course",
    "The Incredibles",
    "Incredibles 2",
    "Monsters, Inc.",
    "Monsters University",
    "Lilo & Stitch",
    "Finding Nemo",
    "Finding Dory",
    "Tarzan",
    "Meet the Robinsons",
    "Ratatouille",
    "Cars",
    "Cars 2",
    "Cars 3"
]
recc = Recommendations(movie_list)
print(recc.get_reccs())
print(recc.json())
print(recc.filter_streaming_availability(provider="Netflix"))
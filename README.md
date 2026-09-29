# The Diridon Divide

A live, shared map for playing a real-world game of hide-and-seek across the South Bay, centered on **San Jose Diridon Station**. It's based on the "Hide and Seek" format from the YouTube series **Jet Lag: The Game**.

You don't need to have seen the show. This page explains the game, then explains how the app helps you play it.

---

## What is Jet Lag: The Game?

*Jet Lag: The Game* is a travel game show on YouTube. In its **Hide and Seek** seasons, one player hides somewhere in a large area (a city, a region, sometimes a whole country) and the other players try to find them using public transit.

The seekers can't just search at random. They find the hider by **asking questions**, and every answer rules out part of the map. The playable area shrinks question by question until the seekers can reach the hider in person.

The Diridon Divide is a smaller, homemade version of that game played around San Jose.

---

## How the game works

### The roles

- **🦊 Hider:** one person. You pick a spot inside the play area and stay hidden there. You answer the seekers' questions honestly.
- **🔎 Seekers:** everyone else. You work as a team to narrow down where the hider is and then go find them.

### The play area

By default the play area is a **20-mile circle around San Jose Diridon Station**. It covers San Jose, Santa Clara, Sunnyvale, Mountain View, Palo Alto, Milpitas, Campbell, Los Gatos, and more. A dashed circle on the map marks the edge, and the hider must stay inside it. The host can change the center point and radius before the game starts.

### A round, step by step

1. **The hider hides.** They head somewhere inside the boundary while the seekers wait.
2. **The seekers ask questions.** Each question splits the map into two sides, for example "Are you within 1 mile of me?"
3. **The hider answers out loud**, by text or call. The seekers record the answer in the app.
4. **The app shades out** every part of the map the answer ruled out.
5. **The seekers travel** toward whatever area is left, ask more questions, and repeat.
6. **The round ends** when the seekers find the hider. Then you start a new round and someone else can hide.

### The questions

The seekers choose from a fixed deck of questions. Most can only be asked **once per game**, so choose them carefully.

| Type | What it asks | Example |
|---|---|---|
| **Matching** | "Is your nearest ___ the same as my nearest ___?" | "Is your nearest **library** the same as mine?" Categories: shopping malls, public parks, movie theatres, hospitals, libraries. |
| **Water** | "Are you closer to or farther from water than I am?" | Uses real creeks, rivers, lakes, reservoirs, and the Bay. |
| **Radar** | "Are you within X distance of me?" | Choices from 100 m up to 5 miles, plus a custom distance. |
| **Thermometer** | The seeker travels a set distance (500 ft, ½ mi, or 1 mi) and asks "Am I hotter or colder?" | The app tracks the seeker's movement and locks in the question once they've gone far enough. |
| **Powerup: VTA stops** | "Are you within N stops of [VTA station]?" | Counts stops along the VTA light rail lines (Orange, Green, Blue). One per game. |
| **Powerup: Directional** | "Are you north or south of me?" or "east or west of me?" | One per round. |

The hider can also **veto** a question. It then goes back into the deck so the seekers can ask it again later.

---

## What the app does for you

In the show, players work out the eliminated areas by hand on a paper map with a compass and ruler. This app does that part for you:

- **Exact boundaries.** It uses real map data (about 60 VTA stations, 700+ parks, 120+ libraries, 20+ hospitals, and hundreds of creeks and lakes from OpenStreetMap) to draw each question's dividing line precisely.
- **Preview before you ask.** Seekers can tap a question to see how it would split the map from where they're standing before they commit to it.
- **Shared, live map.** Everyone in the room sees the same shaded map, question log, and seeker positions, updated in real time.
- **The hider stays hidden.** Seekers' positions are shared with everyone. The hider's position is never shared and only appears on the hider's own screen.
- **GPS or tap-to-place.** Use your phone's GPS, or tap the map to set your location by hand.
- **Survives phone life.** If you lock your phone, switch apps, or reload, reopening the same link puts you back in your room with your name, role, and host status.

---

## How to play with friends

1. **Everyone opens the same link** on their phone.
2. **One person taps "Create a new room instead."** They become the **host** and get a short room code such as `FOXY`.
3. **Everyone else enters their name and that room code** and taps **Join room**.
4. In the **lobby**, each person picks **🦊 Hider** or **🔎 Seeker**. The host can adjust the play area here.
5. **The host taps "Start game."**
6. Seekers go to the **Questions** tab, preview a question, and tap **Ask**. They then ask the hider in person, by text, or by phone, and tap the hider's answer (Yes/No, Closer to A/B, or Veto).
7. Watch the map shrink, then go find them.

Other tabs:
- **Log:** every question asked so far and its answer. You can undo an answer that was recorded by mistake.
- **Players:** who's in the room and on which side.
- **Setup:** the play area, **New round** (clears the shading and resets once-per-round powerups), and **End game** (sends everyone back to the lobby to pick new roles).

> **Playing alone?** If the page can't connect to the shared database, it runs in **solo mode**. Everything still works on one phone, but nobody else can join your room.

---

## Tips for first-timers

- **Start with broad questions.** A big radar or a directional powerup early in the round can cut the map roughly in half.
- **Save the precise questions** (small radars, thermometers, matching) for when the area is already small.
- **Hiders:** a spot close to a boundary line is harder to pin down. So is one where your nearest park or library is the same as a lot of other places'.
- **Be honest.** The game only works if the hider answers truthfully.
- **Stay safe.** Obey traffic laws, stay in public places, and agree on a time limit and a way to check in before you start.

---

## Running it yourself

The whole game is one file, **`index.html`**. Open it in a browser, or host it anywhere that serves static files (for example GitHub Pages).

- **Multiplayer sync** uses Firebase Firestore. The config is already in the file. If you fork this project, replace `FIREBASE_CONFIG` in `source/app_shell.html` with your own Firebase project's config.
- When the page is opened as a **Claude artifact**, it uses Claude's built-in shared storage instead and needs no setup.

### Project layout

```
index.html                         The built game (open this)
source/
  app_shell.html                   App code, with placeholders for the map data
  build.py                         Inserts the map data into app_shell.html to produce the game
  jetlag_data/
    geo_data_block.js              Places, water, and VTA stations (from OpenStreetMap)
    vta_line_topology.json         VTA light rail lines and their station order
    clean_data.py                  Data clean-up script
    DATA_NOTES.md                  Where the data came from, plus known quirks
```

To rebuild, edit the paths at the top of `source/build.py` to point at the `source/` folder, then run `python3 source/build.py`.

---

## Credits

- Game format inspired by **[Jet Lag: The Game](https://www.youtube.com/@jetlagthegame)** (Hide and Seek). This is an unofficial fan project and isn't affiliated with the show.
- Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors.

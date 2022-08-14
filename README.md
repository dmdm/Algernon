# Algernon

A bookmark manager.

> Bright moonlight before my bed;\
> I suppose it is frost on the ground.\
> I raise my head to view the bright moon,\
> then lower it, thinking of my home village.\
-- Li Bai


## Code Layout

All Python code resides in the namespace package "algernon".

## Communication

The services communicate via PostgreSQL's LISTEN/NOTIFY mechanism. A service creates a job and sends a notification,
all other services listen on the job channel and process the job they are notified about.

All UIs communicate with the API service via WAMP and crossbar.io. UIs do never communicate with any other service,
only with the API.


    |- UIs --|                       3rd-party               |- Services & DB -----------------------------|


    +--------+                                                                                   +---------+
    | Web UI |----.                                                                         ,----| Fetcher |
    +--------+     \              +-------------+            +-----+    +------------+     /     +---------+
                    |--- WAMP ----| Crossbar.io |--- WAMP ---| API |----| PostgreSQL |----|
    +--------+     /              +-------------+            +-----+    +------------+     \     +---------+
    |  CLI   |----'                                                                         `----| Parser  |
    +--------+                                                                                   +---------+

For quicker turnarounds during development, the CLI imports the API directly. Don't do that in the final productized
CLI.

## Data Flow

    URL  ---> DB ---> Noti ---> Fetcher
                 <---------------'
                 ---> Noti ---> Parser
                 <---------------'


## Musings

- Each URL is unique
- Each URL has exactly one fetched and one parsed resource
- URLs and their resources are by default public, although they belong to an owner
- URL's tags are in the same way public and shared with and edited by everyone
- There will never be a folder tree, but users can save their queries. If a resource needs to appear in a query, but
  does not, add a respective tag
- Full-text search in title, description, and parsed body (HTML and PDF)
- Simple auth: users are stored in a table within Algernon

Future:

- User may override parsed attributes (cstm); these then are private to that user
- User's view of attributes is COALESCE(cstm, parsed)
- Privacy features (still keep URLs and their resources unique; ownership and shares shall be declared in separate 
  table)
- Proper auth


## Endnotes

Poem “Quiet Night Thought” by Li Bai, found on https://mandarinmatrix.org/chinese-poems-about-the-moon/.

《靜夜思》 李 白

床前明月光，疑是地上霜。\
舉頭望明月，低頭思故鄉。

# Athena: A Generative AI application for Education

Athena was designed to be a hacky tool crrated to use LLMs (specifically, OpenAI's `gpt-3.5-turbo` model) in a contextual educational setting. This demo shows how you could use large textual blocks for history or chemistry, and generate a summary, ask questions, get quizzed and get contextually rendered UI (you see nice timeline UIs for history, depending on what text you're analyzing) and you can render molecules for a chemistry chapter/paper.

## Installation

- Start the server:

  - `cd server && docker-compose up`
  - This exposes the Flask endpoint on port 5000.
  - To run the server in a detached mode, add the `-d` flag to the `docker-compose` command.

- Start the client

  - `cd client && npm install && npm start`
  - This starts up the client on port 3000

- Navigate to the browser and go to `localhost:3000`.
  - `http://localhost:3000/chemistry` takes you to the chemistry viewer
  - `http://localhost:3000/history` takes you to the history viewer

# Spec Generator

A powerful, full-stack tool that transforms messy, unstructured product requirements into clean, structured technical specifications — complete with modules, user stories, API endpoints, database schema, and open questions.

Live Demo:  
Frontend: https://spec-generator-psi.vercel.app/  
Backend: https://saadajee-spec-gen.hf.space

### The Problem

Product requirements are often written in natural language, scattered, ambiguous, and inconsistent. Engineers waste hours interpreting vague descriptions, leading to misaligned implementations, missing features, and endless back-and-forth.

### How It Tackles It

Spec Generator uses a multi-step LLM pipeline to intelligently parse and structure requirements:
1. Extracts core modules and features
2. Generates detailed user stories
3. Designs RESTful API endpoints
4. Creates a normalized database schema
5. Identifies open questions and edge cases

It also supports iterative refinementm, you can ask it to "add JWT auth", "use UUIDs", or "add pagination", and it updates the spec coherently while preserving structure.

### Technologies Used

**Frontend**
- Next.js 16 (App Router alternative, using Pages Router)
- React 18
- Tailwind CSS (with custom theme)
- Headless UI (for accessible tabs)
- Axios (API calls)
- react-syntax-highlighter (beautiful JSON display)

**Backend**
- FastAPI (Python)
- Pydantic (request validation)
- LLM pipeline (custom prompts + structured generation)

**Deployment**
- Frontend: Vercel
- Backend: Hugging Face Spaces

### Features

- Clean, industrial-themed dark UI with glitch animations and glow effects
- Responsive design (fully mobile-friendly)
- Real-time generation with loading spinner
- Tabbed output: Modules & Features, User Stories, API Endpoints, Database Schema, Open Questions
- Syntax-highlighted JSON display for API/DB sections
- Export: Copy full spec or download as JSON
- Iterative refinement panel
- Rate limiting and trace ID tracking 
- Version Storing when running locally, u can check the iteration after refining in logs with versions, first and latest in json files
- Graceful error handling (including short input validation)

### Local Setup

1. Clone the repo:
  ```
  git clone https://github.com/Saadajee/spec-generator.git
  cd spec-generator
  ```
2. Start the backend:
  ```
  cd backend
  conda create -n specgen python=3.11  # or use venv
  conda activate specgen
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  ```
  _Backend runs at [http://localhost:8000](http://localhost:8000)_ (You can change the model by going to pipeline.py and modify the function _llm_generate_ to change the LLM)
  
3. Start the frontend:
  ```
  cd frontend
  npm install
  npm run dev
  ```
  _Frontend runs at [http://localhost:3000](http://localhost:3000) (proxies to backend automatically)_

Open browser and start generating specs!

### Online Deployment

Frontend: You can modify the frontend and deploy on vercel, netlify or any platform of your choice.
Backend: Deployed on Hugging Face Spaces but can be deployed on railway or any platform of your choice.

Note: When the backend is fully connected, set NEXT_PUBLIC_BACKEND_URL="https://backend-link.com" in settings to enable live generation on the deployed frontend. And for backend go for the GROQ_API_KEY varuiable

## Notes
- Minimum 50 characters required for meaningful output (prevents poor results from short prompts like "todo app")
- Refinement preserves original trace context for coherent updates
- Built with care for both aesthetics and developer experience
- Demo mode active on Vercel until full backend integration

## Curator

📧 [saadimran7667@gmail.com](saadimran7667@gmail.com)
Happy to collaborate, debug, or help you extend the project further.

### Tidbits
* This tool started as a way to eliminate the most frustrating part of building software: miscommunication between ideas and implementation.
* It’s not perfect, but it gets remarkably close, and it keeps getting better with every refinement.
* Try it. Break it. Improve it. And may your specs be ever structured.

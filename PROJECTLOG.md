# Project Log

Please regularly update this file to record your project progress. You should be updating the project log _at least_ once a fortnight.

## Week 1 — 03/11/25 → 07/11/25
## Summary of Work ##
This week focused on early project exploration.
I researched existing AI marketing tools such as HubSpot and Jasper AI to understand how current systems support small businesses.
This helped me shape how MarketMind will offer more tailored and simplified features.
## Progress Made ##
Created a MoSCoW requirements list to prioritise features.
Outlined initial system functionality.
Discussed project scope and feasibility with my supervisor.
## Reflection ##
Researching competitor tools helped me recognise gaps in the market and refine the direction of my system.
The MoSCoW method made the feature list more manageable and realistic for Semester 1.
## Next Steps ##
Develop simple UI layout sketches.
Begin writing the literature and background sections of the interim report.
Decide which APIs and tools will be used for content generation.
## Week 2 — 10/11/25 → 20/11/25
## Summary of Work ##
This week was dedicated to developing the Interim Report.
I expanded my research on SME marketing challenges and the role of AI in content creation.
I drafted core report sections including the Background, Aims & Objectives, Literature Review, and Requirements Specification.
## Progress Made ##
Completed most sections of the Interim Report.
Wrote the Literature Review using academic and industry sources.
Finalised the initial MoSCoW requirements.
Produced system architecture and early workflow diagrams.
Evaluated technical tools: Flask (backend), PostgreSQL (database), OpenAI API (content generation), scikit-learn (basic analytics).
## Reflection ##
Writing the interim clarified the full project scope and the technical decisions required.
Documenting aims, goals, and risks strengthened my understanding of the workload and constraints.
This week helped me solidify what is achievable in each semester.
## Next Steps ##
Begin setting up the backend architecture.
Finalise diagrams for the interim.
Start early UI/UX planning for the frontend.
## Week 3 — 25/11/25 → 03/12/25
## Summary of Work ##
This week marked the start of technical development.
I created the complete backend folder structure and configured the Flask API environment.
I also set up version control and committed the foundational backend files to GitHub.
## Progress Made ##
Set up the backend project structure (Flask + PostgreSQL + AI service).
Implemented the app factory pattern and CORS configuration.
Added initial API route /api/ai and controller handler.
Created AI service for future OpenAI integration.
Added environment configuration files (.env, requirements.txt).
Initialised GitHub repository and pushed first backend commit.
## Reflection ##
Starting development made the project feel more concrete.
Creating a structured backend early will help keep the codebase scalable and easy to expand.
Using GitHub for version control also ensures proper tracking of changes and supports future collaboration.
## Next Steps ##
Begin implementing PostgreSQL models.
Connect Flask backend to a local database instance.
Start drafting frontend wireframes and user flow diagrams.
Add input validation and error handling to the AI caption endpoint.

## Week 4 [12/01/26 – 17/01/26]

### Summary of Work
This week, I focused on making corrections to my interim report based on the feedback I received. I improved the structure and clarity of several sections, including the literature review, system design, and business development parts of the report.

I also reviewed my overall project plan and finalised preparation to begin backend development next week beyond file structure.

### Progress Made
- Made corrections and improvements to the interim report  
- Improved clarity and organisation of academic writing  
- Addressed feedback related to structure and explanation  
- Finalised plans to start backend development next week  

### Reflection
Working on the interim report corrections helped me better understand how to present my ideas clearly and academically. Addressing feedback allowed me to strengthen weaker sections of the report and improved my confidence moving forward into the development phase.

### Next Steps
- Begin backend development using Flask   
- Start implementing basic backend functionality  

## Week 5 [19/01/26 – 24/01/26]

### Summary of Work
This week, I focused on extending the backend AI functionality by improving the existing AI marketing caption generator. I expanded the AI prompt to produce more detailed, platform-specific, and culturally appropriate outputs, and updated the backend to support additional input parameters such as region. I also tested the updated endpoint using Postman to ensure the changes worked correctly and did not break existing functionality.

---

### Progress Made
- Enhanced the AI prompt to improve structure, tone control, and output consistency  
- Added regional and cultural adaptation support to the caption generator  
- Updated backend routes, controllers, and services to pass new input parameters safely  
- Debugged and resolved server-side errors related to parameter handling  
- Re-tested the caption endpoint using Postman to confirm end-to-end functionality  

---

### Reflection
This week reinforced the importance of maintaining consistency across backend layers when extending functionality. Debugging issues caused by parameter mismatches highlighted how small changes can impact system stability. Improving the AI prompt also demonstrated how prompt design plays a key role in producing high-quality and relevant outputs.

---

### Next Steps
- Implement an additional AI-powered content generation feature (e.g. ad copy)  
- Reuse the existing backend architecture to support the new AI endpoint  
- Test and compare outputs between different AI content types  
- Commit and document the new AI feature as a separate backend milestone  

## Week 6 [26/01/26 – 30/01/26]

### Summary of Work
This week, I focused on extending the backend AI functionality of MarketMind. Building on the existing AI caption generator, I implemented an additional AI-powered ad copy generation feature to support more direct, conversion-focused marketing content for small businesses.

I also integrated AI image generation for ad content, allowing the backend to return both marketing text and a corresponding visual. This required prompt engineering to improve image quality and ensure outputs were appropriate for social media advertising. All AI endpoints were tested using Postman to verify correct request handling and responses.

### Progress Made
- Implemented a new AI ad copy generation endpoint  
- Extended the backend to support multiple AI content types  
- Integrated AI image generation for marketing advertisements  
- Refined AI prompts to improve ad relevance and quality  
- Tested all AI endpoints using Postman  
- Improved error handling and API response structure  

### Reflection
This week helped reinforce the importance of designing a modular and extensible backend architecture. By reusing the existing routes, controllers, and services structure, I was able to add new AI functionality without restructuring the project. Working with AI image generation also highlighted the need for careful prompt design and awareness of API limitations. Overall, this work strengthened the core functionality of the system before introducing database storage.

### Next Steps
- Refine AI output quality and consistency  
- Begin integrating a database to store generated campaigns and content  
- Implement basic user authentication  
- Prepare the backend for future frontend integration  

## Week 7 — (02/02/26-08/02/26)

### Summary of Work  
This week focused on consolidating the backend foundations of the MarketMind platform and defining a clear development roadmap to support a more robust and credible system. Alongside this, I implemented the core database structure required for future persistence, ensuring the platform is technically prepared for authentication, analytics, and evaluation features.

Work this week was also guided by preparation for interview and viva demonstration, with an emphasis on architectural decisions and system design rather than simple API usage.

---

### Progress Made  
- Implemented and verified the database infrastructure using Flask, PostgreSQL, SQLAlchemy, and Flask-Migrate.  
- Created and applied initial database tables using SQLAlchemy models and migrations, confirming that schema changes can be safely managed and evolved over time.  
- Validated end-to-end backend plumbing, including app factory configuration, environment-based configuration loading, and model registration for migration detection.  
- Explored and refined a development roadmap aimed at evolving the system into a full platform, prioritising authentication, persistence, and evaluation layers.  
- Planned enhancements to improve AI output reliability and user confidence during demonstrations, including content/tone evaluation and analytics.

---

### Reflection  
Implementing actual database tables helped solidify the system’s backend architecture and clarified how future features will integrate with persistent storage. Establishing the database layer early reduces technical risk later in the project and provides a strong foundation for user accounts, historical data, and analytics.

Additionally, focusing on roadmap planning improved my confidence in explaining the project’s technical direction during interviews, allowing me to present MarketMind as a scalable platform rather than a simple AI generation tool.

---

### Next Steps  
- Implement basic user authentication to enable accounts and user-specific persistence.  
- Store AI-generated outputs in the database to support history and evaluation.  
- Introduce a lightweight content/tone evaluation layer to assess generated content.  
- Develop simple analytics and visualisations to support interview and demo scenarios.
 ## Week 8 — (09/02/26–15/02/26)

### Summary of Work  
This week focused on strengthening the core backend generation pipeline and improving overall system robustness. The aim was to move MarketMind beyond simple AI output generation and toward a structured, reliable, and extensible architecture capable of supporting evaluation and adaptive features.

Particular attention was given to integrating persistent storage for generated content and refining the evaluation service to ensure consistent and safe behaviour under edge cases.

---

### Progress Made  

- Implemented and migrated the `GeneratedContent` model to support persistent storage of:
  - Prompt input  
  - Generated output  
  - Timestamps  
  - Evaluation-related fields (tone label and sentiment score)

- Established a complete generation → evaluation → storage workflow:
  1. AI generates content.
  2. Evaluation service processes the output.
  3. Tone classification and score are attached.
  4. Record is saved to the database.

- Refined the evaluation service to improve reliability:
  - Added validation checks for empty or malformed input.
  - Implemented a safe fallback mechanism to prevent system crashes.
  - Standardised tone output to strictly:
    - `positive`
    - `neutral`
    - `negative`
  - Defined a neutral sentiment threshold between `-0.05` and `0.05` to ensure consistent classification.

- Improved backend structure through clearer separation of concerns:
  - Routes handle request logic.
  - Controllers manage orchestration.
  - Services handle AI generation and evaluation logic.
  - Models manage persistence.

- Confirmed that database migrations detect model changes correctly and that records are successfully written and retrieved.

---

### Reflection  

This week significantly improved system stability and architectural clarity. Introducing strict evaluation rules and safe fallback handling ensures the platform behaves predictably during demonstrations and prevents runtime failures caused by unexpected AI outputs.

Persisting generated content lays the groundwork for analytics, historical tracking, and future adaptive features such as brand voice learning and feedback-based optimisation.

The project is now transitioning from a proof-of-concept AI tool to a structured backend platform with measurable output evaluation.

---

### Next Steps  

- Develop a basic frontend interface (React) with minimal styling and no advanced functionality, focused on:
  - Displaying generation input/output.
  - Showing tone classification results.
  - Preparing layout structure for future interaction.

- Design and begin implementation of a text-based feedback loop mechanism to:
  - Capture user preference or rating of generated outputs.
  - Store feedback in the database.
  - Prepare the foundation for adaptive brand voice learning.

## Week 9 — (23/02/26–26/02/26)

### Summary of Work  
This week focused on transitioning MarketMind from a single-output generation flow into a structured A/B feedback system with stronger backend architecture and security consistency. I prioritised modularity, protected routes, schema evolution, and end-to-end validation of generation and selection workflows.

---

### Progress Made  
- Completed a staged backend refactor and feature rollout with traceable commits:
  - `refactor(ai)` provider abstraction for OpenAI/Stability and stronger platform/region prompting.
  - `feat(auth)` JWT enforcement added for ad-copy route to align protected AI endpoints.
  - `scaffold` feedback/publishing service stubs and standardised API error responses.
  - `feat(db)` added `BrandMemory` model + migration (one-to-one user memory profile).
  - `feat(ai)` extended `GeneratedContent` schema for A/B variants (eval JSON, selected state, original prompt).
  - `feat(ai)` implemented A/B generation endpoint and persisted variant outputs.
  - `feat(ai)` implemented selection feedback loop with memory persistence updates.
- Notable implementation outcomes:
  - Routes/controllers now avoid model SDK-specific logic through provider abstraction.
  - Error responses are consistent across auth and AI routes using shared helper and JWT callbacks.
  - Ownership-safe selection logic was validated (cross-user selection blocked; owner selection succeeds).
  - Migration issue (`can't adapt type 'dict'`) was resolved by serialising JSON payloads during backfill.
- Key commit evidence (this week):
  - `c4c92d8f` add A/B generation, selection feedback loop, and brand memory persistence
  - `bafd6df5` add A/B text generation endpoint and extend `GeneratedContent` schema
  - `554cca04` add `BrandMemory` model and migration with one-to-one user link
  - `19d152d7` scaffold feedback/publishing modules and standardise error responses
  - `983d53f8` require JWT for ad-copy endpoint

---

### Reflection  
This week highlighted the importance of sequencing architectural work before feature expansion. Implementing abstractions and consistent error handling first made later endpoint development cleaner and easier to debug. Migration issues also reinforced that schema changes must be validated against the real database engine, not only compile checks. Overall, the system now better demonstrates technical depth through modular design, secure multi-user behaviour, and a working feedback loop foundation.

---

### Next Steps  
- Implement `GET /api/ai/history` with user-scoped records and selected-variant visibility.
- Implement `GET /api/ai/analytics` with baseline metrics for generation and sentiment distribution.
- Integrate memory-aware prompt augmentation into generation flow using persisted `BrandMemory`.
- Expand testing evidence (integration/smoke) for dissertation results and viva preparation.

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

## Week 11 — 01/03/26–13/03/26

### Summary of Work

This period focused on moving MarketMind from a stable MVP toward a more entrepreneurial
product workflow. Development concentrated on strengthening the end-to-end application
flow, improving generation usability, introducing deeper image controls, implementing
analytics visualisation, and adding an early monetisation layer through a simulated
credit and transaction system.

---

### Progress Made

#### Frontend & System Stability
- Stabilised the **end-to-end frontend workflow** across authentication, generation,
  content history, and the analytics dashboard.
- Completed **frontend–backend wiring** for:
  - `login / register` with **JWT persistence**
  - **text generation** with explicit variant save flow
  - **ad copy generation** with selectable image options
  - **history rendering**
  - **analytics data visualisation**

#### Generation UX Improvements
- Split the **Generate page** into two distinct sections:
  - Text Generation
  - Ad Copy + Image Generation
- Introduced a clear **separation between choosing and saving text variants**, reducing
  accidental saves and giving users more control over which outputs are persisted.

#### Ad Image Persistence
- The **selected ad image is now saved alongside the generated content**.
- Saved images are surfaced within dashboard previews and the history view, ensuring
  visual outputs remain tied to the original generation context.

#### Data Model & API Extensions
- Added **ad image selection fields** to the persisted content model.
- Added a dedicated **ad-image selection endpoint**.
- **Restructured the history API response** to separate text generation records from
  ad copy generation records, improving data organisation and simplifying frontend
  rendering logic.

#### Analytics Improvements
- Added tracking of **image creativity modes**: Safe, Balanced, Bold, and Experimental.
- Replaced raw numerical displays with **visual chart-based analytics** for improved
  interpretability.

#### Advanced Image Controls
New user-facing image generation inputs:
- Style preset, aspect ratio, shot type, include/avoid keywords,
  colour palette, and high-quality toggle.

Supporting backend additions:
- Enum validation, prompt mapping, and aspect ratio → dimension mapping.

#### Image Generation Reliability
- **High-quality rendering adjustments** for sharper outputs.
- **Retry and fallback handling** for provider timeouts (e.g. 504 errors).
- **Cleaner error responses** to surface partial generation failures more clearly.

#### Monetisation Mechanics
- Introduced a **per-user credit balance** with generation-based deductions.
- Added **simulated subscription tiers** (Basic, Pro, Growth) for testing purchase flows.
- Built a **transaction log table** capturing credit purchases, usage, and generation costs.
- Credit spending is **validated and enforced on generation routes**.
- Added purchase simulation endpoints, a **Plans & Credits UI**, and a
  **live credit balance display** in the application layout.

---

### Reflection

This development period significantly increased the technical depth and product realism
of the MarketMind system beyond basic LLM integration. The system now demonstrates:

- persistent user feedback and selection tracking across modules,
- clearer generation workflows with explicit save behaviour,
- visual analytics dashboards,
- advanced image generation parameters with validation,
- and monetisation-aware backend mechanics via credits and transaction logging.

A notable operational risk encountered was **third-party image provider instability**,
particularly 504 gateway timeouts. Addressing this required implementing graceful
degradation strategies — retry logic and fallback behaviour — which are essential
considerations for production-grade AI systems.

---

### Next Steps

#### Business Profile System
- Implement **business profile registration** from the dashboard.
- Each profile will include: business name, vision statement, brand values,
  industry, and target audience.

#### Campaign Management
- Introduce campaign organisation under each business profile.
- Features include: campaign creation, grouping generated content by campaign,
  and campaign-level evaluation and analytics.

#### Logo Generation
- Integrate **logo generation per business profile** using the existing image AI pipeline.
- Surface generated logos on the dashboard and optionally composite them into
  advertisement image prompts.

#### Emotion Evaluation Upgrade (VAD Model)
- Upgrade the evaluation service from a 3-level tone classification to a
  **7-level VAD scale** (very positive → very negative).
- Surface numeric **valence, arousal, and dominance scores** in the UI per generation.

#### Target Tone Controls
- Add **VAD target sliders** within an Advanced Settings panel on the Generate page.
- Users will specify a desired emotional tone and receive an **alignment score**
  comparing generated output against their target emotion profile.

#### Regeneration System
- Introduce a **guided regeneration workflow** allowing users to describe desired
  changes (e.g. "make it more persuasive") or select quick presets:
  more positive, more formal, shorter, more energetic.
- Revisions will be **linked to the original generation** to maintain traceability.

#### Brand-Aware Prompting
- Use the **active business profile context** during generation so the same prompt
  produces measurably different outputs across profiles — demonstrating brand voice divergence.

#### Expanded Analytics
- Add **per-campaign performance metrics**, **brand voice tracking**, and
  **VAD target alignment averages** to the analytics dashboard.

## Week 12 — 13/03/26–27/03/26

### Summary of Work
This period focused on significantly upgrading the evaluation layer of MarketMind, moving from a basic 3-level tone classification toward a richer VAD (Valence, Arousal, Dominance) model with granular scoring. Alongside the backend improvements, the frontend evaluation display was redesigned to surface these scores meaningfully to the user, and the Generate page was restructured to reduce form complexity.

---

### Progress Made

#### VAD Evaluation Upgrade (Backend)
- Expanded tone classification from **3 levels to 7 levels**: Very Positive, Positive, Slightly Positive, Neutral, Slightly Negative, Negative, Very Negative.
- Expanded arousal and dominance classification from 3 to **5 levels** each.
- Extended intensifier, assertive, and hedge word lists to improve scoring sensitivity across all three VAD dimensions.
- Added `tone_label`, `tone_category`, `arousal_label`, and `dominance_label` to the evaluation response.
- Retained `tone_category` as a backward-compatible 3-way field so existing analytics charts remain unaffected.
- Added human-readable `explanation` descriptions for all tone, energy, and voice levels.

#### Evaluation UI (Frontend)
- Redesigned the `EvalBlock` component to display granular labels (e.g. "Very Positive", "High", "Assertive") instead of raw programmatic keys.
- Introduced a `ScoreBar` component with colour-coded progress bars — teal for valence, amber for energy, purple for voice — filled based on numeric scores.
- Added an **A vs B Comparison** panel below generated variants showing side-by-side labels and numeric scores per dimension with a plain English verdict (e.g. "→ B scores higher").
- Comparison uses a 0.05 threshold to avoid flagging negligible differences as meaningful.
- Graceful fallback for older records that do not contain the new VAD fields.

#### Generate Page UX (Frontend)
- Refactored both the text and ad copy forms into **required** and **advanced** sections.
- Required fields (business name, industry, target audience, description, tone, platform) are always visible.
- Optional and advanced fields hidden behind a collapsible **Advanced Settings ▾** toggle per form.
- Text advanced section: goal, length, region.
- Ad copy advanced section: goal, length, region, offer, CTA, colour palette, style preset, aspect ratio, shot type, keywords, high quality toggle.

---

### Reflection
Upgrading the evaluation layer added meaningful technical depth to the system. The shift from a 3-level label to a 7-level tone scale with numeric VAD scores makes the evaluation genuinely useful rather than decorative, and directly supports the dissertation objective around output evaluation. The A vs B comparison panel addresses a real usability gap — previously both variants could return near-identical looking scores even when the generated text differed significantly in style.

Refactoring the Generate forms improved the experience for first-time users considerably. The ad copy form previously presented 14 fields at once, which was overwhelming. Collapsing these behind a toggle aligns better with the SME user persona central to this project.

---

### Next Steps
- Implement VAD target sliders so users can specify a desired emotional tone and receive an alignment score.
- Build the Regenerate endpoint to allow guided revision of existing outputs.
- Implement the BusinessProfile and Campaign database models as the foundation for brand-aware generation and campaign analytics.

## Week 13 — 31/03/26–14/04/26

### Summary of Work
This period focused on introducing the business profile and campaign systems, closing the human-in-the-loop feedback loop, and significantly upgrading the analytics, history, and generate pages. The brand memory aggregation was rewritten, campaign-level analytics were introduced, VAD emotional targeting was added, and several usability improvements were made across the application.

---

### Progress Made

#### Business Profile & Brand System
- Implemented the `BusinessProfile` model, migration, and CRUD routes.
- Built the Brand Profile page allowing users to store business name, industry, target audience, and region.
- Generate form now pre-fills from the stored business profile, removing repeated manual input.
- Added logo generation per business profile using the existing image pipeline.
- Added business name greeting to the dashboard and sidebar using brand profile data.

#### Campaign Management
- Introduced the `Campaign` model with name, goal, and VAD target fields (valence, arousal, dominance).
- Built campaign creation, editing, and deletion with VAD target sliders and a toggle to enable emotional targeting.
- Generated content is now linked to a campaign via `campaign_id`.
- Campaign name and goal are injected into generation prompts as contextual instructions.

#### VAD Emotional Targeting
- Added VAD target sliders to the campaign edit and create forms.
- Campaign VAD targets are retrieved during generation and converted to natural language instructions injected into the prompt.
- Alignment score calculated per generation comparing output VAD scores against campaign targets.
- Made tone field optional — when a campaign has VAD targets set, tone is ignored and VAD drives the emotional direction.

#### Brand Memory Aggregation
- Rewrote `update_brand_memory_from_selection` to aggregate preferences from the full selection history using `Counter`-based pattern matching rather than overwriting on each selection.
- Brand memory now reflects the dominant tone, platform, and region across all past selections, and derives style notes and CTA preferences from the 3 most recent selections.
- Brand memory is now injected into both text generation and regeneration prompts, closing the human-in-the-loop feedback loop.
- Removed unused `context` parameter and dead code left over from the previous implementation.

#### AI Provider Reliability
- Added retry logic with delay to both OpenAI text generation and Stability AI image generation.
- Added `timeout=15` to OpenAI API calls to prevent indefinite hangs.
- Retries handle connection errors and 5xx responses; 4xx errors fail immediately without retrying.

#### Regeneration
- Added `POST /api/ai/regenerate/text` and `POST /api/ai/regenerate/ad-copy` endpoints.
- Regenerate re-uses stored prompt fields and overwrites the existing content row in place.
- Costs 1 credit per regeneration.

#### Generate Page
- Added edit and re-evaluate feature — users can manually edit variant text and re-score it against campaign VAD targets without spending credits.
- Added regeneration instruction input field below generated variants.

#### History Page
- Rewrote History page with collapsible `VariantCard` components.
- Selected variants display a teal border and "Selected" badge.
- Added copy buttons, full VAD score display, and campaign name pills.
- Added campaign filter dropdown to filter history by campaign.

#### Campaign Analytics
- Replaced old tone/region/creativity charts with per-campaign analytics.
- Metrics per campaign: generation count, selection rate, dominant tone, average VAD scores, and brand language accuracy.
- Brand language accuracy measures how closely selected content aligns with campaign VAD targets, shown as a colour-coded progress bar.
- Added brand language accuracy trend line chart showing accuracy per selection over time.
- Summary cards show most active and highest accuracy campaigns.
- Backed by new `GET /api/campaigns/analytics` endpoint.

#### Code Quality
- Removed dead `GET /api/ai/analytics` endpoint and `get_user_analytics` controller function.
- Removed `_extract_context_from_prompt` helper no longer needed after analytics refactor.

---

### Reflection
This period brought the most significant technical and usability improvements to the system. Rewriting brand memory aggregation properly closed the human-in-the-loop feedback loop — selections now have a measurable cumulative effect on future generations. Campaign analytics gave the system a clear evaluation layer that directly supports dissertation objectives around brand language alignment and output quality measurement. Introducing VAD emotional targeting at the campaign level added a second dimension of personalisation beyond brand voice, allowing users to specify desired emotional outputs and measure how closely generated content achieves them. The history and generate page improvements address real usability gaps identified through self-testing.

---

### Next Steps
- Implement `preferred_creativity` field in brand memory to track whether users prefer reliable or creative outputs and adapt generation temperature accordingly.
- Add low credits warning when balance drops below a threshold.
- Build demo seed profiles (GlowSkin and FinTrust) with pre-populated history and brand memory to demonstrate brand voice divergence during the dissertation demo.

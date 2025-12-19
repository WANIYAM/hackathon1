# Tasks: ROS 2 Nervous System Module

**Input**: Design documents from `specs/001-ros2-nervous-system/`
**Prerequisites**: plan.md, spec.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the Docusaurus project and configure it for deployment.

- [X] T001 Initialize a new Docusaurus project named `ros2-docs` using the 'classic' theme by running `npx create-docusaurus@latest ros2-docs classic` in the repository root.
- [X] T002 Configure `ros2-docs/docusaurus.config.js` for deployment to GitHub Pages, setting `organizationName`, `projectName`, and other necessary fields.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Prepare the core documentation structure before content is added.

- [X] T003 Delete the default documentation files (e.g., `intro.md`) inside the `ros2-docs/docs/` directory.
- [X] T004 Update the `ros2-docs/sidebars.js` file to define the navigation and sequential order for Chapter 1, Chapter 2, and Chapter 3.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Foundational Concepts (Priority: P1) 🎯 MVP

**Goal**: A student can understand the fundamental role of ROS 2 as a "nervous system" for robots.

**Independent Test**: Review the rendered Chapter 1 on the local Docusaurus development server (`npm run start` in `ros2-docs/`) to verify its clarity, accuracy, and completeness.

### Implementation for User Story 1

- [X] T005 [P] [US1] Create the content file `ros2-docs/docs/chapter1.md`.
- [X] T006 [US1] Write the full content for Chapter 1 in `ros2-docs/docs/chapter1.md`, explaining the foundational concepts of ROS 2, physical AI, and embodied intelligence.

**Checkpoint**: At this point, User Story 1 should be fully readable and testable on the local development server.

---

## Phase 4: User Story 2 - Core Building Blocks (Priority: P2)

**Goal**: A student can define and differentiate between ROS 2 Nodes, Topics, and Services.

**Independent Test**: Review the rendered Chapter 2, ensuring the explanations of primitives are clear and any diagrams are correctly displayed.

### Implementation for User Story 2

- [X] T007 [P] [US2] Create the content file `ros2-docs/docs/chapter2.md`.
- [X] T008 [US2] Write the full content for Chapter 2 in `ros2-docs/docs/chapter2.md`, providing detailed explanations for ROS 2 Nodes, Topics, and Services.

**Checkpoint**: At this point, User Stories 1 AND 2 should both be readable and correctly ordered in the sidebar.

---

## Phase 5: User Story 3 - Python Application (Priority: P3)

**Goal**: A student can apply their Python knowledge to write a simple ROS 2 node using `rclpy`.

**Independent Test**: Execute the Python code examples from a local terminal to verify they run without errors against a running ROS 2 environment.

### Implementation for User Story 3

- [X] T009 [P] [US3] Create the content file `ros2-docs/docs/chapter3.md`.
- [X] T010 [US3] Write the full content for Chapter 3 in `ros2-docs/docs/chapter3.md`, focusing on practical `rclpy` examples and an introduction to URDF.
- [X] T011 [P] [US3] Create and add the Python code examples (e.g., `publisher.py`, `subscriber.py`) to a new directory: `ros2-docs/src/code-examples/`.

**Checkpoint**: All three chapters should now be complete and readable.

---

## Phase 6: Polish & Deployment

**Purpose**: Final review and setup of automated deployment.

- [X] T012 Proofread all three chapters for grammar, spelling, and technical accuracy.
- [X] T013 Run a full local build of the Docusaurus site via `npm run build` within the `ros2-docs/` directory to ensure there are no errors.
- [X] T014 Create a GitHub Actions workflow file at `.github/workflows/deploy-docs.yml` to automatically build and deploy the site from the `ros2-docs` directory to GitHub Pages on pushes to the `main` branch.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Stories (Phases 3-5)**: Depend on Foundational phase completion.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### User Story Dependencies

- The user stories represent a sequential learning path (US1 → US2 → US3). While the content creation tasks can happen in parallel, they should be presented to the learner in order.

### Parallel Opportunities

- Once Phase 2 is complete, different authors could work on the content for US1, US2, and US3 simultaneously, as they are separate markdown files.
  - T006 [US1] Write content for Chapter 1
  - T008 [US2] Write content for Chapter 2
  - T010 [US3] Write content for Chapter 3

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Deploy Chapter 1 as a standalone, valuable piece of content.

### Incremental Delivery

1. Add User Story 2 → Deploy Chapters 1 & 2.
2. Add User Story 3 → Deploy the complete 3-chapter module.

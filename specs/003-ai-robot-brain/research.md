# Research: Adding a Docusaurus Module

**Decision**: A new module will be added to the Docusaurus site by creating a new directory in `ros2-docs/docs`, adding markdown files for each chapter, and updating `ros2-docs/sidebars.js`.

**Rationale**: This is the standard and recommended way to add new content to a Docusaurus v2 site.

**Alternatives considered**: None, as this is the idiomatic approach for the framework.

## Implementation Steps

1.  **Create Module Directory**: Create a new directory named `module3` inside `ros2-docs/docs`.
2.  **Create Chapter Files**: Inside `ros2-docs/docs/module3`, create three new markdown files:
    *   `isaac-sim-photorealism.md`
    *   `isaac-ros-vslam.md`
    *   `nav2-path-planning.md`
3.  **Create Category File**: Inside `ros2-docs/docs/module3`, create a `_category_.json` file to define the sidebar label for the module.
4.  **Update Sidebar Configuration**: Edit `ros2-docs/sidebars.js` to add the new `module3` directory to the sidebar.

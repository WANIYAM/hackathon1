// ros2-docs/src/utils/selectionUtils.js

export const getSelectedText = () => {
  if (typeof window !== 'undefined') {
    // Ensure this runs only in browser environment
    const selection = window.getSelection();
    if (selection && selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      return range.toString().trim();
    }
  }
  return '';
};

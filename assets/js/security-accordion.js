document.addEventListener('DOMContentLoaded', function() {
  const questionButtons = document.querySelectorAll('.question-button > a');
  
  questionButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Find the content div within the same question-button container
      const questionButton = this.parentElement;
      const content = questionButton.querySelector('.question-content');
      
      // Close all other question contents
      document.querySelectorAll('.question-content').forEach(item => {
        if (item !== content) {
          item.style.display = 'none';
          // Reset the + symbol for closed items
          const otherButton = item.parentElement.querySelector('a');
          otherButton.style.setProperty('--after-content', "'+'");
        }
      });
      
      // Toggle this content
      if (content.style.display === 'block') {
        content.style.display = 'none';
        this.style.setProperty('--after-content', "'+'");
      } else {
        content.style.display = 'block';
        this.style.setProperty('--after-content', "'-'");
      }
    });
  });
});

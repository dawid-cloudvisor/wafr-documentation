document.addEventListener('DOMContentLoaded', function() {
  const questionButtons = document.querySelectorAll('.question-button > a');
  
  questionButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      
      const content = this.nextElementSibling;
      
      // Close all other question contents
      document.querySelectorAll('.question-content').forEach(item => {
        if (item !== content) {
          item.style.display = 'none';
        }
      });
      
      // Toggle this content
      if (content.style.display === 'block') {
        content.style.display = 'none';
      } else {
        content.style.display = 'block';
      }
    });
  });
});

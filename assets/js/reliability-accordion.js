console.log('Reliability accordion script loading...');

document.addEventListener('DOMContentLoaded', function() {
  console.log('Reliability accordion DOM loaded');
  
  const questionButtons = document.querySelectorAll('.question-button > a');
  console.log('Found question buttons:', questionButtons.length);
  
  questionButtons.forEach((button, index) => {
    console.log('Setting up button', index);
    
    button.addEventListener('click', function(e) {
      e.preventDefault();
      console.log('Button clicked:', index);
      
      // Find the content div within the same question-button container
      const questionButton = this.parentElement;
      const content = questionButton.querySelector('.question-content');
      
      if (!content) {
        console.error('No content found for button', index);
        return;
      }
      
      console.log('Content found, current display:', content.style.display);
      
      // Close all other question contents
      document.querySelectorAll('.question-content').forEach(item => {
        if (item !== content) {
          item.style.display = 'none';
          // Reset the + symbol for closed items
          const otherButton = item.parentElement.querySelector('a');
          if (otherButton) {
            otherButton.style.setProperty('--after-content', "'+'");
          }
        }
      });
      
      // Toggle this content
      if (content.style.display === 'block') {
        content.style.display = 'none';
        this.style.setProperty('--after-content', "'+'");
        console.log('Closed content');
      } else {
        content.style.display = 'block';
        this.style.setProperty('--after-content', "'-'");
        console.log('Opened content');
        
      }
    });
  });
  
  console.log('Reliability accordion setup complete');
});

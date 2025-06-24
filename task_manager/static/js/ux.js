document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.edit-inline').forEach(icon => {
    icon.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const tabLink = this.closest('.tab-link');
      const nameSpan = tabLink.querySelector('.project-name');
      const currentName = nameSpan.textContent.trim();
      const projectId = tabLink.dataset.projectId;

      // Create input field
      const input = document.createElement('input');
      input.type = 'text';
      input.value = currentName;
      input.className = 'edit-input';
      nameSpan.replaceWith(input);
      input.focus();

      input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
          const newName = input.value.trim();
          if (newName && newName !== currentName) {
            fetch(`/rename_project/${projectId}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ new_name: newName })
            })
              .then(response => response.ok ? location.reload() : alert('Rename failed'));
          } else {
            input.replaceWith(nameSpan); // Cancel if unchanged
          }
        }
      });

      input.addEventListener('blur', () => input.replaceWith(nameSpan)); // Cancel on blur
    });
  });
  document.querySelectorAll('.edit-desc').forEach(icon => {
    icon.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const td = this.closest('td');
      const span = td.querySelector('.desc-text');
      const currentText = span.textContent.trim();
      const taskId = span.dataset.taskId;

      const input = document.createElement('input');
      input.type = 'text';
      input.value = currentText;
      input.className = 'edit-input';
      span.replaceWith(input);
      input.focus();

      input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
          const newText = input.value.trim();
          if (newText && newText !== currentText) {
            fetch(`/rename_task_desc/${taskId}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ new_desc: newText })
            })
              .then(res => res.ok ? location.reload() : alert('Update failed'));
          } else {
            input.replaceWith(span);
          }
        }
      });

      input.addEventListener('blur', () => input.replaceWith(span));
    });
  });
});
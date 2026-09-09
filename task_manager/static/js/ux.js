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

// Edit Due Date
$(document).on("click", ".edit-due-date", function () {
    const span = $(this).siblings("span[data-due-date]");
    const taskId = span.closest("tr").find(".desc-text").data("task-id");
    const currentDue = span.data("due-date") || "";

    // Create an input[type=date]
    const input = $("<input>", {
        type: "date",
        class: "due-date-input",
        value: currentDue,
    });

    // Replace the span with the input
    span.replaceWith(input);
    input.focus();

    // When user leaves the field, submit the update
    input.on("change blur", function () {
        const newDue = input.val(); // empty string clears the date

        $.ajax({
            url: `/edit_due_date/${taskId}`,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ due_date: newDue }),
            success: function () {
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                let textValue = "";
                let cssClass = "due-date";

                if (!newDue) {
                    // No date → show "Unassigned"
                    textValue = "Unassigned";
                } else {
                    // Convert YYYY-MM-DD → DD/MM
                    textValue = formatDateDisplay(newDue);

                    const due = new Date(newDue);
                    const isOverdue = due < today;
                    cssClass = isOverdue ? "overdue" : "due-date";
                }

                const updatedSpan = $("<span>", {
                    class: cssClass,
                    "data-due-date": newDue,
                    text: textValue,
                });

                input.replaceWith(updatedSpan);
            },
            error: function () {
                alert("Invalid date format. Use YYYY-MM-DD.");
                input.replaceWith(span); // revert
            },
        });
    });
});

// Helper: convert YYYY-MM-DD → DD/MM
function formatDateDisplay(isoDate) {
    if (!isoDate) return "";
    const [year, month, day] = isoDate.split("-");
    return `${day}/${month}`;
}

(function () {
  function parsePositionValue(textarea) {
    const value = textarea.value.trim();
    if (!value) {
      return null;
    }

    try {
      const parsed = JSON.parse(value);
      if (
        parsed &&
        typeof parsed === "object" &&
        typeof parsed.x === "number" &&
        typeof parsed.y === "number"
      ) {
        return {
          x: Math.max(0, Math.min(1, parsed.x)),
          y: Math.max(0, Math.min(1, parsed.y)),
        };
      }
    } catch (error) {
      return null;
    }

    return null;
  }

  function writePositionValue(textarea, position) {
    if (!position) {
      textarea.value = "";
    } else {
      textarea.value = JSON.stringify(
        {
          x: Number(position.x.toFixed(3)),
          y: Number(position.y.toFixed(3)),
        },
        null,
        2
      );
    }

    textarea.dispatchEvent(new Event("input", { bubbles: true }));
    textarea.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function attachPositionPicker(textarea) {
    if (textarea.dataset.positionPickerEnhanced === "true") {
      return;
    }

    const arenaShape = textarea.dataset.arenaShape || "SQUARE";
    const wrapper = document.createElement("div");
    wrapper.className = "rc-position-picker";

    const picker = document.createElement("div");
    picker.className = "rc-position-picker__arena";
    picker.tabIndex = 0;
    if (arenaShape === "CIRCLE") {
      picker.classList.add("rc-position-picker__arena--circle");
    }

    const marker = document.createElement("span");
    marker.className = "rc-position-picker__marker";
    picker.appendChild(marker);

    const legend = document.createElement("div");
    legend.className = "rc-position-picker__legend";

    const readout = document.createElement("span");
    readout.className = "rc-position-picker__coords";

    const actions = document.createElement("div");
    actions.className = "rc-position-picker__actions";

    const centerButton = document.createElement("button");
    centerButton.type = "button";
    centerButton.className = "button";
    centerButton.textContent = "Center";
    centerButton.addEventListener("click", function () {
      writePositionValue(textarea, { x: 0.5, y: 0.5 });
      render();
    });

    const clearButton = document.createElement("button");
    clearButton.type = "button";
    clearButton.className = "button";
    clearButton.textContent = "Clear";
    clearButton.addEventListener("click", function () {
      writePositionValue(textarea, null);
      render();
    });

    actions.appendChild(centerButton);
    actions.appendChild(clearButton);
    legend.appendChild(readout);
    legend.appendChild(actions);
    wrapper.appendChild(picker);
    wrapper.appendChild(legend);
    textarea.parentNode.insertBefore(wrapper, textarea);

    function render() {
      const position = parsePositionValue(textarea);
      if (!position) {
        marker.style.display = "none";
        readout.textContent = "No position selected";
        return;
      }

      marker.style.display = "block";
      marker.style.left = `${position.x * 100}%`;
      marker.style.top = `${position.y * 100}%`;
      readout.textContent = `x ${position.x.toFixed(3)} · y ${position.y.toFixed(3)}`;
    }

    function updateFromClientPosition(clientX, clientY) {
      const rect = picker.getBoundingClientRect();
      const x = (clientX - rect.left) / rect.width;
      const y = (clientY - rect.top) / rect.height;
      writePositionValue(textarea, {
        x: Math.max(0, Math.min(1, x)),
        y: Math.max(0, Math.min(1, y)),
      });
      render();
    }

    let dragging = false;

    picker.addEventListener("pointerdown", function (event) {
      dragging = true;
      picker.setPointerCapture(event.pointerId);
      updateFromClientPosition(event.clientX, event.clientY);
    });

    picker.addEventListener("pointermove", function (event) {
      if (!dragging) {
        return;
      }
      updateFromClientPosition(event.clientX, event.clientY);
    });

    picker.addEventListener("pointerup", function (event) {
      dragging = false;
      picker.releasePointerCapture(event.pointerId);
    });

    picker.addEventListener("pointercancel", function (event) {
      dragging = false;
      picker.releasePointerCapture(event.pointerId);
    });

    textarea.addEventListener("input", render);
    render();
    textarea.dataset.positionPickerEnhanced = "true";
  }

  function attachJsonTools(textarea) {
    if (textarea.dataset.jsonEnhanced === "true") {
      return;
    }

    const tools = document.createElement("div");
    tools.className = "rc-json-tools";

    const button = document.createElement("button");
    button.type = "button";
    button.className = "button";
    button.textContent = "Format JSON";
    button.addEventListener("click", function () {
      const value = textarea.value.trim();
      if (!value) {
        textarea.value = "";
        return;
      }

      try {
        textarea.value = JSON.stringify(JSON.parse(value), null, 2);
      } catch (error) {
        window.alert("JSON is invalid. Fix it before formatting.");
      }
    });

    tools.appendChild(button);
    textarea.parentNode.insertBefore(tools, textarea);
    textarea.dataset.jsonEnhanced = "true";
  }

  function init() {
    document
      .querySelectorAll('textarea[data-json-editor="true"]')
      .forEach(attachJsonTools);
    document
      .querySelectorAll('textarea[data-position-picker="true"]')
      .forEach(attachPositionPicker);
  }

  document.addEventListener("DOMContentLoaded", init);
  document.addEventListener("formset:added", init);
})();

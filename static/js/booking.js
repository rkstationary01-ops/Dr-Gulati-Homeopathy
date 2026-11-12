(() => {
  const dateInput = document.getElementById('id_appointment_date');
  const timeSelect = document.getElementById('id_appointment_time');
  const help = document.getElementById('slot-help');
  if (!dateInput || !timeSelect) return;
  const endpoint = '/appointments/available-slots/';
  const loadSlots = async () => {
    const selected = dateInput.value;
    timeSelect.innerHTML = '<option value="">Loading available times…</option>';
    timeSelect.disabled = true;
    if (!selected) { timeSelect.innerHTML = '<option value="">Choose a date first</option>'; help.textContent = 'Choose a date to load available times.'; return; }
    try {
      const response = await fetch(`${endpoint}?date=${encodeURIComponent(selected)}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      const data = await response.json();
      timeSelect.innerHTML = '';
      if (!data.available || data.available.length === 0) {
        timeSelect.innerHTML = '<option value="">No slots available</option>';
        help.textContent = 'No available appointments for this date. Please choose another date.';
      } else {
        timeSelect.innerHTML = '<option value="">Select a time</option>';
        data.available.forEach(slot => {
          const option = document.createElement('option');
          option.value = slot;
          option.textContent = slot;
          timeSelect.appendChild(option);
        });
        help.textContent = `${data.available.length} available time slots.`;
      }
    } catch (error) {
      timeSelect.innerHTML = '<option value="">Could not load slots</option>';
      help.textContent = 'Please refresh or contact the clinic.';
    } finally { timeSelect.disabled = false; }
  };
  dateInput.addEventListener('change', loadSlots);
  if (dateInput.value) loadSlots();
})();

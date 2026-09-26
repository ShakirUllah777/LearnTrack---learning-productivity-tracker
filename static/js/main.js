// LearnTrack main scripts

// Auto-dismiss Django flash messages after 5 seconds (5000ms)
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      if (window.bootstrap && window.bootstrap.Alert) {
        const bsAlert = window.bootstrap.Alert.getOrCreateInstance(alert);
        if (bsAlert) {
          bsAlert.close();
          return;
        }
      }
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(function () {
        alert.remove();
      }, 500);
    }, 5000);
  });

  // Interactive SVG Weekly Momentum Chart Tooltip
  const chartSvg = document.getElementById('chart-svg');
  const tooltip = document.getElementById('chart-tooltip');

  if (chartSvg && tooltip) {
    const bars = chartSvg.querySelectorAll('.bar');
    bars.forEach(function(bar) {
      bar.addEventListener('mousemove', function(e) {
        const day = bar.dataset.day || '';
        const date = bar.dataset.date || '';
        const val = bar.dataset.val || '0';
        const tasks = bar.dataset.tasks || '0';
        const skills = bar.dataset.skills || '0';

        tooltip.innerHTML = `<strong>${day} (${date})</strong>: ${val} item${val === '1' ? '' : 's'}<br><small style="opacity:0.85">${tasks} task activity • ${skills} learning activity</small>`;

        const parentRect = chartSvg.parentElement.getBoundingClientRect();
        
        tooltip.style.left = (e.clientX - parentRect.left) + 'px';
        tooltip.style.top = (e.clientY - parentRect.top - 12) + 'px';
        tooltip.classList.add('show');
      });

      bar.addEventListener('mouseleave', function() {
        tooltip.classList.remove('show');
      });
    });
  }
});

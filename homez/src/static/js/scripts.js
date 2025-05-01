document.addEventListener('DOMContentLoaded', function () {
    const algorithmSelect = document.getElementById('algorithm');
    const bandwidthGroup = document.getElementById('bandwidth-group');
    const confidenceGroup = document.getElementById('confidence-group');

    if (algorithmSelect) {
        algorithmSelect.addEventListener('change', function () {
            const value = this.value;
            bandwidthGroup.style.display = value === 'KDE' ? 'block' : 'none';
            confidenceGroup.style.display = value === 'MCP' ? 'block' : 'none';
        });
    }
});
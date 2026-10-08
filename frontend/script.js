// Database madhun live appointments fetch karnyasathi function
async function loadAppointments() {
    try {
        const response = await fetch('/api/appointments');
        const appointments = await response.json();

        // Table Body select kara
        const tableBody = document.querySelector('tbody');
        if (!tableBody) return;

        // Juna mock/dummy data saaf kara
        tableBody.innerHTML = '';

        // Live appointments count (Total Counts) update kara
        const cards = document.querySelectorAll('.card h2, .card div, h2');
        if (cards.length > 0) {
            cards[0].textContent = appointments.length; // Today's Appointments
        }

        // Database madhun aalela pratyek data table madhe taka
        appointments.forEach(app => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="padding: 12px; border-bottom: 1px solid #eee;">${app.patient_name}</td>
                <td style="padding: 12px; border-bottom: 1px solid #eee;">${app.phone_number}</td>
                <td style="padding: 12px; border-bottom: 1px solid #eee;">${app.appointment_time}</td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error('Error fetching appointments:', error);
    }
}

// Page load zalyavar data load kara ani pratyek 5 secondani auto-refresh kara
document.addEventListener('DOMContentLoaded', () => {
    loadAppointments();
    setInterval(loadAppointments, 5000); // 5 sec interval sathi
});
const appState = {
  isAuthenticated: false,
  currentUser: null,
  patients: [
    { id: 1, time: '9:00', name: 'John Doe', age: 30, reason: 'Consultation', status: 'Terminé' },
    { id: 2, time: '10:30', name: 'Jane Smith', age: 25, reason: 'Vaccination', status: 'En attente' },
    { id: 3, time: '14:00', name: 'Lucas Martin', age: 41, reason: 'Renouvellement ordonnance', status: 'Planifié' }
  ],
  appointments: [
    { id: 101, time: '11:30 - 12:00', type: 'Consultation libre', available: true },
    { id: 102, time: '15:30 - 16:00', type: 'Consultation libre', available: true },
    { id: 103, time: '16:30 - 17:00', type: 'Urgence / Téléconsultation', available: true }
  ],
  invoices: [
    { id: 'FAC-2026-081', patient: 'Pierre Durand', amount: 50.0, dueDate: "Aujourd'hui", status: 'En attente' },
    { id: 'FAC-2026-083', patient: 'Amina Benali', amount: 35.0, dueDate: "Aujourd'hui", status: 'En attente' }
  ]
};

const uiController = {
  init() {
    this.setupEventListeners();
    this.renderAll();
  },

  setupEventListeners() {
    document.querySelectorAll('.auth-toggle-btn').forEach((button) => {
      button.addEventListener('click', () => this.toggleAuthentication());
    });

    const nav = document.querySelector('nav');
    if (nav) {
      nav.addEventListener('click', (event) => {
        const link = event.target.closest('a');
        if (!link) return;

        const targetId = link.getAttribute('href');
        const protectedRoutes = ['#dashboard', '#patients', '#rendez-vous', '#factures', '#dossiers', '#conseils', '#contact'];

        if (!appState.isAuthenticated && protectedRoutes.includes(targetId)) {
          event.preventDefault();
          this.showMessage('Veuillez vous connecter pour accéder à cette section.');
          return;
        }

        if (appState.isAuthenticated) {
          event.preventDefault();
          this.showAuthenticatedView(targetId);
        }
      });
    }

    const patientBtn = document.getElementById('add-patient-btn');
    if (patientBtn) {
      patientBtn.addEventListener('click', () => {
        this.showMessage('Fonctionnalité d\'ajout de patient à venir.', 'info');
      });
    }

    const appointmentBtn = document.getElementById('add-appointment-btn');
    if (appointmentBtn) {
      appointmentBtn.addEventListener('click', () => {
        this.showMessage('Fonctionnalité d\'ajout de rendez-vous à venir.', 'info');
      });
    }

    const invoiceBtn = document.getElementById('create-invoice-btn');
    if (invoiceBtn) {
      invoiceBtn.addEventListener('click', () => {
        this.showMessage('Fonctionnalité de création de facture à venir.', 'info');
      });
    }

    const supportBtn = document.getElementById('support-btn');
    if (supportBtn) {
      supportBtn.addEventListener('click', () => {
        this.showMessage('Fonctionnalité de support à venir.', 'info');
      });
    }
  },

  toggleAuthentication() {
    appState.isAuthenticated = !appState.isAuthenticated;

    const publicView = document.getElementById('public-view');
    const dashboardView = document.getElementById('dashboard-view');
    const authButtons = document.querySelectorAll('.auth-toggle-btn');

    if (appState.isAuthenticated) {
      publicView.style.display = 'none';
      dashboardView.style.display = 'block';
      authButtons.forEach((button) => {
        button.textContent = 'Se déconnecter';
      });
      appState.currentUser = { name: 'Dr. Melissa' };
      this.showMessage(`Vous êtes maintenant connecté${appState.currentUser ? ', ' + appState.currentUser.name : ''} !`);
      this.renderAll();
    } else {
      publicView.style.display = 'block';
      dashboardView.style.display = 'none';
      authButtons.forEach((button) => {
        button.textContent = 'Se connecter';
      });
      appState.currentUser = null;
      this.showMessage('Vous êtes maintenant déconnecté.');
    }
  },

  showAuthenticatedView(targetId) {
    const publicView = document.getElementById('public-view');
    const dashboardView = document.getElementById('dashboard-view');
    const targetSection = document.querySelector(targetId);

    if (!publicView || !dashboardView) return;

    if (targetId === '#accueil') {
      publicView.style.display = 'block';
      dashboardView.style.display = 'none';
      return;
    }

    publicView.style.display = 'none';
    dashboardView.style.display = 'block';

    if (targetSection) {
      targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      document.getElementById('dashboard')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  },

  renderPatients() {
    const tbody = document.getElementById('patients-list');
    if (!tbody) return;

    tbody.innerHTML = appState.patients.map((patient) => `
      <tr>
        <td>${patient.time}</td>
        <td><strong>${patient.name}</strong></td>
        <td>${patient.reason}</td>
        <td>${patient.status}</td>
      </tr>
    `).join('');
  },

  renderAppointments() {
    const ul = document.getElementById('appointments-list');
    if (!ul) return;

    ul.innerHTML = appState.appointments.map((appointment) => `
      <li style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem;">
        <div>
          <strong>${appointment.time}</strong> - <span>${appointment.type}</span>
        </div>
        <button
          type="button"
          class="btn btn-sm"
          onclick="window.uiController.bookAppointment(${appointment.id})"
          ${appointment.available ? '' : 'disabled style="opacity: 0.5;"'}
        >
          ${appointment.available ? 'Réserver' : 'Réservé'}
        </button>
      </li>
    `).join('');
  },

  renderInvoices() {
    const tbody = document.getElementById('invoices-list');
    if (!tbody) return;

    tbody.innerHTML = appState.invoices.map((invoice) => `
      <tr>
        <td><strong>${invoice.id}</strong></td>
        <td>${invoice.patient}</td>
        <td><strong>${invoice.amount.toFixed(2)} €</strong></td>
        <td>${invoice.dueDate}</td>
        <td>${invoice.status}</td>
      </tr>
    `).join('');
  },

  renderAll() {
    if (appState.isAuthenticated) {
      this.renderPatients();
      this.renderAppointments();
      this.renderInvoices();
    }
  },

  bookAppointment(appointmentId) {
    const appointment = appState.appointments.find((app) => app.id === appointmentId);
    if (appointment && appointment.available) {
      appointment.available = false;
      this.showMessage(`Rendez-vous réservé pour ${appointment.time}.`);
      this.renderAppointments();
    }
  },

  getBadgeClass(status) {
    switch (status) {
      case 'Terminé':
        return 'badge-success';
      case 'En attente':
        return 'badge-warning';
      case 'Planifié':
        return 'badge-info';
      default:
        return '';
    }
  },

  showMessage(message, type = 'info') {
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.id = 'toastContainer';
      toastContainer.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px;';
      document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    const bgColor = type === 'success' ? '#2f855a' : type === 'warning' ? '#dd6b20' : '#2b6cb0';

    toast.style.cssText = `
      background-color: ${bgColor};
      color: white;
      padding: 12px 20px;
      border-radius: 6px;
      font-size: 0.9rem;
      font-weight: bold;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      opacity: 0;
      transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
      transform: translateY(20px);
    `;

    toast.textContent = message;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
    }, 10);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(20px)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
};

window.uiController = uiController;

document.addEventListener('DOMContentLoaded', () => {
  uiController.init();
});
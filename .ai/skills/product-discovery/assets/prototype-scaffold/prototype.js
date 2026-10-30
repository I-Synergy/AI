/**
 * Prototype Shell - Interactive Navigation and State Management
 * No dependencies. Runs from file:// with no build step.
 */

class PrototypeShell {
  constructor() {
    this.currentScreen = 'SCR-001';
    this.currentPersona = 'user';
    this.currentState = 'default';
    this.currentTheme = this.getInitialTheme();
    this.currentLanguage = 'en';
    this.deviceFrame = 'web-desktop';
    this.screens = [];
    this.i18n = this.initializeI18n();

    this.init();
  }

  init() {
    this.loadScreens();
    this.setupEventListeners();
    this.applyTheme();
    this.applyLanguage();
    this.navigateToScreen();
    this.updateToolbar();
    window.addEventListener('hashchange', () => this.navigateToScreen());
  }

  /**
   * Initialize a minimal i18n dictionary for UI elements.
   * In real use, the user provides their own translation.
   */
  initializeI18n() {
    return {
      en: {
        screens: 'Screens',
        theme: 'Theme',
        language: 'Language',
        state: 'State',
        persona: 'Persona',
        device: 'Device',
        light: 'Light',
        dark: 'Dark',
        highContrast: 'High Contrast',
        default: 'Default',
        empty: 'Empty',
        loading: 'Loading',
        error: 'Error',
        offline: 'Offline',
        success: 'Success',
        noPermission: 'No Permission',
        user: 'User',
        admin: 'Admin',
        guest: 'Guest',
      },
      nl: {
        screens: 'Schermen',
        theme: 'Thema',
        language: 'Taal',
        state: 'Status',
        persona: 'Persona',
        device: 'Apparaat',
        light: 'Licht',
        dark: 'Donker',
        highContrast: 'Hoog Contrast',
        default: 'Standaard',
        empty: 'Leeg',
        loading: 'Laden',
        error: 'Fout',
        offline: 'Offline',
        success: 'Succes',
        noPermission: 'Geen Toestemming',
        user: 'Gebruiker',
        admin: 'Beheerder',
        guest: 'Gast',
      },
      es: {
        screens: 'Pantallas',
        theme: 'Tema',
        language: 'Idioma',
        state: 'Estado',
        persona: 'Persona',
        device: 'Dispositivo',
        light: 'Claro',
        dark: 'Oscuro',
        highContrast: 'Alto Contraste',
        default: 'Predeterminado',
        empty: 'Vacío',
        loading: 'Cargando',
        error: 'Error',
        offline: 'Sin conexión',
        success: 'Éxito',
        noPermission: 'Sin Permiso',
        user: 'Usuario',
        admin: 'Administrador',
        guest: 'Invitado',
      },
    };
  }

  t(key) {
    return this.i18n[this.currentLanguage]?.[key] || key;
  }

  getInitialTheme() {
    const stored = localStorage.getItem('proto-theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  /**
   * Load screen metadata from DOM.
   * Each <section class="screen" id="SCR-001" data-device-frame="..."> is a screen.
   */
  loadScreens() {
    document.querySelectorAll('.screen[id]').forEach((el) => {
      this.screens.push({
        id: el.id,
        label: el.dataset.label || el.id,
        deviceFrame: el.dataset.deviceFrame || 'web-desktop',
      });
    });
  }

  setupEventListeners() {
    // Theme toggle
    document.getElementById('theme-select')?.addEventListener('change', (e) => {
      this.setTheme(e.target.value);
    });

    // Language toggle
    document.getElementById('language-select')?.addEventListener('change', (e) => {
      this.setLanguage(e.target.value);
    });

    // State toggle
    document.getElementById('state-select')?.addEventListener('change', (e) => {
      this.setState(e.target.value);
    });

    // Persona toggle
    document.getElementById('persona-select')?.addEventListener('change', (e) => {
      this.setPersona(e.target.value);
    });

    // Device frame toggle
    document.getElementById('device-select')?.addEventListener('change', (e) => {
      this.setDeviceFrame(e.target.value);
    });

    // Screen links
    document.querySelectorAll('.screen-link').forEach((link) => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const screenId = link.dataset.screen;
        window.location.hash = screenId;
      });
    });
  }

  setTheme(theme) {
    this.currentTheme = theme;
    this.applyTheme();
    localStorage.setItem('proto-theme', theme);
    const select = document.getElementById('theme-select');
    if (select) select.value = theme;
  }

  applyTheme() {
    const body = document.body;
    body.classList.remove('theme-light', 'theme-dark', 'theme-hc');
    if (this.currentTheme === 'dark') {
      body.classList.add('theme-dark');
    } else if (this.currentTheme === 'hc') {
      body.classList.add('theme-hc');
    } else {
      body.classList.add('theme-light');
    }
  }

  setLanguage(lang) {
    this.currentLanguage = lang;
    this.applyLanguage();
    localStorage.setItem('proto-language', lang);
    const select = document.getElementById('language-select');
    if (select) select.value = lang;
  }

  applyLanguage() {
    const html = document.documentElement;
    html.lang = this.currentLanguage;
    if (this.currentLanguage === 'ar' || this.currentLanguage === 'he' || this.currentLanguage === 'ur') {
      html.dir = 'rtl';
    } else {
      html.dir = 'ltr';
    }
    this.updateUILabels();
  }

  updateUILabels() {
    // Update toolbar labels with current language
    const labels = {
      themeLabel: document.querySelector('label[for="theme-select"]'),
      langLabel: document.querySelector('label[for="language-select"]'),
      stateLabel: document.querySelector('label[for="state-select"]'),
      personaLabel: document.querySelector('label[for="persona-select"]'),
      deviceLabel: document.querySelector('label[for="device-select"]'),
      sidebarTitle: document.querySelector('.sidebar-title'),
    };

    if (labels.themeLabel) labels.themeLabel.textContent = this.t('theme') + ':';
    if (labels.langLabel) labels.langLabel.textContent = this.t('language') + ':';
    if (labels.stateLabel) labels.stateLabel.textContent = this.t('state') + ':';
    if (labels.personaLabel) labels.personaLabel.textContent = this.t('persona') + ':';
    if (labels.deviceLabel) labels.deviceLabel.textContent = this.t('device') + ':';
    if (labels.sidebarTitle) labels.sidebarTitle.textContent = this.t('screens');
  }

  setState(state) {
    this.currentState = state;
    const screen = document.getElementById(this.currentScreen);
    if (screen) {
      screen.dataset.state = state;
    }
    const select = document.getElementById('state-select');
    if (select) select.value = state;
  }

  setPersona(persona) {
    this.currentPersona = persona;
    const screen = document.getElementById(this.currentScreen);
    if (screen) {
      screen.dataset.persona = persona;
    }
    const select = document.getElementById('persona-select');
    if (select) select.value = persona;
  }

  setDeviceFrame(device) {
    this.deviceFrame = device;
    const screen = document.getElementById(this.currentScreen);
    if (screen) {
      screen.dataset.deviceFrame = device;
    }
    const select = document.getElementById('device-select');
    if (select) select.value = device;
  }

  navigateToScreen() {
    const hash = window.location.hash.replace('#', '') || 'SCR-001';
    const screen = document.getElementById(hash);

    if (!screen) {
      window.location.hash = 'SCR-001';
      return;
    }

    // Hide all screens
    document.querySelectorAll('.screen').forEach((s) => {
      s.classList.remove('active');
    });

    // Show current screen
    screen.classList.add('active');
    this.currentScreen = hash;

    // Update sidebar highlight
    document.querySelectorAll('.screen-link').forEach((link) => {
      link.classList.remove('active');
      if (link.dataset.screen === hash) {
        link.classList.add('active');
      }
    });

    // Apply current settings to screen
    screen.dataset.state = this.currentState;
    screen.dataset.persona = this.currentPersona;
    screen.dataset.deviceFrame = this.deviceFrame;

    // Announce change for screen readers
    const label = screen.dataset.label || hash;
    const announcement = document.createElement('div');
    announcement.className = 'sr-only';
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.textContent = `Screen ${label} loaded`;
    document.body.appendChild(announcement);
    setTimeout(() => announcement.remove(), 1000);
  }

  updateToolbar() {
    const themeSelect = document.getElementById('theme-select');
    const langSelect = document.getElementById('language-select');

    if (themeSelect) themeSelect.value = this.currentTheme;
    if (langSelect) langSelect.value = this.currentLanguage;
  }
}

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  window.proto = new PrototypeShell();
});

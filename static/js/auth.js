/**
 * Authentication & Demo Quick-Login Manager
 */

const AuthManager = {
  getUser() {
    const raw = localStorage.getItem('mc_user');
    try {
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },

  getToken() {
    return localStorage.getItem('mc_auth_token');
  },

  setSession(token, user) {
    localStorage.setItem('mc_auth_token', token);
    localStorage.setItem('mc_user', JSON.stringify(user));
  },

  clearSession() {
    localStorage.removeItem('mc_auth_token');
    localStorage.removeItem('mc_user');
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  redirectByRole(role) {
    if (role === 'ADMIN') {
      window.location.href = '/admin-portal/';
    } else if (role === 'TEACHER') {
      window.location.href = '/teacher/';
    } else {
      window.location.href = '/student/';
    }
  },

  async login(username_or_email, password) {
    try {
      const res = await api.post('/auth/login/', { username_or_email, password });
      this.setSession(res.token, res.user);
      showToast(`Welcome back, ${res.user.full_name}!`, 'success');
      setTimeout(() => {
        this.redirectByRole(res.user.role);
      }, 600);
      return res;
    } catch (err) {
      showToast(err.message, 'error');
      throw err;
    }
  },

  async demoLogin(role) {
    try {
      showToast(`Logging in as Demo ${role.toUpperCase()}...`, 'info', 2000);
      const res = await api.post('/auth/demo-login/', { role });
      this.setSession(res.token, res.user);
      showToast(`Successfully logged in as ${res.user.full_name} (${res.user.role})!`, 'success');
      setTimeout(() => {
        this.redirectByRole(res.user.role);
      }, 600);
      return res;
    } catch (err) {
      showToast(err.message, 'error');
      throw err;
    }
  },

  async logout() {
    try {
      await api.post('/auth/logout/', {});
    } catch (e) {
      console.warn('Logout API error, clearing local state', e);
    }
    this.clearSession();
    showToast('Logged out successfully.', 'info');
    setTimeout(() => {
      window.location.href = '/login/';
    }, 400);
  },

  protectPage(requiredRole = null) {
    const user = this.getUser();
    if (!this.isAuthenticated() || !user) {
      window.location.href = '/login/';
      return false;
    }

    if (requiredRole) {
      const role = user.role;
      if (requiredRole === 'ADMIN' && role !== 'ADMIN') {
        showToast('Admin privilege required.', 'error');
        this.redirectByRole(role);
        return false;
      }
      if (requiredRole === 'TEACHER' && role !== 'TEACHER' && role !== 'ADMIN') {
        showToast('Teacher privilege required.', 'error');
        this.redirectByRole(role);
        return false;
      }
    }
    return true;
  }
};

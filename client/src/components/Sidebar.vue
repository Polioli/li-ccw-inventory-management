<template>
  <transition name="overlay-fade">
    <div v-if="open" class="sidebar-overlay" @click="$emit('close')"></div>
  </transition>

  <aside class="sidebar" :class="{ open }">
    <div class="sidebar-logo">
      <h1>{{ t('nav.companyName') }}</h1>
      <span class="subtitle">{{ t('nav.subtitle') }}</span>
    </div>

    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item" :class="{ active: route.path === '/' }" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="7" height="9" rx="1" />
          <rect x="14" y="3" width="7" height="5" rx="1" />
          <rect x="14" y="12" width="7" height="9" rx="1" />
          <rect x="3" y="16" width="7" height="5" rx="1" />
        </svg>
        <span>{{ t('nav.overview') }}</span>
      </router-link>

      <router-link to="/inventory" class="nav-item" :class="{ active: route.path === '/inventory' }" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 8l-9-5-9 5 9 5 9-5z" />
          <path d="M3 8v8l9 5 9-5V8" />
          <path d="M12 13v8" />
        </svg>
        <span>{{ t('nav.inventory') }}</span>
      </router-link>

      <router-link to="/orders" class="nav-item" :class="{ active: route.path === '/orders' }" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 2h12v20l-3-2-3 2-3-2-3 2V2z" />
          <line x1="9" y1="7" x2="15" y2="7" />
          <line x1="9" y1="11" x2="15" y2="11" />
          <line x1="9" y1="15" x2="13" y2="15" />
        </svg>
        <span>{{ t('nav.orders') }}</span>
      </router-link>

      <router-link to="/spending" class="nav-item" :class="{ active: route.path === '/spending' }" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="6" width="18" height="13" rx="2" />
          <path d="M3 10h18" />
          <circle cx="17" cy="14.5" r="1.25" fill="currentColor" stroke="none" />
        </svg>
        <span>{{ t('nav.finance') }}</span>
      </router-link>

      <router-link to="/demand" class="nav-item" :class="{ active: route.path === '/demand' }" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="3 17 9 11 13 15 21 5" />
          <polyline points="15 5 21 5 21 11" />
        </svg>
        <span>{{ t('nav.demandForecast') }}</span>
      </router-link>

      <router-link to="/restocking" class="nav-item" :class="{ active: route.path === '/restocking' }" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="9" />
          <path d="M12 7v10M15 9.5c0-1.4-1.3-2.5-3-2.5s-3 1.1-3 2.5 1.3 2.2 3 2.5 3 1.1 3 2.5-1.3 2.5-3 2.5-3-1.1-3-2.5" />
        </svg>
        <span>{{ t('nav.restocking') }}</span>
      </router-link>

      <router-link to="/reports" class="nav-item" :class="{ active: route.path === '/reports' }" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="4" y1="20" x2="4" y2="10" />
          <line x1="10" y1="20" x2="10" y2="4" />
          <line x1="16" y1="20" x2="16" y2="14" />
          <line x1="4" y1="20" x2="20" y2="20" />
        </svg>
        <span>Reports</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useI18n } from '../composables/useI18n'

defineProps({
  open: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

const route = useRoute()
const { t } = useI18n()
</script>

<style scoped>
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: color-mix(in srgb, var(--color-text) 40%, transparent);
  z-index: 150;
}

@media (min-width: 1024px) {
  .sidebar-overlay {
    display: none;
  }
}

.overlay-fade-enter-active,
.overlay-fade-leave-active {
  transition: opacity 0.25s ease;
}

.overlay-fade-enter-from,
.overlay-fade-leave-to {
  opacity: 0;
}

.sidebar {
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  position: sticky;
  top: 0;
  z-index: 200;
  overflow-y: auto;
}

@media (max-width: 1023px) {
  .sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    width: var(--sidebar-width);
    transform: translateX(-100%);
    transition: transform 0.25s ease;
  }

  .sidebar.open {
    transform: translateX(0);
    box-shadow: var(--shadow-dropdown);
  }
}

.sidebar-logo {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-6) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.sidebar-logo h1 {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.sidebar-logo .subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  font-weight: 400;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-4) var(--space-3);
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  border-left: 3px solid transparent;
  color: var(--color-text-muted);
  text-decoration: none;
  font-weight: 500;
  font-size: var(--text-md);
  transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.nav-item svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.nav-item:hover {
  color: var(--color-text);
  background: var(--color-surface-alt);
}

.nav-item.active {
  color: var(--color-primary-600);
  background: var(--color-primary-50);
  border-left-color: var(--color-primary-600);
  font-weight: 600;
}
</style>

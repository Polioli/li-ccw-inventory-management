<template>
  <div class="stat-card">
    <div class="stat-card-label">{{ label }}</div>
    <div class="stat-card-value" :class="`variant-${variant}`">{{ value }}</div>
    <slot />
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    label: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    variant: {
      type: String,
      default: 'neutral',
      validator: (v) => ['success', 'warning', 'danger', 'info', 'neutral'].includes(v)
    }
  }
}
</script>

<style scoped>
/* .stat-card box styling (background, radius, padding, border, shadow, hover)
   comes from the global rule in main.css — reused as-is, not redeclared here. */

.stat-card-label {
  color: var(--color-text-muted);
  font-size: var(--text-base);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--space-3);
}

.stat-card-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
  margin-bottom: var(--space-2);
}

.stat-card-value.variant-success {
  color: var(--color-success-solid);
}

.stat-card-value.variant-warning {
  color: var(--color-warning-solid);
}

.stat-card-value.variant-danger {
  color: var(--color-danger-solid);
}

.stat-card-value.variant-info {
  color: var(--color-info-solid);
}

.stat-card-value.variant-neutral {
  color: var(--color-text);
}
</style>
